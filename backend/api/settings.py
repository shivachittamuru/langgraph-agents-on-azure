
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

class AppSettings(BaseSettings):
    
    azure_openai_key: str = os.environ.get('AZURE_OPENAI_API_KEY')
    azure_openai_endpoint: str = os.environ.get('AZURE_OPENAI_ENDPOINT')
    azure_openai_api_version: str = os.environ.get('AZURE_OPENAI_API_VERSION')
    azure_openai_deployment_name: str = os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME')
    host: str = os.environ.get('PG_VECTOR_HOST')
    user: str = os.environ.get('PG_VECTOR_USER')
    password: str = os.environ.get('PG_VECTOR_PASSWORD')
    database: str = os.environ.get('PGDATABASE')
        
    
    # model_config = SettingsConfigDict(env_file=".env")

    class Config:
        env_file = ".env"
        extra = "ignore"
        
app_settings = AppSettings()