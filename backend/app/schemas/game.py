from pydantic import BaseModel, field_validator
from datetime import datetime


class GameSubmit(BaseModel):
    score: int
    lines_cleared: int
    level_reached: int
    duration_seconds: int | None = None
    device_type: str | None = None

    @field_validator('score')
    @classmethod
    def validate_score(cls, v):
        if v < 0:
            raise ValueError('점수는 음수일 수 없습니다')
        if v > 999999999:
            raise ValueError('점수가 너무 큽니다')
        return v

    @field_validator('lines_cleared', 'level_reached')
    @classmethod
    def validate_positive(cls, v):
        if v < 0:
            raise ValueError('값은 음수일 수 없습니다')
        return v


class GameResponse(BaseModel):
    id: int
    score: int
    lines_cleared: int
    level_reached: int
    duration_seconds: int | None
    played_at: datetime
    rank: dict | None = None

    class Config:
        from_attributes = True


class LeaderboardEntry(BaseModel):
    rank: int
    username: str | None
    score: int
    lines_cleared: int
    level_reached: int
    played_at: datetime


class LeaderboardResponse(BaseModel):
    leaderboard: list[LeaderboardEntry]
    total_count: int
    current_user_rank: int | None = None


class GameHistoryResponse(BaseModel):
    games: list[GameResponse]
    total_count: int
