-- write a SQL query that lists the names of any songs that have danceability, energy, and valence greater than 0.75

SELECT name FROM songs WHERE danceability > .75 AND energy > .75 AND valence > .75;