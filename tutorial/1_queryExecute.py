# import sqlalchemy

# print (sqlalchemy.__version__)

from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData, Column, Integer, text
# from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('mssql+pymssql://sa:^449qkrwndbsA@IT-JYPARK/WideWorldImporters')
# engine.connect()

# m = MetaData()
# t = Table('t', m,
#         Column('id', Integer, primary_key=True),
#         Column('x', Integer))
# m.create_all(engine)
"""
CREATE TABLE T (
    id  INTEGER NOT NULL IDENTITY,
    x   INTEGER NULL,
    PRIMARY KEY (id)
)

디폴트가 AI가 들어있음 autoincrement=False로 처리 가능

"""
###
### query execute
with engine.connect() as conn:
    result = conn.execute(text("SELECT 'hello'"))
    print(result.all())

    
# with engine.connect() as conn:
#     # conn.execute(text("CREATE TABLE t2 (id int NOT NULL PRIMARY KEY, x int)"))
#     conn.execute(
#         text("insert into t2 Values(:id, :x)"),
#         [{"id":1,"x":2},{"id":2,"x":22}]
#     )

###
### query execute & transaction unit/autocommit

# "begin once"
# with engine.begin() as conn:
#     conn.execute(
#         text("insert into t2 values (:id, :x)"),
#         [{"id":17,"x":125}]
#     )


# with engine.connect() as conn:
#     result = conn.execute(text("SELECT x, id FROM t2"))
#     for row in result:
#         print(f"id: {row[1]}  x: {row.x}")


# with engine.connect() as conn:
#     result = conn.execute(text("SELECT x, id FROM t2"))
#     for row in result.mappings():
#         x=row["x"]
#         id=row["id"]
#         print(f"id: {id}  x: {x}")

with engine.connect() as conn:
    result = conn.execute(
        text("SELECT id, :kk FROM t2"),
        {"kk":'x'}
    )
    for row in result:
        print(row.x,row.id)