import sqlalchemy as db
from sqlalchemy import Column, Integer, BigInteger, DateTime, select, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils import singleton, format_time
import config_reader


@singleton
class DB_Controller:

    def __init__(self, db_name):
        self.engine = db.create_engine(f"sqlite:///{db_name}")
        self.session = sessionmaker(self.engine)

    Base = declarative_base()

    class Favorite(Base):
        __tablename__ = "favorite"

        id = Column(Integer, primary_key=True)
        user_id = Column(BigInteger, nullable=False)
        film_id = Column(BigInteger, nullable=False)

    class History(Base):
        __tablename__ = "history"

        id = Column(Integer, primary_key=True)
        user_id = Column(BigInteger, nullable=False)
        film_id = Column(BigInteger, nullable=False)
        date = Column(DateTime, nullable=False, default=format_time)

    def create_tables(self):
        self.Base.metadata.create_all(self.engine)

    def toggle_favorite(self, user_id, film_id):
        with self.session.begin() as session:
            query = select(self.Favorite.__table__).where(self.Favorite.user_id == user_id, self.Favorite.film_id == film_id)
            favs = session.execute(query).mappings().fetchall()
            if favs:
                session.execute(delete(self.Favorite.__table__).where(self.Favorite.user_id == user_id, self.Favorite.film_id == film_id))
            else:
                new_fav = self.Favorite(user_id=user_id, film_id=film_id)
                session.add(new_fav)
            session.commit()

    def add_history(self, user_id, film_id):
        with self.session.begin() as session:
            new_fav = self.History(user_id=user_id, film_id=film_id)
            session.add(new_fav)
            session.commit()

    def get_all_records(self, cls):
        with self.session.begin() as session:
            return session.execute(select(cls.__table__)).mappings().fetchall()

    def get_all_faves(self):
        return self.get_all_records(self.Favorite)

    def get_all_history(self):
        res = self.get_all_records(self.History)
        return res


db_controller = DB_Controller(db_name=config_reader.config.db_name)
db_controller.create_tables()
