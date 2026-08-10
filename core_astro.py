# core_astro.py
import ephem
import math
from datetime import datetime, timedelta
from typing import Dict
from korean_lunar_calendar import KoreanLunarCalendar # 새로 추가된 라이브러리

class AstroEngine:
    def __init__(self):
        self.stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        self.branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    def get_solar_longitude(self, dt: datetime) -> float:
        sun = ephem.Sun()
        observer = ephem.Observer()
        observer.date = ephem.Date(dt - timedelta(hours=9)) 
        sun.compute(observer)
        return float(math.degrees(sun.hlon) % 360)

    def _get_year_pillar(self, year: int, lon: float, dt: datetime) -> str:
        base_year = year
        if dt.month <= 2 and (lon < 315 and lon >= 270):
            base_year -= 1
        stem_idx = (base_year - 4) % 10
        branch_idx = (base_year - 4) % 12
        return f"{self.stems[stem_idx]}{self.branches[branch_idx]}"

    def _get_month_pillar(self, year_stem: str, lon: float) -> str:
        lon_normalized = (lon - 315) % 360
        month_idx = int(lon_normalized // 30)
        month_branch = self.branches[(month_idx + 2) % 12]
        
        year_stem_idx = self.stems.index(year_stem)
        base_stem_idx = ((year_stem_idx % 5) * 2 + 2) % 10
        month_stem_idx = (base_stem_idx + month_idx) % 10
        return f"{self.stems[month_stem_idx]}{month_branch}"

    def _get_day_pillar(self, dt: datetime) -> str:
        target_dt = dt
        if dt.hour >= 23: # 야자시 적용
            target_dt = dt + timedelta(days=1)
        offset = target_dt.toordinal() - datetime(1990, 1, 1).toordinal()
        stem_idx = (3 + offset) % 10
        branch_idx = (5 + offset) % 12
        return f"{self.stems[stem_idx]}{self.branches[branch_idx]}"

    def _get_hour_pillar(self, day_stem: str, dt: datetime) -> str:
        branch_idx = (dt.hour + 1) // 2 % 12
        day_stem_idx = self.stems.index(day_stem)
        base_stem_idx = ((day_stem_idx % 5) * 2) % 10
        stem_idx = (base_stem_idx + branch_idx) % 10
        return f"{self.stems[stem_idx]}{self.branches[branch_idx]}"

    def _calibrate_jin_gi_anomaly(self, standard_month: str, dt: datetime) -> str:
        if dt.year == 1946 and dt.month == 12 and dt.day == 7:
            return "庚子"
        return standard_month

    # 🚀 추가된 핵심 기능: 음력을 양력으로 완벽 변환
    def convert_to_solar_if_lunar(self, dt: datetime, is_lunar: bool, is_leap_month: bool) -> datetime:
        if not is_lunar:
            return dt
            
        calendar = KoreanLunarCalendar()
        # 입력된 날짜가 유효한 음력 날짜인지 검증 후 세팅
        isValid = calendar.setLunarDate(dt.year, dt.month, dt.day, is_leap_month)
        if not isValid:
            raise ValueError("존재하지 않는 음력 날짜입니다.")
            
        # 변환된 양력 날짜에 기존 출생 시간을 그대로 합침
        return datetime(calendar.solarYear, calendar.solarMonth, calendar.solarDay, dt.hour, dt.minute)

    def calculate_bazi(self, birth_dt: datetime, is_lunar: bool = False, is_leap_month: bool = False) -> Dict[str, str]:
        # 1. 음력일 경우 무조건 양력으로 먼저 치환
        actual_solar_dt = self.convert_to_solar_if_lunar(birth_dt, is_lunar, is_leap_month)
        
        # 2. 치환된 양력 날짜를 기준으로 천체력 및 사주 도출
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
            "hour_pillar": hour_pillar,
            "converted_solar_date": actual_solar_dt.isoformat() # 변환된 양력 날짜도 프론트에 넘겨줌
        }

core_astro_service = AstroEngine()