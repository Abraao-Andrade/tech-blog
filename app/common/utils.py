import jwt
from ipware import get_client_ip
from django.http import HttpRequest
from django.conf import settings
from typing import Union


def get_ip_and_agent(request: HttpRequest) -> dict:
    try:
        agent = request.META.get("HTTP_USER_AGENT") or ""
        client_ip, _ = get_client_ip(request)
        return {"ip": client_ip, "agent": agent}
    except AttributeError:
        return {}


def normalize_email(email: str) -> str:
    """
    Normalize the email address by lowercasing the domain part of it.
    """
    email = email or ""
    try:
        email_name, domain_part = email.strip().rsplit("@", 1)
    except ValueError:
        pass
    else:
        email = email_name + "@" + domain_part
    return email.lower()


def phone(ddd: str, phone: str) -> Union[str, None]:
    if ddd and phone:
        return f"{ddd}{phone}"
    return None


def jwt_encode(data: dict) -> str:
    return jwt.encode(
        data, settings.SECRET_KEY, algorithm=settings.SIMPLE_JWT.get("ALGORITHM")
    )


def jwt_decode(token: str) -> dict:
    return jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.SIMPLE_JWT.get("ALGORITHM")]
    )
