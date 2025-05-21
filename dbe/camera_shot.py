import uuid
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from database import Base
from dbe.image import Image


class CameraShot(Base):
    __tablename__ = "camera_shot"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    name: Mapped[str]
    device_id: Mapped[Optional[int]]
    shot_frequency_sec: Mapped[Optional[int]]
    insert_timestamp: Mapped[bool] = mapped_column(default=False)
    # images: Mapped[List[Image]] = relationship(passive_deletes=True)


def get_all(session: Session):
    return session.query(CameraShot).all()

def find_by_id(session: Session, camera_shot_id: UUID):
    return session.query(CameraShot).filter_by(id=camera_shot_id).first()