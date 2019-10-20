CREATE TABLE person_gender AS
SELECT a.inventor_id, a.name_first, a.name_last, b.male
FROM rawinventor as a
	INNER JOIN inventor_gender as b
	on a.inventor_id = b.disamb_inventor_id_20170808