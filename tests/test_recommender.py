from pathlib import Path

import pytest

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
