from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker, registry  # type: ignore
from app.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

mapper_registry = registry()
Base = mapper_registry.generate_base()
