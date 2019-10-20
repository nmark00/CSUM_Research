SELECT DISTINCT a.nconst,  primaryName
FROM name AS a
	INNER JOIN person_showOutput AS b
	ON a.nconst = b.nconst