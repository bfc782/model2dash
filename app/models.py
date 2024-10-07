import datetime
from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

from app import db


class User(db.Model):
    __tablename__ = "users"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, user_name={self.user_name!r})"


class Team(db.Model):
    __tablename__ = "teams"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    team_name: Mapped[str] = mapped_column(String(30))
    max_size: Mapped[int]
    min_size: Mapped[int]
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_date: Mapped[datetime.date]

    def __repr__(self) -> str:
        return f"Team(id={self.id!r}, team_name={self.team_name!r}, creator_id={self.creator_id!r})"


class Roster(db.Model): # userteamlink
    __tablename__ = "rosters"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user_status: Mapped[str] = mapped_column(String(30)) # Invited, Confirmed, Rejected, Left, Inactive
    user_role: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Roster(team_id={self.team_id!r}, user_id={self.user_id!r})"


class Target(db.Model):
    __tablename__ = "targets"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    training_id: Mapped[int] = mapped_column(ForeignKey("trainings.id"))
    target_event_result: Mapped[int] # in minutes
    target_block_training_count: Mapped[int] # in training sessions
    target_block_training_metric: Mapped[str] # Distance, Time, Repetitions, Ascent
    target_block_training_measure: Mapped[int] # in minutes, km, reps, m

    def __repr__(self) -> str:
        return f"Target(user_id={self.user_id!r}, event_id={self.event_id!r}, training_id={self.training_id!r})"


class Event(db.Model):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    date: Mapped[datetime.date]
    url: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(String(150))


class Training(db.Model):
    __tablename__ = "trainings"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(30))
    activity: Mapped[str] = mapped_column(String(30))
    type: Mapped[str] = mapped_column(String(30))
    phase: Mapped[int]
    intensity: Mapped[str] = mapped_column(String(30)) # Low, Medium, High
    metric: Mapped[str] = mapped_column(String(30)) # Distance, Time, Repetitions, Ascent
    target: Mapped[int]

    def __repr__(self) -> str:
        return f"Training(id={self.id!r}, name={self.activity!r}"


class Challenge(db.Model):
    __tablename__ = "challenges"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    training_id: Mapped[int] = mapped_column(ForeignKey("trainings.id"))
    start_date: Mapped[datetime.date]
    block_duration: Mapped[int] # in weeks
    wager: Mapped[int] # in CCY
    currency: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Challenge(id={self.id!r}, challenge_name={self.name!r}, challenge_creator={self.challenge_creator!r})"
    
    
class TrainingSession(db.Model):
    __tablename__ = "training_sessions"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    challenge_id: Mapped[int] = mapped_column(ForeignKey("challenges.id"))
    training_id: Mapped[int] = mapped_column(ForeignKey("trainings.id"))
    block_id: Mapped[int] = mapped_column(ForeignKey("blocks.id"))
    completion_date: Mapped[datetime.date]
    upload_timestamp: Mapped[datetime.date] # within 2 days of completion and before block end date
    url: Mapped[str] = mapped_column(String(150))

    def __repr__(self) -> str:
        return f"TrainingSession(user_id={self.user_id!r}, training_id={self.training_id!r})"


class Block(db.Model): # TODO: make this a view
    __tablename__ = "blocks"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30)) # weekly, fortnightly, monthly
    challenge_id: Mapped[int] = mapped_column(ForeignKey("challenges.id"))
    block_number: Mapped[int]
    block_start_date: Mapped[datetime.date]
    block_end_date: Mapped[datetime.date]

    def __repr__(self) -> str:
        return f"Block(id={self.id!r}, name={self.name!r}"


class ProgressScore(db.Model): # TODO: make this a view
    __tablename__ = "progress_scores"
     
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    challenge_id: Mapped[int] = mapped_column(ForeignKey("challenges.id"))
    block_id: Mapped[int] = mapped_column(ForeignKey("blocks.id"))
    user_block_training_count: Mapped[int] # in training sessions
    team_block_training_count: Mapped[int] # in training sessions
    user_total_training_count: Mapped[int] # in training sessions
    team_total_training_count: Mapped[int] # in training sessions

    def __repr__(self) -> str:
        return f"ProgressScore(user_id={self.user_id!r}, challenge_id={self.challenge_id!r})"


### End of rest of models
