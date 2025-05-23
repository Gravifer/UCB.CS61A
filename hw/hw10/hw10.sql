CREATE TABLE parents AS
  SELECT "ace" AS parent, "bella" AS child UNION
  SELECT "ace"          , "charlie"        UNION
  SELECT "daisy"        , "hank"           UNION
  SELECT "finn"         , "ace"            UNION
  SELECT "finn"         , "daisy"          UNION
  SELECT "finn"         , "ginger"         UNION
  SELECT "ellie"        , "finn";

CREATE TABLE dogs AS
  SELECT "ace" AS name, "long" AS fur, 26 AS height UNION
  SELECT "bella"      , "short"      , 52           UNION
  SELECT "charlie"    , "long"       , 47           UNION
  SELECT "daisy"      , "long"       , 46           UNION
  SELECT "ellie"      , "short"      , 35           UNION
  SELECT "finn"       , "curly"      , 32           UNION
  SELECT "ginger"     , "short"      , 28           UNION
  SELECT "hank"       , "curly"      , 31;

CREATE TABLE sizes AS
  SELECT "toy" AS size, 24 AS min, 28 AS max UNION
  SELECT "mini"       , 28       , 35        UNION
  SELECT "medium"     , 35       , 45        UNION
  SELECT "standard"   , 45       , 60;


-- All dogs with parents ordered by decreasing height of their parent
CREATE TABLE by_parent_height AS
  -- SELECT child as name FROM parents JOIN dogs ON parent = name ORDER BY height DESC;
  SELECT parents.child AS name
    FROM ( parents JOIN dogs ON parents.parent = dogs.name )
    ORDER BY dogs.height DESC;
  -- SELECT name FROM (
  --   SELECT child AS name,
  --     height AS parent_height
  --   FROM (
  --       SELECT *
  --       FROM parents
  --         JOIN dogs ON parents.parent = dogs.name
  --     )
  --   ORDER BY parent_height DESC
  -- );


-- The size of each dog
CREATE TABLE size_of_dogs AS
  SELECT DISTINCT name, size
  FROM ( dogs JOIN sizes ON (
        dogs.height <= sizes.max
        AND dogs.height > sizes.min
      )
    );


-- [Optional] Filling out this helper table is recommended
CREATE TABLE siblings AS
  SELECT A.name AS name1, B.name AS name2 
  FROM size_of_dogs AS A 
  JOIN size_of_dogs AS B 
  JOIN parents AS P1 ON A.name = P1.child
  JOIN parents AS P2 ON B.name = P2.child
  WHERE name1 != name2 AND A.size = B.size AND P1.parent = P2.parent AND name1 < name2;

-- Sentences about siblings that are the same size
CREATE TABLE sentences AS
  SELECT "The two siblings, " || name1 || " and " || name2 || ", have the same size: " || size_of_dogs.size AS sentence
  FROM siblings
    JOIN size_of_dogs ON name1 = size_of_dogs.name;


-- Height range for each fur type where all of the heights differ by no more than 30% from the average height
CREATE TABLE low_variance AS
  SELECT fur, MAX(height) - MIN(height) AS height_range
  FROM dogs
  WHERE fur IN (
    SELECT fur
    FROM dogs
    GROUP BY fur
    HAVING MIN(height) >= (SELECT AVG(height) * 0.7 FROM dogs GROUP BY fur) 
      AND MAX(height) <= (SELECT AVG(height) * 1.3 FROM dogs GROUP BY fur)
  )
  GROUP BY fur;

