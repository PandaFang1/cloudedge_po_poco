import logging
import os
from datetime import datetime
from pathlib import Path

ROOT_MARKERS = ["config","utils","pages"]
def operate_log_filepath(makers=None):
    """
    根据markers中文件名来寻找项目根目录
    :param makers: list of str, if None, use ROOT_MARKERS
    """
    if makers is None:
        makers = ROOT_MARKERS
    current_dir = Path(__file__).resolve().parent #获取当前文件所在目录
    for dir in [current_dir,*current_dir.parents]: #根据目录层级遍历目录，current_dir.parents返回的是一个path的对象，*解包
        for marker in ROOT_MARKERS:#遍历ROOT_MARKERS中的文件名，如果都存在则返回当前目录确认为根目录
            if not (dir/marker).exists(): #dir/marker拼接目录，判断是否存在此目录
                break  #不存在直接中断进行下一个循环
            return dir #若均存在，则返回当前目录
    return current_dir #若均没有存在，则返回当前执行的文件目录

def file_size(file_path):
    size = Path(file_path).stat().st_size
    while size > 1024:




def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(filename)s|%(module)s  - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)
    current_date = datetime.now().strftime('%Y-%m-%d')
    fh = logging.FileHandler(f'operate/log_{current_date}.log')
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    return logger
