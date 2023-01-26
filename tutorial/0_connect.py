# import sqlalchemy

# print (sqlalchemy.__version__)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base


# inline
engine = create_engine('mssql+pymssql://sa:^449qkrwndbsA@IT-JYPARK/WideWorldImporters')

# format, param receive
engine = create_engine('mssql+pymssql://{}:{}@{}/{}?charset=cp949'.format("sa","^449qkrwndbs","localhost:1433","WideWorldImporters"))

conn = engine.connect()
conn.close()


