from typing import List, Tuple
from datetime import datetime

FILE_PATH = './DATASAMPLE.txt'

def read_data(path: str) -> List[str]:
    """读取数据"""
    with open(path, 'r', encoding='UTF-8') as f:
        return [line for line in f]


class SecondaryRadar048:
    """二次雷达数据CAT048"""
    def __init__(self, source: str) -> None:
        soc = source.split()
        self.recv_time = self.__read_utc_time(soc[0])   # 接收到数据的时间
        self.__source = soc[1]
        self.__analysis()
    
    def __read_utc_time(self, utc: str) -> datetime:
        """解析时间"""
        day, month, year, hour, minute, second = 0, 0, 0, 0, 0, 0
        date_str, sec_str = utc.split(':')
        day = int(date_str[-2:])        # 日
        month = int(date_str[-4:-2])    # 月
        year = int(date_str[:-4])       # 年
        sec = float(sec_str)
        hour = int(sec % 3600)          # 时
        sec -= 3600 * hour
        minute = int(sec % 60)          # 分
        sec -= 60 * minute
        second = int(sec % 1)           # 秒
        sec -= 1 * second
        microsecond = int(sec * 1e6)
        return datetime(year=year, month=month, day=day, 
                    hour=hour, minute=minute, second=second, microsecond=microsecond)
    
    def __read_bits(self, bits: int) -> int:
        """从数据中读取bits个比特"""
        soc = self.__read_bits_str(bits)
        return int(soc, 16)
    
    def __read_bits_str(self, bits: int) -> str:
        """从数据中读取bits个比特"""
        soc = self.__source[:bits*2]
        self.__source = self.__source[bits*2:]
        return soc
    
    def __read_bits_FX(self, min: int=1, step: int=1) -> Tuple[int, int]:
        """
        依据FX位读取若干个比特
        至少读取min个
        一次步进step个比特
        @return 读取的数据, 实际读取的比特数
        """
        read_num = 0
        result_list = []
        result_list.append(self.__read_bits_str(min))
        read_num += min
        while (int(result_list[-1], 16) & 1) != 0:
            result_list.append(self.__read_bits_str(step))
            read_num += step
        soc = ''.join(result_list)
        return int(soc, 16), read_num
    
    def __analysis(self) -> None:
        self.HDLC_address = self.__read_bits(1) # HDLC地址字段
        self.HDLC_control = self.__read_bits(1) # HDLC控制字段
        self.CAT = self.__read_bits(1)          # CAT数据种类
        self.LEN = self.__read_bits(2)          # 数据帧的总长度
        self.FSPEC, _ = self.__read_bits_FX()   # UAP表的数据索引


if __name__ == '__main__':
    data = read_data(FILE_PATH)[0]
    a = SecondaryRadar048(data)
    print(len(bin(a.FSPEC)) - 2)
