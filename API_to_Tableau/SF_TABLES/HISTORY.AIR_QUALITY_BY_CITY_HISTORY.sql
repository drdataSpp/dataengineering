USE ROLE SYSADMIN;
USE SCHEMA AIR_QUALITY.HISTORY;


CREATE TABLE IF NOT EXISTS AIR_QUALITY_BY_CITY_HISTORY (

    COUNTRY_NAME STRING,
    CITY_NAME STRING,
    RAW_AIR_QUALITY VARIANT,
    ROW_START_DATE DATE,
    ROW_END_DATE DATE,
    IS_ACTIVE BOOLEAN

);