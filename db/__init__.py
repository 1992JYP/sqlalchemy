from db.session import (
    engine
    ,engine_maria
    , SessionLocal
    ,SessionLocalMaria
)
from db.base import get_base

Base = get_base(engine, 'MSSQL')
BaseMaria = get_base(engine_maria, 'maria')