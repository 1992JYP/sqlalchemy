from typing import Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, MetaData, Table
from sqlalchemy.engine import Engine
from sqlalchemy.ext.automap import AutomapBase
from sqlalchemy.orm import relationship
from sqlalchemy.ext.automap import automap_base

TARGET_TABLE_CONF = {
    'MSSQL': {
        'only': [
            't'
        ]
    },
    'maria':{
        'only':[
            't'
        ]
    }
}

def get_base(engine:Engine, target:str)-> Optional[AutomapBase]:
    Base = None
    public_schema_metadata = None

    if target == 'MSSQL':
        public_schema_metadata = MetaData(schema="dbo")

        public_schema_metadata.reflect(engine,
            **TARGET_TABLE_CONF[target]
        )

        Base = automap_base(metadata = public_schema_metadata)
        Base.prepare()


    
    elif target =='maria':
        # print("inmaria")
        public_schema_metadata = MetaData(schema="test")

        public_schema_metadata.reflect(engine,
            **TARGET_TABLE_CONF[target]
        )

        Base = automap_base(metadata=public_schema_metadata)
        Base.prepare()
    
    return Base