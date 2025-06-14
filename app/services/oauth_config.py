from authlib.integrations.starlette_client import OAuth

oauth = OAuth()

# Google OAuth Configuration
oauth.register(
    name="google",
    client_id="YOUR_GOOGLE_CLIENT_ID",
    client_secret="YOUR_GOOGLE_CLIENT_SECRET",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    access_token_url="https://oauth2.googleapis.com/token",
    client_kwargs={"scope": "openid email profile"},
)

# Facebook OAuth Configuration
oauth.register(
    name="facebook",
    client_id="YOUR_FACEBOOK_CLIENT_ID",
    client_secret="YOUR_FACEBOOK_CLIENT_SECRET",
    authorize_url="https://www.facebook.com/dialog/oauth",
    access_token_url="https://graph.facebook.com/oauth/access_token",
    client_kwargs={"scope": "email public_profile"},
)

# Instagram OAuth Configuration
oauth.register(
    name="instagram",
    client_id="YOUR_INSTAGRAM_CLIENT_ID",
    client_secret="YOUR_INSTAGRAM_CLIENT_SECRET",
    authorize_url="https://api.instagram.com/oauth/authorize",
    access_token_url="https://api.instagram.com/oauth/access_token",
    client_kwargs={"scope": "user_profile"},
)
