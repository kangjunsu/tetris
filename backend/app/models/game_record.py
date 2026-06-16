from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class GameRecord(Base):
    __tablename__ = "game_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, nullable=False, index=True)
    lines_cleared = Column(Integer, nullable=False, default=0)
    level_reached = Column(Integer, nullable=False, default=1)
    duration_seconds = Column(Integer, nullable=True)
    played_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    device_type = Column(String(50), nullable=True)

    # Relationship
    user = relationship("User", back_populates="game_records")

    __table_args__ = (
        Index('idx_score_desc', score.desc()),
        Index('idx_user_score', 'user_id', score.desc()),
        Index('idx_played_at', 'played_at'),
    )
