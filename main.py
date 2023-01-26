import click

import datetime

@click.group()
def main():
    pass

@main.command()
@click.option('-t','--target-date',default=None)
@click.option('-p','--data-path',type=str)
@click.option('-m','--tm', default='3')
@click.option('-d','--debug', default=False, is_flag=True)
def alc(
    target_date:str,
    data_path:str,
    tm:str,
    debug:bool
) -> None:
    """
    main app cli
    """
    from koscom.ftp import extract_data

    if target_date is None:
        target_date = datetime.datetime.now().strftime('%Y%m%d')
    
    result = extract_data(
        exe_tm=tm,
        target_date=target_date,
        data_path=data_path,
        bat_cd='KOSCOMFTPBATCHMANUAL',
        debug=debug
    )


@main.command()
def hello():
    click.echo("hello")


if __name__ =="__main__":
    main()