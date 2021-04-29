from datetime import datetime, time
import math

from plane_data import Coordinate, RADAR_COOR

class Test:
    def __init__(self) -> None:
        self.polar_diameter = 156609.75
        self.polar_angle = 114.906005859375

    def calculate_coor(self) -> Coordinate:
        """计算经纬度"""
        c = self.polar_diameter / 6371000 * 180 / math.pi
        a = math.acos(math.cos(90 - RADAR_COOR.latitude) * math.cos(c) + math.sin(90 - RADAR_COOR.latitude) * math.sin(c) * math.cos(self.polar_angle))
        t = math.asin(math.sin(c) * math.sin(self.polar_angle) / math.sin(a))
        return Coordinate(RADAR_COOR.longitude + t, RADAR_COOR.latitude - a)


if __name__ == "__main__":
    print(datetime.now().time())
    print(Test().calculate_coor())
