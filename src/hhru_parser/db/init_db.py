from hhru_parser.db import Base, engine
from hhru_parser.db import models

def init_db():
    Base.metadata.create_all(bind=engine)