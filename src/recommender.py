import csv
import logging
import math
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the songs this recommender can recommend."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return up to k songs for the user."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain why a song was recommended to the user."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read valid songs from a CSV file and convert their numeric fields."""
    numeric_columns = (
        "energy",
        "tempo_bpm",
        "valence",
        "danceability",
        "acousticness",
    )
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        for row_number, song in enumerate(csv.DictReader(csv_file), start=2):
            try:
                for column in ("title", "genre", "mood"):
                    value = song.get(column)
                    if not isinstance(value, str) or not value.strip():
                        raise ValueError(f"missing or empty {column}")

                song["id"] = int(song["id"])
                for column in numeric_columns:
                    song[column] = float(song[column])
                    if not math.isfinite(song[column]):
                        raise ValueError(f"{column} must be a finite number")

                if not 0 <= song["energy"] <= 1:
                    raise ValueError("energy must be between 0 and 1")
            except (KeyError, TypeError, ValueError) as error:
                logging.warning("Skipping invalid song row %d: %s", row_number, error)
                continue

            songs.append(song)
    return songs


def _validate_user_preferences(user_prefs: Dict) -> None:
    """Raise ValueError when required preferences are missing or invalid."""
    if not isinstance(user_prefs, dict):
        raise ValueError("User preferences must be a dictionary")

    for column in ("genre", "mood"):
        value = user_prefs.get(column)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"User preference '{column}' must not be empty")

    energy = user_prefs.get("energy")
    if (
        isinstance(energy, bool)
        or not isinstance(energy, (int, float))
        or not 0 <= energy <= 1
        or not math.isfinite(energy)
    ):
        raise ValueError("User preference 'energy' must be a number between 0 and 1")


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's genre, mood, and energy preferences."""
    _validate_user_preferences(user_prefs)
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["genre"]:
        score += 0.75
        reasons.append("genre match (+0.75)")

    if song["mood"] == user_prefs["mood"]:
        score += 1.5
        reasons.append("mood match (+1.5)")

    energy_score = 2 * (1 - abs(song["energy"] - user_prefs["energy"]))
    score += energy_score
    reasons.append(f"energy closeness (+{energy_score:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top k scored songs with explanations."""
    _validate_user_preferences(user_prefs)
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored_songs.append((song, score, explanation))

    return sorted(scored_songs, key=lambda result: result[1], reverse=True)[:k]
