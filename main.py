from fastapi import FastAPI, HTTPException, Depends
from fastapi.openapi.models import APIKey
from fastapi.security import APIKeyHeader
from httpx import AsyncClient
import os

app = FastAPI()


# API_KEY_ENV_VAR = 'OPENWEATHER_API_KEY'
API_KEY = "77676f3acfcc26ad7823729dc54bec24"
api_key_header = APIKeyHeader(name='api_key',auto_error=False)
OPENWEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

# openweather_api_key = os.getenv(API_KEY_ENV_VAR)
# if not openweather_api_key:
#     raise Exception(f'Please set env variable {API_KEY_ENV_VAR}')



async def get_api_key(api_key_header: str = API_KEY) -> str:
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail='Invalid API KEY')
    

@app.get('/weather/{city}')
async def get_weather(city:str, api_key: APIKey = Depends(get_api_key)):
    params = {
        'q':city,
        'appid':API_KEY,
        'units':'metric'
    }

    async with AsyncClient() as client:
        response = await client.get(OPENWEATHER_API_URL, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        HTTPException(status_code=response.status_code, detail='Failed')

    
if __name__=='__main__':
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000)
