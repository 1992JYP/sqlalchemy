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


from core.config import Settings
from sqlalchemy.orm import Session
from sqlalchemy import text




from db import Base, SessionLocal, engine, BaseProd, SessionLocalProd


# from crud import mssql


@celery_app.task(serializer='json', ignore_result=False, acks_late=True)
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

    # 파일 정보 로드
    if debug:
        data_model = Base.classes.API_H_DATA_DEV
        data_model_prod = BaseProd.classes.API_H_DATA_DEV
    else:    
        data_model = Base.classes.API_H_DATA
        data_model_prod = BaseProd.classes.API_H_DATA
    # file_schema = koscom.get_koscom_info(Base, session, exe_tm=exe_tm)
    file_schema = koscom.get_koscom_info(exe_tm=exe_tm)
    header_info = file_info.get_file_item_info(file_schema)

    # insert_qry = data_model.__table__.insert().execution_options(autocommit=False)

    session = SessionLocal()
    session.commit()
    session_prod = SessionLocalProd()
    session_prod.commit()
    try:
        monitor.insert_log(None, None, target_date_hypen, bat_cd, 0, 'start')
        for file in file_schema:
            file_path = os.path.join(
                data_path, 
                FILE_NAME_TEMPLATE.format(file[1], target_date)
            )
            
            if os.path.exists(file_path):
                log.info(f'{file_path} exists')
                file_cd = file[0]
                encoding = file[2]
                length = header_info[file_cd]

                with open(file_path, 'r', encoding=encoding) as input_stream:
                    bulk_list = []
                    for idx, line in enumerate(input_stream):
                        encoded_line = line.encode(encoding)
                        header = encoded_line[:length].decode(encoding)
                        data =  {
                            'STD_DATE': target_date,
                            'FILE_CD': file_cd,
                            'DTL_CD': header,
                            'EVT_TM': exe_tm,
                            'INS_ID': 'egio',
                            'INS_IP': '0.0.0.0',
                            'FILE_DATA': encoded_line[:-1],
                            'INS_DTM': datetime.datetime.now()
                        }

                        bulk_list.append(data)
                        if idx > 0 and idx % bulk_limit == 0:
                            celery_app.control.heartbeat()
                            # engine.execute(
                            #     insert_qry,
                            #     bulk_list
                            # )
                            # engine.execute('COMMIT')
                            session.bulk_insert_mappings(
                                data_model, bulk_list)
                            session.commit()

                            # 운영DB
                            session_prod.bulk_insert_mappings(
                                data_model_prod, bulk_list)
                            session_prod.commit()
                            bulk_list.clear()
                    
                    if len(bulk_list) > 0:
                        celery_app.control.heartbeat()
                        # engine.execute(
                        #     insert_qry,
                        #     bulk_list
                        # )
                        # engine.execute('COMMIT')
                        session.bulk_insert_mappings(
                            data_model, bulk_list)
                        session.commit()
                        
                        # 운영DB
                        session_prod.bulk_insert_mappings(
                            data_model_prod, bulk_list)
                        session_prod.commit()

                        bulk_list.clear()

            else:
                log.info(f'{file_path} dosen\'t exists')
        

    except Exception as exc:
        log.error(exc)
        monitor.insert_log(None, None, target_date_hypen, bat_cd, 2, str(exc))
    finally:
        log.info(bat_cd)
        monitor.insert_log(None, None, target_date_hypen, bat_cd, 1, 'end')
        log.info('finish job')
        session.close()



