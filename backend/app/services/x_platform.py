import tweepy

from app.config import settings


def is_configured() -> bool:
    return bool(
        settings.x_api_key and settings.x_api_secret
        and settings.x_access_token and settings.x_access_secret
    )


def publish(text: str) -> dict:
    if not is_configured():
        raise RuntimeError("X is not configured (requires a paid X API developer plan).")

    client = tweepy.Client(
        consumer_key=settings.x_api_key,
        consumer_secret=settings.x_api_secret,
        access_token=settings.x_access_token,
        access_token_secret=settings.x_access_secret,
    )
    response = client.create_tweet(text=text)
    tweet_id = response.data["id"]
    return {"uri": tweet_id, "url": f"https://x.com/i/web/status/{tweet_id}"}
