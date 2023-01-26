from sqlalchemy import create_engine, text

from sqlalchemy.orm import Session

# inline
engine = create_engine('mssql+pymssql://sa:^449qkrwndbsA@IT-JYPARK/WideWorldImporters')

stmt = text("select id,x from t2 order by x desc")

with Session(engine) as session:
    result =  session.execute(stmt)
    for row in result:
        print(row.x,row.id)


with Session(engine) as session:
    result = session.execute(
        text("update t2 SET x=3 WHERE x=2")
    )
    session.commit()

