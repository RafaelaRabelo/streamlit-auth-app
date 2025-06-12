import os
import asyncio
from httpx_oauth.clients.google import GoogleOAuth2

client = GoogleOAuth2(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
)

async def get_authorization_url(redirect_uri):
    return await client.get_authorization_url(
        redirect_uri,
        scope=["openid", "email", "profile"]
    )

async def get_access_token(code, redirect_uri):
    return await client.get_access_token(code, redirect_uri)

async def get_user_info(token):
    return await client.get_id_email(token["access_token"])
