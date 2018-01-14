DROP DATABASE pgadapter_db;
CREATE DATABASE pgadapter_db
WITH
    OWNER = kenta
    ENCODIGNG = 'utf8'
    LC_COLLATE = 'ja_JP.UTF-8'
    LC_CTYPE = 'ja_JP.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

DROP TABLE IF EXISTS persons;
CREATE TABLE persons (name text NOT NULL, age integer NOT NULL);

DROP FUNCTION IF EXISTS save_person(text, integer);
CREATE OR REPLACE FUNCTION save_person(p_name text, p_age integer)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    INSERT INTO persons (name, age) VALUES (p_name, p_age);
END $$;

DROP FUNCTION IF EXISTS find_persons(text);
CREATE OR REPLACE FUNCTION find_persons(p_name text)
RETURNS TABLE(name text, age integer)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.name,
        p.age
    FROM persons AS p
    where p.name = p_name;
END $$;

DROP FUNCTION IF EXISTS delete_person(text);
CREATE OR REPLACE FUNCTION delete_person(p_name text)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    DELETE FROM persons WHERE name = p_name;
END $$;
