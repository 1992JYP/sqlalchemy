import os

import logging

from pydantic import BaseSettings

from typing import Dict, List


SRC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
LOG_DIR = os.path.join(SRC_DIR, 'sqlalchemy')


class Settings(BaseSettings):
    
    APP_NAME: str = 'EGIO'
    
    # Logging
    LOGGING_LOGGER_NAME: str = 'EGIOLOGGER'
    LOGGING_PATH: str = LOG_DIR
    LOGGING_LEVEL: str = 'DEBUG'
    LOGGING_FORMAT: str = '[$RED$BOLD%(levelname)s$RESET %(asctime)s %(processName)s %(filename)s > %(funcName)s:%(lineno)d] %(message)s'

    # rotate logger 환경설정
    RT_LOGGING_FILE_NAME: str = "data.log"
    RT_LOGGING_SUFFIX: str = "%Y%m%d"
    # RT_LOGGING_FORMAT: str = "%(levelname)s||%(asctime)s||%(message)s"
    RT_LOGGING_FORMAT: str = "{levelname:<8s}||{asctime}||{message}"
    RT_LOGGING_DTF: str = "%Y-%m-%d %H:%M:%S"
    RT_LOGGING_WHEN: str = "midnight"

    def get_logger_name(self, additional_token: List[str] = []) -> str:
        general = f'{self.LOGGING_LOGGER_NAME}'
        additional = '.'.join(additional_token)

        if additional == '':
            return general
        else:
            return f'{general}.{additional}'

    def get_rt_log_file_name(self, additional_token: List[str] = []) -> str:        
        general = f'{self.APP_NAME}.{self.RT_LOGGING_FILE_NAME}'
        additional = '.'.join(additional_token)

        if additional != '':
            general = f'{additional}.{general}'
            
        return os.path.join(self.LOGGING_PATH, general)

    def get_logging_level(self) -> int:
        """Setting에 설정된 LOGGING_LEVEL 문자열을 바탕으로 정수 값 반환

        Returns:
            int: LOGGING_LEVEL
        """
        return logging.getLevelName(self.LOGGING_LEVEL)



    DB_URI_TYPE : str = 'MSSQL'
    DB_URI_TEMPLATE: Dict[str, str] = {
        # 'MSSQL' : 'mssql+pymssql://{}:{}@{}:{}/{}?charset=cp949'
        'MSSQL' : 'mssql+pymssql://{}:{}@{}/{}?charset=cp949',
        'maria' : 'mariadb+mariadbconnector://{}:{}@{}/{}'
    }

    DB_CONNECTION_INFO: Dict[str, Dict[str, str]] = {
        'MSSQL':{
            'user':'sa',
            'pwd':'^449qkrwndbsA',
            'host':'IT-JYPARK',
            'database':'WideWorldImporters'
        },
        'maria':{
            'user':'jyp',
            'pwd':'jyp',
            'host':'localhost:3306',
            'database':'test'
        }
    }

    DB_POOL_SIZE : int = 0
    DB_MAX_OVERFLOW: int = -1

    def get_db_uri(
        self,
        uri_type:str,
        user:str,
        pwd:str,
        host:str,
        database:str
    ) -> str:
        return self.DB_URI_TEMPLATE[uri_type].format(
            user,
            pwd,
            host,
            database
        )

settings = Settings()