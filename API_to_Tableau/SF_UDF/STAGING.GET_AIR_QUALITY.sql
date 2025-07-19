USE ROLE SYSADMIN;
USE SCHEMA Air_Quality.STAGING;
CREATE OR REPLACE FUNCTION GET_AIR_QUALITY(CITY_NAME STRING)
  RETURNS VARIANT
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.11'
  HANDLER = 'fetch_air_quality_by_city'
  EXTERNAL_ACCESS_INTEGRATIONS = (Juhe_API_ext_access_integration)
  PACKAGES = ('requests')
  SECRETS = ('api_key' = AIR_QUALITY.STAGING.Air_Quality_API_Key )
AS 
$$

import _snowflake
import requests

def get_secret():
    secret_type = _snowflake.get_generic_secret_string('api_key')
    return secret_type

def fetch_air_quality_by_city(CITY_NAME):

    try:
        BASE_URL = 'https://hub.juheapi.com/aqi/v1/city'
        
        API_KEY = get_secret()

        """
        API DOCS:
        * apikey	string	Required	Your API KEY
        * q	        string	Required	Name of the city or station (e.g., beijing, london)
        """
        
        response = requests.get(BASE_URL, params={
            'apikey': API_KEY,
            'q': CITY_NAME
        })

        # Check if the response was successful
        if response.status_code != 200:
            raise Exception(f"API returned non-200 status code: {response.status_code} - {response.text}")

        # Check the api's custom code was successful
        if response.json().get('code') != "0":
            raise Exception(f"API error code: {response.json().get('code')} - {response.json().get('msg')}")
        
        return response.json()
        
    except Exception as e:
    
    # Build a custom error output similar to API return.
    
        return {
            "code": "999",
            "msg": f"Failed to fetch air quality data: {str(e)}",
            "data": {
                "city": None,
                "aqi": None,
                "co": None,
                "no2": None,
                "o3": None,
                "pm10": None,
                "pm25": None,
                "so2": None,
                "geo": None
            }
        }
$$
;

-- Test
SELECT GET_AIR_QUALITY('Chennai');