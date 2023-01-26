from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base

engine = create_engine('mssql+pymssql://sa:^449qkrwndbsA@IT-JYPARK/WideWorldImporters')

from sqlalchemy import MetaData
metadata = MetaData()

from sqlalchemy import Table, Column, Integer, String

new_table = Table(
    "t3",
    metadata,
    Column("id",Integer,primary_key=True),
    Column("name",String(30),nullable=True),
)

new_table.c.keys()

metadata.create_all(engine)


from sqlalchemy.orm import registry