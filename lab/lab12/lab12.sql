CREATE TABLE finals AS
  SELECT 'RSF' AS hall, '61A' AS course UNION
  SELECT 'Wheeler'    , '61A'           UNION
  SELECT 'Pimentel'   , '61A'           UNION
  SELECT 'Li Ka Shing', '61A'           UNION
  SELECT 'Stanley'    , '61A'           UNION
  SELECT 'RSF'        , '61B'           UNION
  SELECT 'Wheeler'    , '61B'           UNION
  SELECT 'Morgan'     , '61B'           UNION
  SELECT 'Wheeler'    , '61C'           UNION
  SELECT 'Pimentel'   , '61C'           UNION
  SELECT 'Soda 310'   , '61C'           UNION
  SELECT 'Soda 306'   , '10'            UNION
  SELECT 'RSF'        , '70';

CREATE TABLE sizes AS
  SELECT 'RSF' AS room, 900 AS seats    UNION
  SELECT 'Wheeler'    , 700             UNION
  SELECT 'Pimentel'   , 500             UNION
  SELECT 'Li Ka Shing', 300             UNION
  SELECT 'Stanley'    , 300             UNION
  SELECT 'Morgan'     , 100             UNION
  SELECT 'Soda 306'   , 80              UNION
  SELECT 'Soda 310'   , 40              UNION
  SELECT 'Soda 320'   , 30;

CREATE TABLE sharing AS
  SELECT a.course, COUNT(DISTINCT a.hall) AS shared
    FROM finals AS a, finals AS b
    WHERE a.hall = b.hall AND a.course != b.course GROUP BY a.course;

CREATE TABLE pairs AS
  SELECT a.room || " and " || b.room || " together have " || (a.seats + b.seats) || " seats" AS rooms
  FROM sizes AS a, sizes AS b
  ON a.seats + b.seats >= 1000 AND a.room < b.room
  ORDER BY (a.seats + b.seats) DESC;

CREATE TABLE big AS
  SELECT finals.course
  FROM finals, sizes
  WHERE finals.hall == sizes.room
  GROUP BY finals.course
  HAVING SUM(sizes.seats) >= 1000;

CREATE TABLE remaining AS
  SELECT finals.course AS course, SUM(sizes.seats) - MAX(sizes.seats) AS remaining 
  FROM finals, sizes
  WHERE finals.hall == sizes.room
  GROUP BY finals.course;

