from pydantic import BaseSettings, SecretStr, PostgresDsn


class Settings(BaseSettings):
    bot_token: SecretStr
    chat_id: int
    db_url: PostgresDsn
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()