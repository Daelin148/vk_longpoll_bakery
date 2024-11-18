import os

from dotenv import load_dotenv
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


load_dotenv()

Base = declarative_base()

user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
db = os.getenv('DB_NAME')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')


engine = create_engine(
    f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'
)
Session = sessionmaker(bind=engine)


class Category(Base):
    """Модель категорий продуктов."""

    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    products = relationship('Product', backref='category')


class Product(Base):
    """Модель продуктов."""

    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))


Base.metadata.create_all(engine)
