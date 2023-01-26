from typing import Callable, Tuple, List, Optional, Union
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings

MSSQL_TYPE = 'MSSQL'
MARIA_TYPE = 'maria'

engine = create_engine(
    settings.get_db_uri(
        MSSQL_TYPE,
        **settings.DB_CONNECTION_INFO[MSSQL_TYPE]
    ),
    # echo=True,
    pool_pre_ping=False,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

engine_maria = create_engine(
    settings.get_db_uri(
        MARIA_TYPE,
        **settings.DB_CONNECTION_INFO[MARIA_TYPE]
    ),
    pool_pre_ping=False,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW
)

SessionLocalMaria = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_maria
)

def make_session(db_type:str) -> Tuple[Engine,Callable]:
    
    engine = create_engine(
        settings.get_db_uri(db_type,**settings.DB_CONNECTION_INFO[db_type]),
        echo=False
    )

    session_factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    return engine, session_factory