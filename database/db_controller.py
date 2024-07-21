import sqlalchemy as db
from sqlalchemy import Column, Integer, String, BigInteger, select, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


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
        date = Column(Integer, nullable=False)

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

    def toggle_history(self, user_id, film_id, date):
        with self.session.begin() as session:
            query = select(self.History.__table__).where(self.History.user_id == user_id, self.History.film_id == film_id, self.History.date == date)
            favs = session.execute(query).mappings().fetchall()
            if favs:
                session.execute(delete(self.History.__table__).where(self.History.user_id == user_id, self.History.film_id == film_id, self.History.date == date))
            else:
                new_fav = self.History(user_id=user_id, film_id=film_id, date=date)
                session.add(new_fav)
            session.commit()

    # def get_all_favs(self):
    #     with self.session.begin() as session:
    #         return session.execute(select(self.Favorite.__table__)).mappings().fetchall()

    def get_all_favs(self, cls):
        with self.session.begin() as session:
            return session.execute(select(cls.__table__)).mappings().fetchall()