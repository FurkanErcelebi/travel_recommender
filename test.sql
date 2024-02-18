SELECT tp1.* , tp2.place_id 
FROM ( 
	SELECT (point(18.46709, -34.10375) <@> point(tp.longitude,tp.latitude)) as distance , tp.* 
	FROM travel_search_tripplaces tp 
	ORDER BY distance 
	LIMIT 3
 ) tp1
INNER JOIN travel_search_tripplaces_place_type_id tp2 ON tp1.id = tp2.tripplaces_id
WHERE tp1.distance < 20; 