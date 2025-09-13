import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets


security = HTTPBasic()


PANEL_BASIC_USER = os.getenv("PANEL_BASIC_USER", "teacher")
PANEL_BASIC_PASS = os.getenv("PANEL_BASIC_PASS", "1234")


def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, PANEL_BASIC_USER)
    correct_password = secrets.compare_digest(credentials.password, PANEL_BASIC_PASS)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True