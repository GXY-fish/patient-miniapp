from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


bearer_scheme = HTTPBearer(auto_error=False)


@dataclass
class CurrentUser:
    phone: str
    role: str


def _parse_demo_token(token: str) -> CurrentUser:
    if token.startswith("demo-access-token:"):
        parts = token.split(":", 2)
        if len(parts) == 3:
            _, phone, role = parts
            return CurrentUser(phone=phone, role=role)

    if token.startswith("demo-access-token-"):
        role = token.removeprefix("demo-access-token-")
        return CurrentUser(phone="unknown", role=role)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> CurrentUser:
    if not credentials:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return _parse_demo_token(credentials.credentials)


def require_role(*allowed_roles: str):
    def dependency(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if allowed_roles and current_user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return current_user

    return dependency