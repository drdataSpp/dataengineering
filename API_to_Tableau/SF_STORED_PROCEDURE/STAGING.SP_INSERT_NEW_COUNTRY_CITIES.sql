USE ROLE SYSADMIN;
USE SCHEMA AIR_QUALITY.STAGING;

CREATE OR REPLACE PROCEDURE SP_INSERT_NEW_COUNTRY_CITIES()
RETURNS STRING
LANGUAGE SQL
AS
DECLARE
  ROWS_INSERTED INTEGER;
  
BEGIN
    -- Insert only new city-country pairs into history
    INSERT INTO AIR_QUALITY.HISTORY.COUNTRY_CITIES (
      COUNTRY_NAME,
      CITY_NAME,
      INSERTED_AT_UTC
    )
    
    SELECT
      src.COUNTRY_NAME,
      src.CITY_NAME,
      CONVERT_TIMEZONE('UTC', CURRENT_TIMESTAMP())
    FROM AIR_QUALITY.STAGING.COUNTRY_CITIES src
    WHERE MD5(src.COUNTRY_NAME || src.CITY_NAME) NOT IN (
      SELECT MD5(tgt.COUNTRY_NAME || tgt.CITY_NAME)
      FROM AIR_QUALITY.HISTORY.COUNTRY_CITIES tgt
    );

    RETURN '✅ Insert completed. New records inserted: ' || SQLROWCOUNT;

    EXCEPTION
        WHEN OTHER THEN
        RETURN 'Error: ' || SQLERRM;

END;
;

-- VERIFY
CALL SP_INSERT_NEW_COUNTRY_CITIES();