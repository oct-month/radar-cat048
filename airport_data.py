from typing import Generator, List
import re
from datetime import datetime

FILE_PATH = './AWOS202008010000.SJN'

class AutomaticObservationData:
    """民航自动观测数据"""
    def __init__(self) -> None:
        self.date_time : datetime = datetime.now()  # 时间组
        self.runway_num : str = '' # 跑道编号
        self.TDZ_num : str = '' # 着陆端编号
        self.MID_num : str = '' # 中间端标识
        self.END_num : str = '' # 停止端编号
    
    @staticmethod
    def fromSource(source: str) -> 'AutomaticObservationData':
        """解析数据，返回对象"""
        result = AutomaticObservationData()
        sourc_list = source.splitlines()
        date_value = [int(v) for v in sourc_list[0].split(':')]
        result.date_time = datetime(year=date_value[0], month=date_value[1], day=date_value[2], hour=date_value[3], minute=date_value[4])
        runway_value = sourc_list[1].split()
        result.runway_num = runway_value[0]
        result.TDZ_num = runway_value[1]
        result.MID_num = runway_value[2]
        result.END_num = runway_value[3]
        return result
    

class SingleEndedData:
    """单端的自观数据"""
    def __init__(self) -> None:
        pass


def read_data() -> str:
    """读取文件数据"""
    with open(FILE_PATH, 'r', encoding='UTF-8') as f:
        return f.read()

def analysis_data(source: str) -> Generator:
    """拆分文件数据为单个数据项"""
    pattern = r'ZCZC\n.*?\nNNNN'
    for value in re.findall(pattern, source, re.M | re.S):
        yield value[5:-5]


if __name__ == '__main__':
    source = read_data()
    data_list = analysis_data(source)
    for data in data_list:
        AutomaticObservationData.fromSource(data)

