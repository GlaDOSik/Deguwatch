import uuid
from uuid import UUID

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, Session
from datetime import datetime

from database import Base


class Image(Base):
    __tablename__ = "image"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    camera_shot_id: Mapped[UUID] = mapped_column(ForeignKey("camera_shot.id"))
    timestamp: Mapped[datetime] = mapped_column(DateTime)


def find_by_id(session: Session, image_id: UUID):
    return session.query(Image).filter_by(id=image_id).first()

def find_newest(session: Session, camera_shot_id: str):
    return session.query(Image).filter(Image.camera_shot_id == camera_shot_id).order_by(Image.timestamp.desc()).first()

def find_next(session: Session, camera_shot_id: UUID, timestamp: datetime):
    return (
        session.query(Image)
        .filter(
            Image.camera_shot_id == camera_shot_id,
            Image.timestamp > timestamp
        )
        .order_by(Image.timestamp.asc())
        .first()
    )

def find_previous(session: Session, camera_shot_id: UUID, timestamp: datetime):
    return (
        session.query(Image)
        .filter(
            Image.camera_shot_id == camera_shot_id,
            Image.timestamp < timestamp
        )
        .order_by(Image.timestamp.desc())
        .first()
    )
