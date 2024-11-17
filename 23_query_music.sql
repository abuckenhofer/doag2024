SELECT 
    artistName, 
    songName, 
    songVector <=> (SELECT songVector 
                    FROM music 
                    WHERE id = 5) AS similarity
FROM music
ORDER BY similarity
FETCH FIRST 5 ROWS ONLY;