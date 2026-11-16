from pathlib import Path

import pytest

import src.main as main_module
from src.recommender import (
    Recommender,
    Song,
    UserProfile,
    load_songs,
    recommend_songs,
    score_song,
)


SONGS_CSV = Path(__file__).resolve().parents[1] / "data" / "songs.csv"


def make_song(
    *,
    title: str,
    genre: str = "rock",
    mood: str = "sad",
    energy: float = 0.5,
) -> dict:
    return {
        "title": title,
        "genre": genre,
        "mood": mood,
        "energy": energy,
    }


def test_load_songs_reads_all_18_rows_and_converts_numeric_fields():
    songs = load_songs(str(SONGS_CSV))

    assert len(songs) == 18
    assert songs[0]["id"] == 1
    assert songs[-1]["id"] == 18
    assert songs[0]["title"] == "Sunrise City"
    assert songs[-1]["title"] == "Neon Horizon"
    assert isinstance(songs[0]["energy"], float)
    assert isinstance(songs[0]["tempo_bpm"], float)


def test_genre_match_adds_current_weight():
    score, reasons = score_song(
        {"genre": "pop", "mood": "happy", "energy": 0.0},
        make_song(title="Genre match", genre="pop", energy=1.0),
    )

    assert score == pytest.approx(0.75)
    assert "genre match (+0.75)" in reasons


def test_mood_match_adds_current_weight():
    score, reasons = score_song(
        {"genre": "pop", "mood": "happy", "energy": 0.0},
        make_song(title="Mood match", mood="happy", energy=1.0),
    )

    assert score == pytest.approx(1.5)
    assert "mood match (+1.5)" in reasons


def test_energy_similarity_uses_current_formula():
    score, reasons = score_song(
        {"genre": "pop", "mood": "happy", "energy": 0.8},
        make_song(title="Energy match", energy=0.3),
    )

    expected_energy_score = 2 * (1 - abs(0.3 - 0.8))
    assert score == pytest.approx(expected_energy_score)
    assert f"energy closeness (+{expected_energy_score:.2f})" in reasons


def test_recommendations_are_sorted_highest_score_first():
    songs = [
        make_song(title="Low", energy=0.0),
        make_song(title="High", genre="pop", mood="happy", energy=0.8),
        make_song(title="Middle", genre="pop", energy=0.5),
    ]

    recommendations = recommend_songs(
        {"genre": "pop", "mood": "happy", "energy": 0.8},
        songs,
        k=3,
    )

    scores = [score for _, score, _ in recommendations]
    assert scores == sorted(scores, reverse=True)
    assert [song["title"] for song, _, _ in recommendations] == [
        "High",
        "Middle",
        "Low",
    ]


def test_recommendations_return_only_requested_number():
    songs = [
        make_song(title="First", energy=0.8),
        make_song(title="Second", energy=0.5),
        make_song(title="Third", energy=0.0),
    ]

    recommendations = recommend_songs(
        {"genre": "pop", "mood": "happy", "energy": 0.8},
        songs,
        k=2,
    )

    assert len(recommendations) == 2
    assert [song["title"] for song, _, _ in recommendations] == ["First", "Second"]


def test_load_songs_skips_invalid_rows_and_logs_warnings(tmp_path, caplog):
    csv_path = tmp_path / "songs.csv"
    csv_path.write_text(
        "id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness\n"
        "1,Valid Song,Artist,pop,happy,0.8,120,0.5,0.5,0.5\n"
        "2,,Artist,pop,happy,0.8,120,0.5,0.5,0.5\n"
        "3,Missing Mood,Artist,pop,,0.8,120,0.5,0.5,0.5\n"
        "4,Out of Range,Artist,pop,happy,1.2,120,0.5,0.5,0.5\n"
        "5,Invalid Energy,Artist,pop,happy,high,120,0.5,0.5,0.5\n",
        encoding="utf-8",
    )

    songs = load_songs(str(csv_path))

    assert [song["title"] for song in songs] == ["Valid Song"]
    warnings = [record for record in caplog.records if record.levelname == "WARNING"]
    assert len(warnings) == 4
    assert all("Skipping invalid song row" in record.message for record in warnings)


@pytest.mark.parametrize(
    "user_prefs",
    [
        {"genre": "", "mood": "happy", "energy": 0.5},
        {"genre": "pop", "mood": " ", "energy": 0.5},
        {"genre": "pop", "mood": "happy", "energy": -0.1},
        {"genre": "pop", "mood": "happy", "energy": 1.1},
        {"genre": "pop", "mood": "happy", "energy": "0.5"},
        {"genre": "pop", "mood": "happy"},
    ],
)
def test_recommendations_reject_invalid_user_preferences(user_prefs):
    with pytest.raises(ValueError):
        recommend_songs(user_prefs, [])


def test_main_logs_invalid_profile_and_continues(monkeypatch, caplog):
    monkeypatch.setattr(main_module, "load_songs", lambda _: [])
    attempted_profiles = []

    def fake_recommend_songs(user_prefs, songs, k):
        attempted_profiles.append(user_prefs)
        if user_prefs["genre"] == "pop":
            raise ValueError("invalid test profile")
        return []

    monkeypatch.setattr(main_module, "recommend_songs", fake_recommend_songs)

    main_module.main()

    assert len(attempted_profiles) == 3
    assert "Skipping invalid profile 'Profile 1: High-Energy Pop'" in caplog.text


def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""
