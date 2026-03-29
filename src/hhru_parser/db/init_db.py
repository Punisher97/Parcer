from hhru_parser.db import engine
from hhru_parser.db.models import Base
from hhru_parser.db import models

def init_db():
    Base.metadata.create_all(bind=engine)