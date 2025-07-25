import ast
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig


@tool
def get_albums_by_artist(artist: str, config: RunnableConfig):
    """
    Get albums by an artist from the music database.

    Args:
        artist (str): The name of the artist to search for albums.
        config (RunnableConfig): The configuration for the runnable.
    Returns:
        str: Database query results containing album titles and artist names.
    """
    return config["db"].run(
        f"""
            SELECT Album.Title, Artist.Name 
            FROM Album 
            JOIN Artist ON Album.ArtistId = Artist.ArtistId 
            WHERE Artist.Name LIKE '%{artist}%';
            """,
        include_columns=True,
    )


@tool
def get_tracks_by_artist(artist: str, config: RunnableConfig):
    """
    Get songs/tracks by an artist (or similar artists) from the music database.

    Args:
        artist (str): The name of the artist to search for tracks.
        config (RunnableConfig): The configuration for the runnable.
    Returns:
        str: Database query results containing song names and artist names.
    """
    return config["db"].run(
        f"""
        SELECT Track.Name as SongName, Artist.Name as ArtistName 
        FROM Album 
        LEFT JOIN Artist ON Album.ArtistId = Artist.ArtistId 
        LEFT JOIN Track ON Track.AlbumId = Album.AlbumId 
        WHERE Artist.Name LIKE '%{artist}%';
        """,
        include_columns=True,
    )


@tool
def get_songs_by_genre(genre: str, config: RunnableConfig):
    """
    Fetch songs from the database that match a specific genre.

    This function first looks up the genre ID(s) for the given genre name,
    then retrieves songs that belong to those genre(s), limiting results
    to 8 songs grouped by artist.

    Args:
        genre (str): The genre of the songs to fetch.
        config (RunnableConfig): The configuration for the runnable.
    Returns:
        list[dict] or str: A list of songs with artist information that match
                        the specified genre, or an error message if no songs found.
    """
    # First, get the genre ID(s) for the specified genre
    genre_id_query = f"SELECT GenreId FROM Genre WHERE Name LIKE '%{genre}%'"
    genre_ids = config["db"].run(genre_id_query)

    # Check if any genres were found
    if not genre_ids:
        return f"No songs found for the genre: {genre}"

    # Parse the genre IDs and format them for the SQL query
    genre_ids = ast.literal_eval(genre_ids)
    genre_id_list = ", ".join(str(gid[0]) for gid in genre_ids)

    # Query for songs in the specified genre(s)
    songs_query = f"""
        SELECT Track.Name as SongName, Artist.Name as ArtistName
        FROM Track
        LEFT JOIN Album ON Track.AlbumId = Album.AlbumId
        LEFT JOIN Artist ON Album.ArtistId = Artist.ArtistId
        WHERE Track.GenreId IN ({genre_id_list})
        GROUP BY Artist.Name
        LIMIT 8;
    """
    songs = config["db"].run(songs_query, include_columns=True)

    # Check if any songs were found
    if not songs:
        return f"No songs found for the genre: {genre}"

    # Format the results into a structured list of dictionaries
    formatted_songs = ast.literal_eval(songs)
    return [
        {"Song": song["SongName"], "Artist": song["ArtistName"]}
        for song in formatted_songs
    ]


@tool
def check_for_songs(song_title, config: RunnableConfig):
    """
    Check if a song exists in the database by its name.

    Args:
        song_title (str): The title of the song to search for.
        config (RunnableConfig): The configuration for the runnable.
    Returns:
        str: Database query results containing all track information
            for songs matching the given title.
    """
    return config["db"].run(
        f"""
        SELECT * FROM Track WHERE Name LIKE '%{song_title}%';
        """,
        include_columns=True,
    )


def get_music_tools():
    """Get all music-related database tools."""
    return [
        get_albums_by_artist,
        get_tracks_by_artist,
        get_songs_by_genre,
        check_for_songs,
    ]
