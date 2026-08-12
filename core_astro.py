import ephem
import math
from datetime import datetime, timedelta

# ==========================================
# 1. 기초 명리 메타데이터 (천간/지지)
# ==========================================
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

class CoreAstroEngine:
    def __init__(self):
        self.sun = ephem.Sun()

    def _get_solar_longitude(self, dt_utc: datetime) -> float:
        """UTC 기준 진태양 겉보기 황경 계산"""
        observer = ephem.Observer()
        observer.date = ephem.date(dt_utc.strftime('%Y/%m/%d %H:%M:%S'))
        self.sun.compute(observer)
        equatorial = ephem.Equatorial(self.sun.ra, self.sun.dec, epoch=observer.date)
        ecliptic = ephem.Ecliptic(equatorial)
        return math.degrees(ecliptic.lon) % 360

    def get_true_solar_time(self, dt_kst: datetime, longitude: float = 127.0) -> datetime:
        """
        진태양시(True Solar Time) 계산
        1. 지역 경도 보정 (한국 표준시 135도 기준)
        2. 균시차(Equation of Time) 보정
        """
        # 1. 경도 보정: 1도당 4분(240초) 차이 발생
        longitude_diff_seconds = (longitude - 135.0) * 240
        lmt_dt = dt_kst + timedelta(seconds=longitude_diff_seconds)
        
        # 2. 균시차 보정 (근사식 적용)
        day_of_year = lmt_dt.timetuple().tm_yday
        B = math.radians((day_of_year - 81) * 360 / 365.2425)
        eot_minutes = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)
        
        return lmt_dt + timedelta(minutes=eot_minutes)

    def calculate_bazi(self, dt_kst: datetime, gender: str, longitude: float = 127.0, 
                       apply_true_solar: bool = True, apply_yaja: bool = True) -> dict:
        """
        정밀 사주 원국(8글자) 추출 엔진 (완벽 교체판)
        """
        # 1. 시간 보정 (진태양시 적용 여부)
        target_dt = self.get_true_solar_time(dt_kst, longitude) if apply_true_solar else dt_kst
        target_dt_utc = target_dt - timedelta(hours=9)
        
        # 2. 태양 황경 도출 (절기 판단의 핵심)
        ecliptic_lon = self._get_solar_longitude(target_dt_utc)
        
        # --- 연주(Year) ---
        # 🚨 [버그 수정 완료] 입춘(315도) 기준 연주 교체 결함 해결
        if target_dt.month == 1:
            base_year = target_dt.year - 1
        elif target_dt.month == 2:
            if ecliptic_lon < 315:
                base_year = target_dt.year - 1
            else:
                base_year = target_dt.year
        else:
            base_year = target_dt.year

        year_stem_idx = (base_year - 4) % 10
        year_branch_idx = (base_year - 4) % 12
        year_stem = HEAVENLY_STEMS[year_stem_idx]
        year_branch = EARTHLY_BRANCHES[year_branch_idx]
        
        # --- 월주(Month) ---
        # 황경 315도(입춘/인월)를 시작점으로 30도 단위 분기
        month_index = int((ecliptic_lon - 315) % 360 // 30)
        month_branch_idx = (month_index + 2) % 12
        month_stem_idx = ((year_stem_idx % 5) * 2 + 2 + month_index) % 10
        
        month_stem = HEAVENLY_STEMS[month_stem_idx]
        month_branch = EARTHLY_BRANCHES[month_branch_idx]
        
        # --- 일주(Day) 및 시주(Hour) 야자시 로직 ---
        # 🌟 [복구 완료] 파이썬 절대 일수 동기화 오프셋(+14) 원복
        base_day_index = (target_dt.toordinal() + 14) % 60 
        
        hour_val = target_dt.hour
        hour_index = ((hour_val + 1) // 2) % 12
        
        if hour_val >= 23:
            if apply_yaja:
                # 야자시 인정: 일주는 오늘, 시주 천간은 내일 기준
                actual_day_index = base_day_index
                tomorrow_day_index = (base_day_index + 1) % 60
                tomorrow_stem_idx = tomorrow_day_index % 10
                hour_stem_idx = (tomorrow_stem_idx % 5 * 2 + hour_index) % 10
            else:
                # 야자시 불인정(자초야반): 일주/시주 모두 내일로 변경
                actual_day_index = (base_day_index + 1) % 60
                current_stem_idx = actual_day_index % 10
                hour_stem_idx = (current_stem_idx % 5 * 2 + hour_index) % 10
        else:
            actual_day_index = base_day_index
            current_stem_idx = actual_day_index % 10
            hour_stem_idx = (current_stem_idx % 5 * 2 + hour_index) % 10

        day_stem = HEAVENLY_STEMS[actual_day_index % 10]
        day_branch = EARTHLY_BRANCHES[actual_day_index % 12]
        hour_stem = HEAVENLY_STEMS[hour_stem_idx]
        hour_branch = EARTHLY_BRANCHES[hour_index]

        return {
            "origin_time": dt_kst.strftime('%Y-%m-%d %H:%M:%S'),
            "corrected_time": target_dt.strftime('%Y-%m-%d %H:%M:%S'),
            "bazi": {
                "year_pillar": f"{year_stem}{year_branch}",
                "month_pillar": f"{month_stem}{month_branch}",
                "day_pillar": f"{day_stem}{day_branch}",
                "hour_pillar": f"{hour_stem}{hour_branch}"
            },
            "options": {
                "longitude_applied": longitude if apply_true_solar else None,
                "yaja_applied": apply_yaja
            },
            "gender": "Male" if gender == 'M' else "Female"
        }