from sqlalchemy import create_engine
from .models import metadata
DATABASE_URL = "mysql+pymysql://user:wodnr3569@db:3306/mushroom_db?charset=utf8mb4"
engine = create_engine(DATABASE_URL, echo=True)
metadata.create_all(engine)
