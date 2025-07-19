USE ROLE SYSADMIN;
USE SCHEMA Air_Quality.STAGING;

CREATE TABLE IF NOT EXISTS COUNTRY_CITIES (
    COUNTRY_NAME STRING,
    CITY_NAME STRING
);

-- insert values:

-- Scotland
INSERT INTO COUNTRY_CITIES VALUES
    ('Scotland', 'Edinburgh'),
    ('Scotland', 'Glasgow'),
    ('Scotland', 'Aberdeen'),
    ('Scotland', 'Dundee'),
    ('Scotland', 'Inverness');

-- United Kingdom (excluding Scotland)
INSERT INTO COUNTRY_CITIES VALUES
    ('United Kingdom', 'London'),
    ('United Kingdom', 'Manchester'),
    ('United Kingdom', 'Birmingham'),
    ('United Kingdom', 'Liverpool'),
    ('United Kingdom', 'Bristol');

-- United States
INSERT INTO COUNTRY_CITIES VALUES
    ('United States', 'New York City'),
    ('United States', 'Los Angeles'),
    ('United States', 'Chicago'),
    ('United States', 'Houston'),
    ('United States', 'San Francisco');

-- India
INSERT INTO COUNTRY_CITIES VALUES
    ('India', 'Mumbai'),
    ('India', 'Delhi'),
    ('India', 'Bangalore'),
    ('India', 'Chennai'),
    ('India', 'Hyderabad');

-- Australia
INSERT INTO COUNTRY_CITIES VALUES
    ('Australia', 'Sydney'),
    ('Australia', 'Melbourne'),
    ('Australia', 'Brisbane'),
    ('Australia', 'Perth'),
    ('Australia', 'Adelaide');

-- New Zealand
INSERT INTO COUNTRY_CITIES VALUES
    ('New Zealand', 'Auckland'),
    ('New Zealand', 'Wellington'),
    ('New Zealand', 'Christchurch'),
    ('New Zealand', 'Hamilton'),
    ('New Zealand', 'Dunedin');

-- Netherlands
INSERT INTO COUNTRY_CITIES VALUES
    ('Netherlands', 'Amsterdam'),
    ('Netherlands', 'Rotterdam'),
    ('Netherlands', 'The Hague'),
    ('Netherlands', 'Utrecht'),
    ('Netherlands', 'Eindhoven');
