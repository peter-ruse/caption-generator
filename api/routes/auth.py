from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from core.auth import create_access_token
from services.auth.google_auth_service import google_auth_service

auth_router = APIRouter(tags=["auth"])


@auth_router.get("/login/google")
async def login_google(request: Request):
    redirect_uri = request.url_for("auth_callback")
    url = await google_auth_service.generate_login_url(str(redirect_uri))
    return RedirectResponse(url)


@auth_router.get("/auth/callback")
async def auth_callback(request: Request, code: str):
    redirect_uri = request.url_for("auth_callback")
    email = await google_auth_service.get_email_from_code(code, str(redirect_uri))

    if not email:
        return RedirectResponse("/login?error=denied")

    access_token = create_access_token({"sub": email})
    response = RedirectResponse("/", status_code=303)

    # httponly=True: prevents javascript from reading the cookie
    # secure=True: ensures the cookie is only sent over https
    # samesite="lax": prevents CSRF (Cross-Site Request Forgery);
    #   "strict" isn't an option because (given that we're using
    #   Google authentication) it would put us in a loop.
    response.set_cookie(
        "access_token", access_token, httponly=True, secure=True, samesite="lax"
    )
    return response
