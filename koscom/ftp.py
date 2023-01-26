"""
KOSCOM FTP 파일 처리를 위한 배치 테스크

Changes
-------
2022-01-19
    최초작성

2022-03-02
    FTP 파일 다운로드 기능 추가

"""
import os
import datetime 

import socket
import sys
import traceback

from email.mime import base
from logging import Logger
from typing import Any, List, Dict, Tuple

## FTP/SFTP 관련 패키지
# import paramiko

from core.config import settings, Settings
from sqlalchemy.orm import Session
from sqlalchemy import text

from kafka import KafkaProducer

# from batch.celery.app import celery_app
from container import inject

from db import Base, BaseMaria, SessionLocal, SessionLocalMaria, engine
from db.base import get_base

# from crud import mssql
# from crud.mssql import file_info, koscom, monitor
# from common import msg



@inject
def extract_data(
    log: Logger,
    settings: Settings,
    data_path: str,
    bat_cd: str = '',
    # base_producer: KafkaProducer,
    target_date: str = '',
    exe_tm: str = '3',
    debug: bool = False
) -> None:
    """FTP로 수신받은 파일에서 데이터를 추출하여 DB에 저장

    Parameters
    ----------
    log: Logger
        DI로 주입된 로거 객체
    settings: Setting
        프로젝트 환경 설정 객체
    data_path

    
    """

    # 대상 일자 설정
    if target_date == '':
        target_date = datetime.datetime.now().strftime('%Y%m%d')
    target_date_hypen = datetime.datetime.now().strftime('%Y-%m-%d')

    

    # 벌크 인서트 설정
    bulk_limit = 10000

    # 파일명 템플릿
    FILE_NAME_TEMPLATE = '{}.{}'

    data_model = Base.classes.t
    data_model_maria = BaseMaria.classes.t

    # file_schema = koscom.get_koscom_info(Base, session, exe_tm=exe_tm)
#    # file_schema = koscom.get_koscom_info(exe_tm=exe_tm)
#    # header_info = file_info.get_file_item_info(file_schema)

    # insert_qry = data_model.__table__.insert().execution_options(autocommit=False)

    session = SessionLocal()
    session.commit()

    sessionMaria = SessionLocalMaria()
    sessionMaria.commit()

    encoding = 'utf-8'
    try:
        with open('C:/Users/202212002/Documents/egioPythonStudy/sqlalchemy/koscom/test.csv', 'r', encoding=encoding) as input_stream:
            bulk_list = []
            for idx, line in enumerate(input_stream):
                encoded_line = line.encode(encoding)
                data =  {
                    'x': idx,
                }
                bulk_list.append(data)
                if idx > 0 and idx % bulk_limit == 0:
                    session.bulk_insert_mappings(
                        data_model, bulk_list)
                    session.commit()

                    # 운영DB

                    bulk_list.clear()
            
            if len(bulk_list) > 0:
                session.bulk_insert_mappings(
                    data_model, bulk_list)
                session.commit()
                
                # 운영DB
                
                bulk_list.clear()


    except Exception as exc:
        log.error(exc)
    finally:
        log.info(bat_cd)
        log.info('finish job')
        session.close()
    try:
        with open('C:/Users/202212002/Documents/egioPythonStudy/sqlalchemy/koscom/test.csv', 'r', encoding=encoding) as input_stream:
            bulk_list = []
            for idx, line in enumerate(input_stream):
                data =  {
                    'x': idx,
                }
                bulk_list.append(data)
                if idx > 0 and idx % bulk_limit == 0:
                    sessionMaria.bulk_insert_mappings(
                        data_model_maria, bulk_list)
                    sessionMaria.commit()

                    # 운영DB

                    bulk_list.clear()
            
            if len(bulk_list) > 0:
                sessionMaria.bulk_insert_mappings(
                    data_model_maria, bulk_list)
                sessionMaria.commit()
                
                # 운영DB
                
                bulk_list.clear()


    except Exception as exc:
        log.error(exc)
    finally:
        log.info(bat_cd)
        log.info('finish job')
        sessionMaria.close()

