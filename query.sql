CREATE TABLE persons (
    name text NOT NULL,
    age integer NOT NULL
);

CREATE TYPE person_t AS (
    name text,
    age integer
);

CREATE OR REPLACE FUNCTION save_person(p_name text, p_age integer)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO persons (
        name,
        age
    ) VALUES (
        p_name,
        p_age
    );
END $$;

CREATE OR REPLACE FUNCTION save_persons(p_persons person_t[])
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO persons (
        name,
        age
    )
    SELECT
        p.name,
        p.age
    FROM unnest(p_persons) AS p;
END $$;

CREATE OR REPLACE FUNCTION find_persons()
RETURNS TABLE(name text, age integer)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.name,
        p.age
    FROM persons AS p;
END $$;

CREATE OR REPLACE FUNCTION find_persons_by(p_name text)
RETURNS TABLE(name text, age integer)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.name,
        p.age
    FROM persons AS p
    WHERE p.name like '%' || p_name || '%';
END $$;

CREATE OR REPLACE FUNCTION delete_person(p_name text)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM persons where name = p_name;
END $$;
