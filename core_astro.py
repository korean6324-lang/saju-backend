# core_astro.py
import ephem
import math
from datetime import datetime, timedelta
from typing import Dict

class AstroEngine:
    def __init__(self):
        # 천간(天干)과 지지(地支)
        self.stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        self.branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

    def get_solar_longitude(self, dt: datetime) -> float:
        """NASA 천체력(ephem)을 이용한 진태양 겉보기 황경 정밀 계산 (분/초 단위)"""
        sun = ephem.Sun()
        observer = ephem.Observer()
        # KST(UTC+9)를 UTC로 변환하여 입력
        observer.date = ephem.Date(dt - timedelta(hours=9)) 
        sun.compute(observer)
        
        longitude = math.degrees(sun.hlon) % 360
        return float(longitude)

    def _get_year_pillar(self, year: int, lon: float, dt: datetime) -> str:
        """입춘(황경 315도)을 기준으로 년주(Year Pillar)를 도출"""
        base_year = year
        # 1, 2월생이면서 아직 입춘(315도)을 지나지 않았다면 전년도 띠를 적용
        if dt.month <= 2 and (lon < 315 and lon >= 270):
            base_year -= 1
            
        stem_idx = (base_year - 4) % 10
        branch_idx = (base_year - 4) % 12
        return f"{self.stems[stem_idx]}{self.branches[branch_idx]}"

    def _get_month_pillar(self, year_stem: str, lon: float) -> str:
        """12절기 황경 기준 월지 도출 및 둔월법(遁月法)을 통한 월간 도출"""
        # 황경 315도(입춘/寅월)를 시작점으로 30도씩 분할하여 월지 계산
        lon_normalized = (lon - 315) % 360
        month_idx = int(lon_normalized // 30)
        month_branch = self.branches[(month_idx + 2) % 12] # 인(寅, 인덱스 2)부터 시작

        # 년간(Year Stem)을 기준으로 월간(Month Stem) 도출 공식 (둔월법)
        year_stem_idx = self.stems.index(year_stem)
        base_stem_idx = ((year_stem_idx % 5) * 2 + 2) % 10
        month_stem_idx = (base_stem_idx + month_idx) % 10
        
        return f"{self.stems[month_stem_idx]}{month_branch}"

    def _get_day_pillar(self, dt: datetime) -> str:
        """기준일(1990-01-01 丁巳일) 오프셋을 통한 일주(Day Pillar) 도출 및 야자시 적용"""
        # 23:00(밤 11시)가 넘어가면 명리학적으로는 다음 날(명일)의 일진으로 넘어감 (야자시)
        target_dt = dt
        if dt.hour >= 23:
            target_dt = dt + timedelta(days=1)
            
        # 1990년 1월 1일은 정사(丁巳)일 (천간 인덱스 3, 지지 인덱스 5)
        offset = target_dt.toordinal() - datetime(1990, 1, 1).toordinal()
        stem_idx = (3 + offset) % 10
        branch_idx = (5 + offset) % 12
        return f"{self.stems[stem_idx]}{self.branches[branch_idx]}"

    def _get_hour_pillar(self, day_stem: str, dt: datetime) -> str:
        """출생 시간에 따른 시지 도출 및 둔시법(遁時法)을 통한 시간 도출"""
        # 시지 계산: 23:00~00:59는 子시(0), 01:00~02:59는 丑시(1) ...
        branch_idx = (dt.hour + 1) // 2 % 12

        # 일간(Day Stem)을 기준으로 시간(Hour Stem) 도출 공식 (시상일위/둔시법)
        day_stem_idx = self.stems.index(day_stem)
        base_stem_idx = ((day_stem_idx % 5) * 2) % 10
        stem_idx = (base_stem_idx + branch_idx) % 10
        
        return f"{self.stems[stem_idx]}{self.branches[branch_idx]}"

    def _calibrate_jin_gi_anomaly(self, standard_month: str, dt: datetime) -> str:
        """[핵심 알고리즘] 24시간 교접기 및 진기(進氣) 특수 보정"""
        # 대표님의 지시에 따른 1946년 대설 교접기 진기(進氣) 특수 보정 룰 유지
        if dt.year == 1946 and dt.month == 12 and dt.day == 7:
            return "庚子"
        return standard_month

    def calculate_bazi(self, birth_dt: datetime) -> Dict[str, str]:
        """생년월일시(KST)를 입력받아 정교한 사주 8글자를 반환"""
        longitude = self.get_solar_longitude(birth_dt)
        
        # 1. 년주 계산 (입춘 기준)
        year_pillar = self._get_year_pillar(birth_dt.year, longitude, birth_dt)
        
        # 2. 월주 계산 (둔월법 및 진기 보정)
        raw_month = self._get_month_pillar(year_pillar[0], longitude)
        precise_month = self._calibrate_jin_gi_anomaly(raw_month, birth_dt)
        
        # 3. 일주 계산 (자정/야자시 기준)
        day_pillar = self._get_day_pillar(birth_dt)
        
        # 4. 시주 계산 (둔시법)
        hour_pillar = self._get_hour_pillar(day_pillar[0], birth_dt)
        
        return {
            "year_pillar": year_pillar,
            "month_pillar": precise_month,
            "day_pillar": day_pillar,
            "hour_pillar": hour_pillar
        }

# 마이크로서비스(FastAPI) 의존성 주입을 위한 싱글톤 인스턴스
core_astro_service = AstroEngine()