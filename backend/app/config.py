from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./social_agent.db"
    llm_api_key: str = ""
    llm_model: str = "gpt-4o-mini"
    llm_base_url: str = ""
    cors_origins: list[str] = ["http://localhost:5173"]
    site_password: str = ""

    bluesky_handle: str = ""
    bluesky_app_password: str = ""

    mastodon_instance_url: str = ""
    mastodon_access_token: str = ""

    x_api_key: str = ""
    x_api_secret: str = ""
    x_access_token: str = ""
    x_access_secret: str = ""

    linkedin_access_token: str = ""
    linkedin_person_urn: str = ""

    meta_page_access_token: str = ""
    meta_page_id: str = ""
    meta_ig_user_id: str = ""


settings = Settings()
