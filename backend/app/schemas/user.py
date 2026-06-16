from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str | None = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class UserWithStats(UserResponse):
    stats: dict


class UserStats(BaseModel):
    total_games: int
    highest_score: int
    total_lines_cleared: int
    average_score: float
    best_level: int
