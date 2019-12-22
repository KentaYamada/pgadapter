DROP TABLE IF EXISTS car_makers;
DROP TABLE IF EXISTS cars;

CREATE TABLE car_makers (
    id serial NOT NULL,
    name text NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE cars (
    id serial NOT NULL,
    car_maker_id int NOT NULL,
    name text NOT NULL,
    PRIMARY KEY(id)
);
