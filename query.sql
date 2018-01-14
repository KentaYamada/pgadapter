

DROP TABLE IF EXISTS persons;

CREATE TABLE persons (name text NOT NULL, age integer NOT NULL);

DROP FUNCTION IF EXISTS save_person(text, integer);

CREATE OR REPLACE FUNCTION save_person(p_name text, p_age integer)
