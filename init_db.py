from dbe import *
from dbe.camera_shot import CameraShot
from database import Base, engine

if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
