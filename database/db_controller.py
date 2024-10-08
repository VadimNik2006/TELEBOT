import sqlalchemy as db
from sqlalchemy import Column, Integer, BigInteger, DateTime, delete, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils import singleton, format_time
from sqlalchemy.future import select
import config_reader
from datetime import datetime, timedelta


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

    def favorite_datas_view(self, user_id, film_id):
        with self.session.begin() as session:
            query = select(self.Favorite.__table__).where(self.Favorite.user_id == user_id,
                                                          self.Favorite.film_id == film_id)
            faves = session.execute(query).mappings().fetchall()
            if faves:
                return True
            return False

    def toggle_favorite(self, user_id, film_id, add=False):
        with self.session.begin() as session:
            query = select(self.Favorite.__table__).where(self.Favorite.user_id == user_id,
                                                          self.Favorite.film_id == film_id)
            faves = session.execute(query).mappings().fetchall()
            if faves and not add:
                session.execute(delete(self.Favorite.__table__).where(self.Favorite.user_id == user_id,
                                                                      self.Favorite.film_id == film_id))
            elif add and not faves:
                new_fav = self.Favorite(user_id=user_id, film_id=film_id)
                session.add(new_fav)
            session.commit()

    def add_history(self, user_id, film_id):
        with self.session.begin() as session:
            now = datetime.now()
            start_of_day = datetime(now.year, now.month, now.day)
            end_of_day = start_of_day + timedelta(days=1)
            query = select(self.History).where(self.History.user_id == user_id,
                                               self.History.film_id == film_id,
                                               self.History.date.between(start_of_day, end_of_day))
            hist = session.execute(query).all()
            if hist:
                stmt = hist[0][0]
                stmt.date = format_time()
            else:
                new_hist = self.History(user_id=user_id, film_id=film_id)
                session.add(new_hist)
            session.commit()

    def get_all_faves(self, user_id):
        with self.session.begin() as session:
            query = select(self.Favorite.__table__).where(self.Favorite.user_id == user_id)
            faves = session.execute(query).mappings().fetchall()
            return faves

    def get_all_history(self, user_id):
        with self.session.begin() as session:
            query = select(self.History.__table__).where(self.History.user_id == user_id)
            hist = session.execute(query).mappings().fetchall()
            return hist


db_controller = DB_Controller(db_name=config_reader.config.db_name)
db_controller.create_tables()
