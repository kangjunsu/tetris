from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import User, GameRecord
from ..schemas import UserWithStats, UserStats
from ..dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserWithStats)
def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user information with statistics"""
    # Calculate user statistics
    games = db.query(GameRecord).filter(GameRecord.user_id == current_user.id).all()

    if games:
        total_games = len(games)
        highest_score = max(game.score for game in games)
        total_lines_cleared = sum(game.lines_cleared for game in games)
        average_score = sum(game.score for game in games) / total_games
        best_level = max(game.level_reached for game in games)
    else:
        total_games = 0
        highest_score = 0
        total_lines_cleared = 0
        average_score = 0.0
        best_level = 0

    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "created_at": current_user.created_at,
        "is_active": current_user.is_active,
        "stats": {
            "total_games": total_games,
            "highest_score": highest_score,
            "total_lines_cleared": total_lines_cleared,
            "average_score": round(average_score, 2),
            "best_level": best_level
        }
    }


@router.get("/me/stats", response_model=UserStats)
def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed user statistics"""
    games = db.query(GameRecord).filter(GameRecord.user_id == current_user.id).all()

    if games:
        total_games = len(games)
        highest_score = max(game.score for game in games)
        total_lines_cleared = sum(game.lines_cleared for game in games)
        average_score = sum(game.score for game in games) / total_games
        best_level = max(game.level_reached for game in games)
    else:
        total_games = 0
        highest_score = 0
        total_lines_cleared = 0
        average_score = 0.0
        best_level = 0

    return {
        "total_games": total_games,
        "highest_score": highest_score,
        "total_lines_cleared": total_lines_cleared,
        "average_score": round(average_score, 2),
        "best_level": best_level
    }
