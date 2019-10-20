CREATE TABLE patents_per_assignee AS
SELECT s.assignee_id, c.cnt
FROM raw_assignee s
INNER JOIN (
	SELECT assignee_id, count(*) as cnt
	from raw_assignee
	group by assignee_id
) c on s.assignee_id = c.assignee_id
order by field1