from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class AnalysisModel(Base):

    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    home_team: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    away_team: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    home_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    draw_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    away_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    best_score: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    best_score_probability: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    poisson_home: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    poisson_draw: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    poisson_away: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    elo_home: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    elo_away: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    monte_carlo_home: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    monte_carlo_draw: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    monte_carlo_away: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    risk_level: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )