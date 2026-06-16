from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from ..database import get_db
from ..models import User, GameRecord
from ..schemas import GameSubmit, GameResponse, LeaderboardResponse, LeaderboardEntry, GameHistoryResponse
from ..dependencies import get_current_user

router = APIRouter(prefix="/games", tags=["games"])


@router.post("/submit", response_model=GameResponse, status_code=201)
def submit_game(
    game_data: GameSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit a game record"""
    new_game = GameRecord(
        user_id=current_user.id,
        score=game_data.score,
        lines_cleared=game_data.lines_cleared,
        level_reached=game_data.level_reached,
        duration_seconds=game_data.duration_seconds,
        device_type=game_data.device_type
    )

    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    # Calculate global rank
    higher_scores = db.query(func.count(GameRecord.id)).filter(
        GameRecord.score > new_game.score
    ).scalar()
    global_rank = higher_scores + 1

    # Calculate personal rank
    user_higher_scores = db.query(func.count(GameRecord.id)).filter(
        GameRecord.user_id == current_user.id,
        GameRecord.score > new_game.score
    ).scalar()
    personal_rank = user_higher_scores + 1

    return {
        "id": new_game.id,
        "score": new_game.score,
        "lines_cleared": new_game.lines_cleared,
        "level_reached": new_game.level_reached,
        "duration_seconds": new_game.duration_seconds,
        "played_at": new_game.played_at,
        "rank": {
            "global": global_rank,
            "personal": personal_rank
        }
    }


@router.get("/leaderboard", response_model=LeaderboardResponse)
def get_leaderboard(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    """Get global leaderboard"""
    # Get top scores with user info
    top_games = db.query(
        GameRecord, User
    ).join(
        User, GameRecord.user_id == User.id
    ).order_by(
        desc(GameRecord.score),
        desc(GameRecord.played_at)
    ).limit(limit).offset(offset).all()

    # Get total count
    total_count = db.query(func.count(GameRecord.id)).scalar()

    # Format leaderboard
    leaderboard = []
    for idx, (game, user) in enumerate(top_games, start=offset + 1):
        leaderboard.append({
            "rank": idx,
            "username": user.username or user.email.split('@')[0],
            "score": game.score,
            "lines_cleared": game.lines_cleared,
            "level_reached": game.level_reached,
            "played_at": game.played_at
        })

    return {
        "leaderboard": leaderboard,
        "total_count": total_count,
        "current_user_rank": None
    }


@router.get("/my-history", response_model=GameHistoryResponse)
def get_my_history(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's game history"""
    games = db.query(GameRecord).filter(
        GameRecord.user_id == current_user.id
    ).order_by(
        desc(GameRecord.played_at)
    ).limit(limit).offset(offset).all()

    total_count = db.query(func.count(GameRecord.id)).filter(
        GameRecord.user_id == current_user.id
    ).scalar()

    games_list = [
        {
            "id": game.id,
            "score": game.score,
            "lines_cleared": game.lines_cleared,
            "level_reached": game.level_reached,
            "duration_seconds": game.duration_seconds,
            "played_at": game.played_at,
            "rank": None
        }
        for game in games
    ]

    return {
        "games": games_list,
        "total_count": total_count
    }
