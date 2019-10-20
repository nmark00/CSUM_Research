CREATE TABLE person_award AS
SELECT a.nconst, b.primaryName, a.emmy
FROM AwardsOUTPUT as a
	INNER JOIN nconst_name as b
	on a.nconst = b.nconst