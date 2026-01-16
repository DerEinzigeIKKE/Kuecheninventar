from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import os

# Definition der Basisklasse für SQLAlchemy-Modelle
Base = declarative_base()

class User(Base):
    """
    Repräsentiert einen Benutzer im System.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    
    # Beziehung zu den gespeicherten Rezepten
    recipes = relationship("Recipe", back_populates="user")

class Recipe(Base):
    """
    Repräsentiert ein gespeichertes Rezept.
    """
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    ingredients = Column(Text, nullable=True) # Gespeichert als JSON-String oder kommagetrennte Liste
    calories = Column(Integer, nullable=True)
    cuisine_type = Column(String, nullable=True)

    # Beziehung zum Benutzer
    user = relationship("User", back_populates="recipes")

# Datenbank-Initialisierung
DATABASE_URL = "sqlite:///recipes.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Erstellt die Datenbanktabellen, falls sie noch nicht existieren.
    """
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Erstellt eine neue Datenbanksitzung.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
