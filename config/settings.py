from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str

    API_VERSION: str

    HOST: str

    PORT: int

    ##################################

    MONGO_URI: str

    DB_NAME: str

    ##################################

    OPENAI_API_KEY: str

    MODEL: str

    ##################################

    GOOGLE_ADS_DEVELOPER_TOKEN: str

    GOOGLE_ADS_CLIENT_ID: str

    GOOGLE_ADS_CLIENT_SECRET: str

    GOOGLE_ADS_REFRESH_TOKEN: str

    GOOGLE_ADS_CUSTOMER_ID: str

    GOOGLE_ADS_LOGIN_CUSTOMER_ID: str

    ##################################

    MONITOR_INTERVAL: int

    MAX_BUDGET_SHIFT_PERCENT: int

    MAX_BID_CHANGE_PERCENT: int

    CPA_THRESHOLD: float

    CTR_THRESHOLD: float

    ROAS_THRESHOLD: float

    class Config:

        env_file=".env"


settings=Settings()