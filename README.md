# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Music apps like Spotify and YouTube recommend songs based on what people like, listen to, or skip. They also look at what similar users enjoy and the type of songs a person likes. My music recommender will focus on finding songs that match the user's favorite genre, mood, and energy level. Songs that match more preferences will be recommended first.

Song Features

Title: Name of the song
Artist: Who sings the song
Genre: Type of music, like pop or rock
Mood: How the song feels, like happy or sad
Energy: Whether the song is calm or energetic
Tempo: How fast or slow the song is

UserProfile Features

Favorite genre: Type of music the user likes
Preferred mood: Mood the user enjoys

Preferred energy: Whether the user likes calm or energetic songs

Preferred tempo: Whether the user prefers fast or slow songs

How Recommendations Work

My program will compare the user's preferences with each song. The more features that match, the higher the song's score will be. Songs with the highest scores will be recommended first.

---
My Algorithm Recipe

My music recommender will give points to songs based on how well they match the user's music taste.

Genre: Add 1.5 points if the genre matches.

Mood: Add 1.5 points if the mood matches.

Energy: Add up to 1 point depending on how close the song's energy is to the user's preferred energy.

The program will add the points together. Songs with higher scores will be recommended first.


Possible Biases

My music recommender might recommend too many songs from the user's favorite genre and miss good songs from other genres. It also only looks at a few features, so it might not always understand what the user really likes.

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:


2. Rooftop Lights (Score: 2.46)
   Reasons: mood match (+1.5), energy closeness (+0.96)

3. Gym Hero (Score: 2.37)
   Reasons: genre match (+1.5), energy closeness (+0.87)

4. Night Drive Loop (Score: 0.95)
   Reasons: energy closeness (+0.95)

5. Golden Steps (Score: 0.94)
   Reasons: energy closeness (+0.94)


---

## Experiments You Tried

Profile 1: High-Energy Pop
--------------------------
1. Sunrise City (Score: 3.92)
   Reasons: genre match (+1.5), mood match (+1.5), energy closeness (+0.92)
2. Gym Hero (Score: 2.47)
   Reasons: genre match (+1.5), energy closeness (+0.97)
3. Rooftop Lights (Score: 2.36)
   Reasons: mood match (+1.5), energy closeness (+0.86)
4. Storm Runner (Score: 0.99)
   Reasons: energy closeness (+0.99)
5. Golden Steps (Score: 0.96)
   Reasons: energy closeness (+0.96)

Profile 2: Chill Lofi
---------------------
1. Library Rain (Score: 3.85)
   Reasons: genre match (+1.5), mood match (+1.5), energy closeness (+0.85)
2. Midnight Coding (Score: 3.78)
   Reasons: genre match (+1.5), mood match (+1.5), energy closeness (+0.78)
3. Spacewalk Thoughts (Score: 2.42)
   Reasons: mood match (+1.5), energy closeness (+0.92)
4. Focus Flow (Score: 2.30)
   Reasons: genre match (+1.5), energy closeness (+0.80)
5. Winter Glass (Score: 0.98)
   Reasons: energy closeness (+0.98)


I changed the genre points from 1.5 to 0.75 and increased the energy points from 1 to 2. I kept the mood points at 1.5.

I wanted to see whether giving more importance to energy would change which songs were recommended.
Profile 3: Deep Intense Rock
----------------------------
1. Storm Runner (Score: 3.94)
   Reasons: genre match (+1.5), mood match (+1.5), energy closeness (+0.94)
2. Gym Hero (Score: 2.42)
   Reasons: mood match (+1.5), energy closeness (+0.92)
3. Golden Steps (Score: 0.99)
   Reasons: energy closeness (+0.99)
4. Sunrise City (Score: 0.97)
   Reasons: energy closeness (+0.97)
5. Rooftop Lights (Score: 0.91)
   Reasons: energy closeness (+0.91)

---
Step 2: Accuracy and Surprises

I tested different music preferences to see if the recommendations made sense. The program gave songs higher scores when their genre, mood, and energy matched the user's preferences.

One thing I noticed is that some songs were recommended even when their genre didn't match. This happened because they still received points for mood or energy. I learned that the scoring system can recommend songs outside the user's favorite genre
## Limitations and Risks

Summarize some limitations of your recommender.

My music recommender only has 18 songs, so it cannot represent everyone's music taste. It also only uses genre, mood, and energy to score songs. Some genres have more songs than others, which can make recommendations less balanced. The program might also recommend similar songs repeatedly instead of introducing different types of music.


---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

I learned that music recommendation systems use information about songs and users to decide what to recommend. I was surprised that changing the scoring points could change the rankings. I also learned that recommendations are not always perfect because a small dataset or limited features can cause some songs to be overlooked. Using AI helped me build the program, but I still needed to test the results and check for problems.



## System Architecture

This diagram shows how my music recommender loads songs, scores them based on music preferences, and displays the top five recommendations for each profile.
