import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2
import asyncio
import jwt

# Sign in with google initialize
CLIENT_ID = st.secrets['CLIENT_ID']
CLIENT_SECRET = st.secrets['CLIENT_SECRET']
REDIRECT_URI = 'http://localhost:8501/'

client = GoogleOAuth2(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

async def get_authorization_url(client: GoogleOAuth2, redirect_uri: str):
    return await client.get_authorization_url(
        redirect_uri, scope=["profile", "email"], extras_params={"access_type": "offline"})

async def get_access_token(client: GoogleOAuth2, redirect_uri: str, code: str):
    return await client.get_access_token(code, redirect_uri)

async def get_email(client: GoogleOAuth2, token: str):
    user_id, user_email = await client.get_id_email(token)
    return user_id, user_email

def decode_user(token: str):
    return jwt.decode(jwt=token, options={"verify_signature": False})

def get_token_from_params(client: GoogleOAuth2, redirect_uri: str):
    code = st.query_params['code']
    token = asyncio.run(get_access_token(client=client, redirect_uri=redirect_uri, code=code))
    st.query_params.clear()
    return token

# Initialization global state email
class global_state:
    def __init__(self):
        self.email = ''

if 'global_state' not in st.session_state:
    st.session_state.global_state = global_state()

global_state = st.session_state.global_state