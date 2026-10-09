# Playlist2Dancelist

Uses Spotify API, Make sure you set environment variables before use!

Danceability: how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.

This program takes a playlist and organizes it by its danceability rating.

The other file included organizes the playlist based on popularity.

> **Note:** Spotify removed access to the Audio Features endpoint (which provides danceability) for new apps in November 2024, so `sort by danceability.py` only works with apps that had access before then. `sort by popularity.py` still works.
