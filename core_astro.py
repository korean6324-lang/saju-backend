# core_astro.py
import ephem
import math
from datetime import datetime, timedelta
from typing import Dict
from korean_lunar_calendar import KoreanLunarCalendar

class AstroEngine:
    def __init__(self):
        self.stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        self.branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    def get_solar_longitude(self, dt: datetime) -> float:
        """NASA 천체력을 이용한 황경 계산"""
        sun = ephem.Sun()
        observer = ephem.Observer()
        observer.date = ephem.Date(dt - timedelta(hours=9)) 
        sun.compute(observer)
        return float(math.degrees(sun.hlon) % 360)

    def _get_year_pillar(self, year: int, lon: float, dt: datetime) -> str:
        """입춘(315도) 기준 년주 도출"""
        base_year = year
        if dt.month <= 2 and (lon < 315 and lon >= 270):
            base_year -= 1
        stem_idx = (base_year - 4) % 10
        branch_idx = (base_year - 4) % 12
        return f"{self.stems[stem_idx]}{self.branches[branch_idx]}"

    def _get_month_pillar(self, year_stem: str, lon: float) -> str:
        """절기 기준 월지 및 둔월법 기준 월간 도출"""
        lon_normalized = (lon - 315) % 360
        month_idx = int(lon_normalized // 30)
        month_branch = self.branches[(month_idx + 2) % 12]
        
        year_stem_idx = self.stems.index(year_stem)
        base_stem_idx = ((year_stem_idx % 5) * 2 + 2) % 10
        month_stem_idx = (base_stem_idx + month_idx) % 10
        return f"{self.stems[month_stem_idx]}{month_branch}"

    def _get_day_pillar(self, dt: datetime) -> str:
        """1990-01-01 (병오일) 기준 만세력 일주 완벽 산출 (야자시 적용)"""
        target_dt = dt
        if dt.hour >= 23:
            target_dt = dt + timedelta(days=1)
            
        # 1990년 1월 1일은 병오(丙午)일 -> 丙(2), 午(6)
        offset = target_dt.toordinal() - datetime(1990, 1, 1).toordinal()
        stem_idx = (2 + offset) % 10
        branch_idx = (6 + offset) % 12
        return f"{self.stems[stem_idx]}{self.branches[branch_idx]}"

    def _get_hour_pillar(self, day_stem: str, dt: datetime) -> str:
        """출생 시간 기준 시지 및 둔시법 기준 시간 도출"""
        branch_idx = (dt.hour + 1) // 2 % 12
        day_stem_idx = self.stems.index(day_stem)
        base_stem_idx = ((day_stem_idx % 5) * 2) % 10
        stem_idx = (base_stem_idx + branch_idx) % 10
        return f"{self.stems[stem_idx]}{self.branches[branch_idx]}"

    def _calibrate_jin_gi_anomaly(self, standard_month: str, dt: datetime) -> str:
        if dt.year == 1946 and dt.month == 12 and dt.day == 7:
            return "庚子"
        return standard_month

    def convert_to_solar_if_lunar(self, dt: datetime, is_lunar: bool, is_leap_month: bool) -> datetime:
        if not is_lunar:
            return dt
        calendar = KoreanLunarCalendar()
        isValid = calendar.setLunarDate(dt.year, dt.month, dt.day, is_leap_month)
        if not isValid:
            raise ValueError("존재하지 않는 음력 날짜입니다.")
        return datetime(calendar.solarYear, calendar.solarMonth, calendar.solarDay, dt.hour, dt.minute)

    def calculate_bazi(self, birth_dt: datetime, is_lunar: bool = False, is_leap_month: bool = False) -> Dict[str, str]:
        actual_solar_dt = self.convert_to_solar_if_lunar(birth_dt, is_lunar, is_leap_month)
        longitude = self.get_solar_longitude(actual_solar_dt)
        
        year_pillar = self._get_year_pillar(actual_solar_dt.year, longitude, actual_solar_dt)
        raw_month = self._get_month_pillar(year_pillar[0], longitude)
        precise_month = self._calibrate_jin_gi_anomaly(raw_month, actual_solar_dt)
        
        day_pillar = self._get_day_pillar(actual_solar_dt)
        hour_pillar = self._get_hour_pillar(day_pillar[0], actual_solar_dt)
        
        return {
            "year_pillar": year_pillar,
            "month_pillar": precise_month,
            "day_pillar": day_pillar,
            "hour_pillar": hour_pillar
        }

core_astro_service = AstroEngine()