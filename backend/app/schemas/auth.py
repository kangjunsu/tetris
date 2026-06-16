from pydantic import BaseModel, EmailStr, field_validator
import re


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    username: str | None = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('비밀번호는 최소 8자 이상이어야 합니다')
        if not re.search(r'[A-Z]', v):
            raise ValueError('비밀번호는 최소 1개의 대문자를 포함해야 합니다')
        if not re.search(r'[a-z]', v):
            raise ValueError('비밀번호는 최소 1개의 소문자를 포함해야 합니다')
        if not re.search(r'\d', v):
            raise ValueError('비밀번호는 최소 1개의 숫자를 포함해야 합니다')
        return v

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if v is not None:
            if len(v) < 3 or len(v) > 100:
                raise ValueError('사용자 이름은 3-100자 사이여야 합니다')
            if not re.match(r'^[a-zA-Z0-9_]+$', v):
                raise ValueError('사용자 이름은 영문, 숫자, 밑줄만 사용 가능합니다')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: dict


class TokenData(BaseModel):
    email: str | None = None
