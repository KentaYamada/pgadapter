CREATE OR REPLACE FUNCTION save_car_maker(p_id integer, p_name text)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    IF p_id IS NULL THEN
        INSERT INTO car_makers (
            name
        ) VALUES (
            p_name
        );
    ELSE
        UPDATE car_makers SET
            name = p_name
        WHERE id = p_id;
    END IF;
END $$;


CREATE OR REPLACE FUNCTION find_car_makers()
RETURNS SETOF car_makers
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY
    SELECT
        id,
        name
    FROM car_makers;
END $$;

CREATE OR REPLACE FUNCTION find_car_maker_by_id(p_id integer)
RETURNS SETOF car_makers
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY
    SELECT
        id,
        name
    FROM car_makers
    WHERE id = p_id;
END $$;
