import calendar
import os
import json
import hashlib
import logging
from enum import Enum
from typing import Optional, Union
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from korean_lunar_calendar import KoreanLunarCalendar
import copy

from cachetools import TTLCache
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# ==========================================
# 🌟 모든 엔진 총동원 (비전 엔진 및 풍수 엔진 포함)
# ==========================================
from core_astro import CoreAstroEngine
from core_mechanics import MechanicsEngine
from dictionary import DictionaryEngine
from logic_dynamics import DynamicsEngine
from logic_fengshui import FengShuiEngine
from logic_gunghap import UltimateGunghapEngine as GunghapEngine
from logic_practical import PracticalEngine
from logic_unse import UnseEngine
from logic_yongshin import YongshinEngine
from logic_classical import ClassicalEngine 
from logic_secret import SecretEngine

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Myeongri Master Bridge API", version="4.0.0")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

astro = CoreAstroEngine()
mech = MechanicsEngine()
dict_db = DictionaryEngine()
dyn = DynamicsEngine()
feng = FengShuiEngine()
ghap = GunghapEngine()
prac = PracticalEngine()
unse = UnseEngine()
yong = YongshinEngine()
clas = ClassicalEngine() 
sec = SecretEngine() 

BAZI_CACHE = TTLCache(maxsize=10000, ttl=86400)
CALENDAR_CACHE = TTLCache(maxsize=5000, ttl=86400)    

def get_cache_key(req_data: dict, today_str: str) -> str:
    serialized = json.dumps(req_data, sort_keys=True) + today_str
    return hashlib.md5(serialized.encode('utf-8')).hexdigest()

NAPEUM_RICH_DESC = {
    "해중금": "바다 깊은 곳에 잠긴 보석. 겉으로 드러나지 않는 깊은 내공과 무한한 잠재력을 지니고 있습니다.",
    "노중화": "화로 속에서 타오르는 불꽃. 따뜻하고 보호받는 환경에서 은근한 끈기와 지성을 발휘합니다.",
    "대림목": "울창하고 거대한 숲. 스케일이 크고 수많은 생명을 품어내는 웅장한 포용력을 뜻합니다.",
    "대림토": "울창하고 거대한 숲(대림목). 스케일이 크고 수많은 생명을 품어내는 웅장한 포용력을 뜻합니다.",
    "노방토": "사람들이 밟고 지나가는 길가의 흙. 희생정신이 강하고 친화력이 뛰어나 대중과 잘 어울립니다.",
    "검봉금": "날카롭게 벼려진 명검. 불의를 참지 않는 예리한 결단력과 강력한 카리스마를 발휘합니다.",
    "산두화": "산봉우리에서 타오르는 횃불. 멀리서도 빛을 발하며 사람들을 이끄는 선구자적 기질이 있습니다.",
    "간하수": "산골짜기를 흐르는 맑은 시냇물. 잔잔하면서도 멈추지 않는 생명력과 맑고 순수한 영혼을 가졌습니다.",
    "성두토": "성벽을 이루는 단단한 흙. 외부의 적을 막아내는 굳건한 책임감과 흔들림 없는 원칙을 상징합니다.",
    "백랍금": "촛물처럼 굳어지는 부드러운 금. 유연성과 융통성이 뛰어나며 환경에 맞게 자신을 다듬어냅니다.",
    "백납금": "촛물처럼 굳어지는 부드러운 금. 유연성과 융통성이 뛰어나며 환경에 맞게 자신을 다듬어냅니다.",
    "양류목": "물가에 흐드러진 수양버들. 부드럽고 유연하며, 거센 바람에도 부러지지 않는 처세술이 뛰어납니다.",
    "천중수": "땅속 깊은 곳에서 솟아나는 옹달샘. 마르지 않는 지혜와 타인에게 베푸는 순수한 자비심이 있습니다.",
    "옥상토": "지붕 위에 덮인 기와/흙. 외부의 풍파로부터 사람들을 보호하며 높은 곳에서 세상을 굽어봅니다.",
    "벽력화": "어둠을 가르는 천둥 번개. 순간적으로 폭발하는 천재성과 누구도 흉내 내지 못할 독창성을 가졌습니다.",
    "송백목": "한겨울에도 푸른 소나무와 잣나무. 어떤 시련 속에서도 굽히지 않는 지조와 매서운 절개가 있습니다.",
    "장류수": "끊임없이 흘러가는 긴 강물. 멈추지 않는 도전정신과 거대한 세력을 형성하여 바다로 나아가는 기상입니다.",
    "사중금": "모래 속에 파묻힌 사금. 오랜 시간 다듬어지고 발견되기를 기다리는 귀하고 섬세한 가치입니다.",
    "산하화": "산기슭에서 타오르는 노을/불꽃. 은은하면서도 세상을 아름답게 물들이는 예술적 감각이 돋보입니다.",
    "평지목": "평야에 자라난 나무. 평탄한 환경 속에서 안정적으로 성장하며 무난하고 건실한 삶을 추구합니다.",
    "벽상토": "집을 지탱하는 벽의 흙. 겉보기엔 평범하나 사람들의 안식처를 지탱하는 보이지 않는 든든한 조력자입니다.",
    "금박금": "불상을 입히는 얇은 금박. 화려하고 장엄한 매력으로 타인을 돋보이게 하는 특수하고 빛나는 재능입니다.",
    "복등화": "어둠을 밝히는 등잔불. 고독하고 외로운 이들에게 희망을 주는 따뜻하고 헌신적인 종교적/철학적 기운입니다.",
    "천하수": "하늘에서 내리는 은하수/비. 만물을 적시고 생명을 부여하는 맑고 고결한 영혼과 순수함이 있습니다.",
    "대역토": "넓은 광야와 역마의 흙. 스케일이 방대하고 여러 지역을 아우르는 수용력과 무역/유통의 기운을 뜻합니다.",
    "차천금": "여인을 장식하는 비녀와 팔찌. 세련되고 섬세한 미적 감각과 귀족적이고 화려한 품격을 상징합니다.",
    "상자목": "비단을 짜는 누에를 치는 뽕나무. 타인을 위해 유용한 가치를 창출하고 희생으로 큰 업적을 이룹니다.",
    "대계수": "깊은 산에서 모여 흐르는 계곡물. 맑고 차가운 지성으로 만물의 갈증을 해소하는 학자적 기질이 있습니다.",
    "사중토": "모래와 섞인 흙. 비바람을 견디며 자신만의 견고한 터전을 일구어내는 강인하고 거친 끈기가 있습니다.",
    "천상화": "하늘 한가운데 뜬 태양. 천하를 공평하게 비추며 만물을 길러내는 압도적인 스케일과 공명정대함을 가졌습니다.",
    "석류목": "가을에 단단하게 익은 석류나무. 화려함 속에 꽉 찬 결실을 품고 있으며 재물과 자손의 번창을 상징합니다.",
    "대해수": "모든 것을 삼키는 거대한 바다. 속을 알 수 없는 깊은 지혜와 모든 선악을 포용하는 압도적인 수용력이 있습니다."
}

FAQ_DB = [
    {"q": "대운수 수동 지정은 언제 사용하는 기능인가요?", "a": "명리학에서 대운이 바뀌는 나이는 절기의 거리를 계산해 도출됩니다. 경계선(교운기) 출생의 경우 체감 운기에 맞춰 대운수를 보정하는 기능입니다."},
    {"q": "고법(古法) 둔월법이란 무엇인가요?", "a": "절기(양력) 기준이 아닌 순수 '음력 달' 기준으로 월주를 강제 세워 심층 분석하는 고법 명리 기능입니다."},
    {"q": "마스터 엔진의 궁합은 일반 궁합과 무엇이 다른가요?", "a": "일지 속궁합, 구궁 팔괘(본명성), 삼원갑자를 크로스체크하여 부부 권력 구조와 파국의 타이밍까지 적나라하게 분석합니다."}
]

class GenderEnum(str, Enum):
    M = "M"
    F = "F"

class CalendarTypeEnum(str, Enum):
    solar = "solar"
    lunar = "lunar"
    lunar_leap = "lunar_leap"

class BaziRequest(BaseModel):
    datetime_str: str = Field(..., description="YYYY-MM-DD HH:MM 형태의 날짜")
    calendar_type: CalendarTypeEnum = Field(CalendarTypeEnum.solar, description="solar, lunar, lunar_leap")
    gender: GenderEnum = Field(..., description="M or F")
    longitude: Union[float, str, None] = Field(127.0, description="태어난 지역 경도")
    timezone: int = Field(9, description="표준 시간대")
    unknown_time: bool = False
    apply_true_solar: bool = True
    apply_yaja: bool = True
    daewun_num: int = 1
    apply_traditional_lunar: bool = False
    lunar_month: Optional[int] = None

    partner_datetime_str: Optional[str] = None
    partner_calendar_type: CalendarTypeEnum = CalendarTypeEnum.solar
    partner_gender: Optional[GenderEnum] = None
    partner_longitude: Union[float, str, None] = 127.0
    partner_timezone: int = 9
    partner_unknown_time: bool = False
    partner_apply_traditional_lunar: bool = False
    partner_lunar_month: Optional[int] = None
    partner_daewun_num: Optional[int] = None

class CalendarRequest(BaseModel):
    datetime_str: str = Field(..., description="YYYY-MM-DD HH:MM 형태의 날짜")
    calendar_type: CalendarTypeEnum = Field(CalendarTypeEnum.solar, description="solar, lunar, lunar_leap")
    gender: GenderEnum = Field(..., description="M or F")
    longitude: Union[float, str, None] = Field(127.0, description="태어난 지역 경도")
    timezone: int = Field(9, description="표준 시간대")
    unknown_time: bool = False
    apply_true_solar: bool = True
    apply_yaja: bool = True
    apply_traditional_lunar: bool = False
    lunar_month: Optional[int] = None
    target_year: int = Field(default_factory=lambda: (datetime.utcnow() + timedelta(hours=9)).year)
    target_month: int = Field(default_factory=lambda: (datetime.utcnow() + timedelta(hours=9)).month)

def adjust_korean_dst(dt: datetime) -> tuple[datetime, bool]:
    dst_ranges = [
        (datetime(1948, 6, 1), datetime(1948, 9, 13)),
        (datetime(1949, 4, 3), datetime(1949, 9, 11)),
        (datetime(1950, 4, 1), datetime(1950, 9, 10)),
        (datetime(1951, 5, 6), datetime(1951, 9, 9)),
        (datetime(1955, 5, 5), datetime(1955, 9, 9)),
        (datetime(1956, 5, 20), datetime(1956, 9, 30)),
        (datetime(1957, 5, 5), datetime(1957, 9, 22)),
        (datetime(1958, 5, 18), datetime(1958, 9, 21)),
        (datetime(1959, 5, 10), datetime(1959, 9, 20)),
        (datetime(1960, 5, 1), datetime(1960, 9, 18)),
        (datetime(1987, 5, 10, 2), datetime(1987, 10, 11, 3)),
        (datetime(1988, 5, 8, 2), datetime(1988, 10, 9, 3)),
    ]
    for start, end in dst_ranges:
        if start <= dt < end:
            return dt - timedelta(hours=1), True
    return dt, False

def build_bridge_response(dt_kst, astro_res, gender, daewun_num, partner_info, apply_trad, lunar_m, unknown_time, real_lunar_m, real_lunar_d, is_dst_applied):
    
    try:
        bazi_raw = astro_res.get("bazi", {})
        y_stem, y_branch = bazi_raw.get("year_pillar", ["-", "-"])[0], bazi_raw.get("year_pillar", ["-", "-"])[1]
        m_stem, m_branch = bazi_raw.get("month_pillar", ["-", "-"])[0], bazi_raw.get("month_pillar", ["-", "-"])[1]
        d_stem, d_branch = bazi_raw.get("day_pillar", ["-", "-"])[0], bazi_raw.get("day_pillar", ["-", "-"])[1]
        
        if unknown_time:
            h_stem, h_branch = "-", "-"
        else:
            h_stem, h_branch = bazi_raw.get("hour_pillar", ["-", "-"])[0], bazi_raw.get("hour_pillar", ["-", "-"])[1]
    except Exception:
        y_stem, y_branch, m_stem, m_branch, d_stem, d_branch, h_stem, h_branch = ["-"] * 8

    if apply_trad and lunar_m:
        try:
            trad_m_stem, trad_m_branch = mech.get_traditional_month_pillar(y_stem, lunar_m)
            if trad_m_stem and trad_m_branch: 
                m_stem, m_branch = trad_m_stem, trad_m_branch
        except Exception:
            pass

    day_master = d_stem

    def get_tg(stem_or_branch):
        if stem_or_branch == "-": return "-"
        try:
            return mech.get_ten_god(day_master, stem_or_branch)
        except Exception:
            return "-"

    bazi_data = {
        "year": {
            "stem": y_stem, "stem_tg": get_tg(y_stem), 
            "branch": y_branch, "branch_tg": get_tg(y_branch),
            "napeum": mech.get_napeum(y_stem, y_branch)
        },
        "month": {
            "stem": m_stem, "stem_tg": get_tg(m_stem), 
            "branch": m_branch, "branch_tg": get_tg(m_branch),
            "napeum": mech.get_napeum(m_stem, m_branch)
        },
        "day": {
            "stem": d_stem, "stem_tg": "일간", 
            "branch": d_branch, "branch_tg": get_tg(d_branch),
            "napeum": mech.get_napeum(d_stem, d_branch)
        },
        "hour": {
            "stem": h_stem, "stem_tg": get_tg(h_stem), 
            "branch": h_branch, "branch_tg": get_tg(h_branch),
            "napeum": mech.get_napeum(h_stem, h_branch)
        }
    }

    try:
        hidden_stems = {
            "year": mech.get_hidden_stems(y_branch),
            "month": mech.get_hidden_stems(m_branch),
            "day": mech.get_hidden_stems(d_branch),
            "hour": {"initial": ["-"], "middle": ["-"], "main": ["-"]} if unknown_time else mech.get_hidden_stems(h_branch)
        }
    except Exception:
        hidden_stems = {}

    bazi_for_engine = {
        "year": bazi_data["year"], 
        "month": bazi_data["month"],
        "day": bazi_data["day"], 
        "hour": bazi_data["hour"]
    }
    
    # 🚨 [HOTFIX] Energy & Balance 데이터 안정성 및 렌더링을 위한 Safe Dictionary 매핑 적용
    try:
        geokguk_raw = yong.determine_geokguk(bazi_for_engine, hidden_stems)
        strength_raw = yong.determine_strength(bazi_for_engine)
        yongshin_raw = yong.determine_yongshin(bazi_for_engine, strength_raw)

        strength = {
            "my_power": strength_raw.get("my_power", 50),
            "other_power": strength_raw.get("other_power", 50),
            "status": strength_raw.get("status") or "중화(中和)",
            "status_code": strength_raw.get("status_code") or "NORMAL",
            "instability": strength_raw.get("instability", False),
            "expert_advice": strength_raw.get("expert_advice") or "사주의 전체적인 기운과 체급을 나타냅니다."
        }
        
        geokguk = {
            "name_clean": geokguk_raw.get("name_clean") or geokguk_raw.get("name") or "기본격",
            "hanja_clean": geokguk_raw.get("hanja_clean") or geokguk_raw.get("hanja") or "",
            "desc": geokguk_raw.get("desc") or "자신의 능력을 사회적 가치로 훌륭하게 환원하는 그릇입니다."
        }
        
        yongshin_data = {
            "yongshin": yongshin_raw.get("yongshin") or "균형과 조화",
            "huishin": yongshin_raw.get("huishin") or "보완 기운",
            "gishin": yongshin_raw.get("gishin") or "주의 기운",
            "desc": yongshin_raw.get("desc") or "일간의 세력과 월령의 기운이 조화를 이루어 중용을 취하고 있습니다. 과도하게 치우치지 않아 평탄하며, 꾸준한 자기개발과 안정을 유지하는 것이 최고의 길입니다."
        }
    except Exception as e:
        logger.error(f"Yongshin Error: {e}")
        geokguk, strength, yongshin_data = {}, {}, {}

    try:
        valid_stems = [s for s in [y_stem, m_stem, d_stem, h_stem] if s != "-"]
        valid_branches = [b for b in [y_branch, m_branch, d_branch, h_branch] if b != "-"]
        elements_dist = mech.get_five_elements_distribution(valid_stems, valid_branches)
    except Exception:
        elements_dist = {}
    
    try:
        career = prac.analyze_career(geokguk, yongshin_data)
    except Exception:
        career = {}

    try:
        health_raw = prac.analyze_health(elements_dist, gender=gender)
    except TypeError:
        try:
            health_raw = prac.analyze_health(elements_dist)
        except Exception:
            health_raw = []
    except Exception:
        health_raw = []
    
    elements_imbalance = []
    for h in health_raw:
        if h.get("element") != "종합":
            elements_imbalance.append({
                "element": h.get("element", ""), 
                "type": h.get("status_code", "양호"), 
                "original_status": h.get("status", ""), 
                "count": elements_dist.get(h.get("element", ""), 0), 
                "desc": h.get("advice", ""),
                "organ": h.get("organ", ""),     
                "symptom": h.get("symptom", "")  
            })

    try:
        special_stars = dyn.scan_special_stars({"year": y_stem, "month": m_stem, "day": d_stem, "hour": h_stem}, {"year": y_branch, "month": m_branch, "day": d_branch, "hour": h_branch})
        disasters = dyn.scan_disasters(valid_branches)
    except Exception:
        special_stars, disasters = [], []

    try:
        classical_reading = clas.generate_classical_reading(bazi_for_engine, yongshin_data, strength, gender, real_lunar_m, real_lunar_d)
    except TypeError:
        try:
            classical_reading = clas.generate_classical_reading(bazi_for_engine, yongshin_data, strength)
        except Exception:
            classical_reading = "고전 엔진 연산 중 오류가 발생했습니다."
    except Exception as e:
        logger.error(f"Classical Engine Error: {e}")
        classical_reading = "고전 엔진 내부 연산 오류."

    try:
        tonggeun_branches = {"year": y_branch, "month": m_branch, "day": d_branch}
        if not unknown_time: tonggeun_branches["hour"] = h_branch
        tonggeun = mech.check_tonggeun(day_master, tonggeun_branches)
    except Exception:
        tonggeun = None

    try:
        now_kst = datetime.utcnow() + timedelta(hours=9)
        now_astro = astro.calculate_bazi(now_kst, gender)
        now_y_b = now_astro.get("bazi", {}).get("year_pillar", ["-", "-"])[1]
        now_m_b = now_astro.get("bazi", {}).get("month_pillar", ["-", "-"])[1]
        now_d_b = now_astro.get("bazi", {}).get("day_pillar", ["-", "-"])[1]

        unse_data = {
            "year": {**unse.analyze_sewun(bazi_for_engine, now_y_b, mech.get_ten_god(day_master, now_y_b), yongshin_data), "stem": now_astro.get("bazi", {}).get("year_pillar", ["-", "-"])[0], "branch": now_y_b},
            "month": {"month_num": now_kst.month, "stem": now_astro.get("bazi", {}).get("month_pillar", ["-", "-"])[0], "branch": now_m_b, "data": unse.analyze_wolgeon(bazi_for_engine, now_m_b, mech.get_ten_god(day_master, now_m_b), yongshin_data)},
            "day": {"day_num": now_kst.day, "stem": now_astro.get("bazi", {}).get("day_pillar", ["-", "-"])[0], "branch": now_d_b, "data": unse.analyze_iljin(bazi_for_engine, now_d_b, mech.get_ten_god(day_master, now_d_b), yongshin_data)}
        }
    except Exception as e:
        logger.error(f"Unse Error: {e}")
        unse_data = None

    try:
        daewun_raw = mech.get_daewun_sequence(gender, y_stem, m_stem, m_branch, int(daewun_num), 10)
        if isinstance(daewun_raw, dict) and "timeline" in daewun_raw:
            timeline_list = daewun_raw["timeline"]
        elif isinstance(daewun_raw, list):
            timeline_list = daewun_raw
            daewun_raw = {"timeline": timeline_list}
        else:
            timeline_list = []
            daewun_raw = {"timeline": []}
            
        for dw in timeline_list:
            dw["stem_tg"] = get_tg(dw.get("stem", "-"))
            dw["branch_tg"] = get_tg(dw.get("branch", "-"))
    except Exception as e:
        logger.error(f"Daewun sequence error (Backward Calculation Failed): {e}")
        daewun_raw = {"timeline": []}
        
    try:
        sewun_raw = mech.get_sewun_sequence(datetime.utcnow().year + 9 - 4, 10)
        if isinstance(sewun_raw, list):
            for sw in sewun_raw:
                sw["stem_tg"] = get_tg(sw.get("stem", "-"))
                sw["branch_tg"] = get_tg(sw.get("branch", "-"))
        else:
            sewun_raw = []
    except Exception as e:
        logger.error(f"Sewun sequence error: {e}")
        sewun_raw = []

    try:
        secret_readings_data = sec.get_secrets(bazi_for_engine, daewun_raw)
    except Exception:
        secret_readings_data = None

    try:
        my_star = ghap.get_bonmyeongseong(dt_kst.year, gender)
    except TypeError:
        try:
            my_star = ghap.get_bonmyeongseong(dt_kst.year)
        except Exception:
            my_star = {"number": 1, "name": "알 수 없음", "hanja": "無"}
    except Exception:
        my_star = {"number": 1, "name": "알 수 없음", "hanja": "無"}

    try:
        fengshui_honmyeong = feng.calculate_honmyeong_gung(dt_kst.year, gender)
        fengshui_dirs = feng.get_auspicious_directions(fengshui_honmyeong.get("number", 1))
        fengshui_data = {
            "honmyeong": fengshui_honmyeong,
            "directions": fengshui_dirs
        }
    except Exception as e:
        logger.error(f"FengShui Routing Error: {str(e)}")
        fengshui_data = None

    gunghap_data = None
    ideal_partner_data = None
    
    if partner_info:
        try:
            p_dt = partner_info["dt"]
            p_gender = partner_info["gender"]
            p_lon = partner_info["longitude"]
            p_unk_time = partner_info["unknown_time"]
            p_lunar_m = partner_info.get("lunar_month", 1)
            
            p_astro = astro.calculate_bazi(p_dt, p_gender, p_lon, False if p_unk_time else True, True)
            p_bazi_raw = p_astro.get("bazi", {})
            p_day_master = p_bazi_raw.get("day_pillar", ["-", "-"])[0]
            
            def get_p_tg(stem_or_branch):
                if stem_or_branch == "-": return "-"
                try:
                    return mech.get_ten_god(p_day_master, stem_or_branch)
                except:
                    return "-"

            p_h_s = "-" if p_unk_time else p_bazi_raw.get("hour_pillar", ["-", "-"])[0]
            p_h_b = "-" if p_unk_time else p_bazi_raw.get("hour_pillar", ["-", "-"])[1]

            p_bazi_for_engine = {
                "year": {"stem": p_bazi_raw.get("year_pillar", ["-", "-"])[0], "branch": p_bazi_raw.get("year_pillar", ["-", "-"])[1], "stem_tg": get_p_tg(p_bazi_raw.get("year_pillar", ["-", "-"])[0]), "branch_tg": get_p_tg(p_bazi_raw.get("year_pillar", ["-", "-"])[1])},
                "month": {"stem": p_bazi_raw.get("month_pillar", ["-", "-"])[0], "branch": p_bazi_raw.get("month_pillar", ["-", "-"])[1], "stem_tg": get_p_tg(p_bazi_raw.get("month_pillar", ["-", "-"])[0]), "branch_tg": get_p_tg(p_bazi_raw.get("month_pillar", ["-", "-"])[1])},
                "day": {"stem": p_bazi_raw.get("day_pillar", ["-", "-"])[0], "branch": p_bazi_raw.get("day_pillar", ["-", "-"])[1], "stem_tg": "일간", "branch_tg": get_p_tg(p_bazi_raw.get("day_pillar", ["-", "-"])[1])},
                "hour": {"stem": p_h_s, "branch": p_h_b, "stem_tg": get_p_tg(p_h_s), "branch_tg": get_p_tg(p_h_b)}
            }
            
            p_valid_stems = [p_bazi_for_engine[k]["stem"] for k in p_bazi_for_engine if p_bazi_for_engine[k]["stem"] != "-"]
            p_valid_branches = [p_bazi_for_engine[k]["branch"] for k in p_bazi_for_engine if p_bazi_for_engine[k]["branch"] != "-"]
            p_elements_dist = mech.get_five_elements_distribution(p_valid_stems, p_valid_branches)
            
            p_strength = yong.determine_strength(p_bazi_for_engine)
            p_yongshin_data = yong.determine_yongshin(p_bazi_for_engine, p_strength)

            try:
                p_star = ghap.get_bonmyeongseong(p_dt.year, p_gender)
            except TypeError:
                try:
                    p_star = ghap.get_bonmyeongseong(p_dt.year)
                except Exception:
                    p_star = {"number": 1, "name": "알 수 없음", "hanja": "無"}
            except Exception:
                p_star = {"number": 1, "name": "알 수 없음", "hanja": "無"}
            
            is_m = (gender == "M")
            m_bazi = bazi_for_engine if is_m else p_bazi_for_engine
            f_bazi = p_bazi_for_engine if is_m else bazi_for_engine
            
            m_l_m = real_lunar_m if is_m else p_lunar_m
            f_l_m = p_lunar_m if is_m else real_lunar_m
            
            m_yong = yongshin_data if is_m else p_yongshin_data
            f_yong = p_yongshin_data if is_m else yongshin_data
            
            m_elem = elements_dist if is_m else p_elements_dist
            f_elem = p_elements_dist if is_m else elements_dist
            
            m_st = my_star.get("number", 1) if is_m else p_star.get("number", 1)
            f_st = p_star.get("number", 1) if is_m else my_star.get("number", 1)

            gunghap_data = ghap.get_ultimate_compatibility(
                m_bazi=m_bazi, f_bazi=f_bazi, 
                m_lunar_m=m_l_m, f_lunar_m=f_l_m, 
                m_yongshin=m_yong, f_yongshin=f_yong, 
                m_elements=m_elem, f_elements=f_elem, 
                m_star=m_st, f_star=f_st
            )
            
            gunghap_data["my_star"] = my_star
            gunghap_data["partner_star"] = p_star
            
        except Exception as e:
            logger.error(f"Gunghap Routing Error: {str(e)}", exc_info=True)
            gunghap_data = {
                "fatal_warnings": ["궁합 분석 중 엔진 내부 충돌이 발생하여 연산이 중단되었습니다."],
                "elemental_salvation": {"score": 0, "desc": "데이터를 해석할 수 없습니다."},
                "match_3d": {"mental": {"status": "오류"}, "physical": {"status": "오류"}},
                "gugung_matrix": {"status": "오류", "desc": "엔진 렌더링 실패"}
            }
    else:
        try:
            ideal_partner_data = ghap.get_ideal_partner(bazi_for_engine, yongshin_data, my_star.get("number", 1), gender)
        except TypeError:
            try:
                ideal_partner_data = ghap.get_ideal_partner(bazi_for_engine, yongshin_data, my_star.get("number", 1))
            except Exception:
                ideal_partner_data = None
        except Exception as e:
            logger.error(f"Ideal Partner Routing Error: {str(e)}", exc_info=True)
            ideal_partner_data = None

    try:
        metadata_dict = {}
        terms_to_fetch = set(["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "비견", "겁재", "식신", "상관", "편재", "정재", "편관", "정관", "편인", "정인", "공망"])
        for p in bazi_data.values():
            terms_to_fetch.add(p.get('stem_tg', ''))
            terms_to_fetch.add(p.get('branch_tg', ''))
            
        for term in terms_to_fetch:
            if term and term != "일간" and term != "-": 
                original_meta = mech.get_metadata(term)
                if isinstance(original_meta, str):
                    meta = {"hanja": "", "meaning": original_meta}
                elif isinstance(original_meta, dict):
                    meta = copy.deepcopy(original_meta)
                else:
                    meta = {"hanja": "", "meaning": ""}
                metadata_dict[term] = meta
    except Exception as e:
        logger.error(f"Metadata fetch error: {e}")
        metadata_dict = {}

    def get_napeum_desc(pillar_type, napeum_full):
        if not napeum_full or napeum_full == "-" or napeum_full == "알수없음": return "납음오행 정보가 없습니다."
        core_name = napeum_full.split("(")[0] if "(" in napeum_full else napeum_full
        base_desc = NAPEUM_RICH_DESC.get(core_name, "-")
        if pillar_type == "year": return f"{base_desc} 초년과 조상궁에 이 웅장한 파동이 깃들어 있습니다."
        elif pillar_type == "month": return f"{base_desc} 청년기와 사회적 성취(직업)에 이 파동이 핵심적으로 작용합니다."
        elif pillar_type == "day": return f"{base_desc} 중년기와 본인/배우자의 내면 깊은 곳에 이 파동이 흐르고 있습니다."
        else: return f"{base_desc} 말년과 자식궁, 그리고 남모르는 비밀스러운 영혼의 파동입니다."

    napeum_reading = [
        {"pillar": "연주 (초년)", "full": bazi_data["year"]["napeum"], "desc": get_napeum_desc("year", bazi_data["year"]["napeum"])},
        {"pillar": "월주 (청년)", "full": bazi_data["month"]["napeum"], "desc": get_napeum_desc("month", bazi_data["month"]["napeum"])},
        {"pillar": "일주 (중년)", "full": bazi_data["day"]["napeum"], "desc": get_napeum_desc("day", bazi_data["day"]["napeum"])},
    ]
    if not unknown_time:
        napeum_reading.append({"pillar": "시주 (말년)", "full": bazi_data["hour"]["napeum"], "desc": get_napeum_desc("hour", bazi_data["hour"]["napeum"])})

    return {
        "metadata": {
            "origin_kst": astro_res.get("origin_time", ""),
            "true_solar_time": astro_res.get("corrected_time", "") if not unknown_time else "시간 모름 (보정 생략)",
            "is_yaja_applied": astro_res.get("options", {}).get("yaja_applied", False),
            "is_dst_applied": is_dst_applied
        },
        "bazi_data": bazi_data,
        "hidden_stems": hidden_stems,
        "analysis_result": {
            "my_star": my_star, 
            "strength": strength,
            "geokguk": geokguk,
            "yongshin": yongshin_data,
            "mechanics": {
                "gongmang": mech.get_gongmang(d_stem, d_branch),
                "elements_dist": elements_dist,
                "tonggeun": tonggeun,
                "metadata": metadata_dict
            },
            "practical": {"career": career, "health": health_raw},
            "elements_imbalance": elements_imbalance,
            "dynamics": {"special_stars": special_stars, "disasters": disasters},
            "unse": unse_data,
            "napeum_reading": napeum_reading,
            "timeline": {"daewun": daewun_raw, "sewun": sewun_raw},
            "gunghap": gunghap_data,
            "ideal_partner": ideal_partner_data,
            "secret_readings": secret_readings_data,
            "fengshui": fengshui_data,
            "classical": {"reading": classical_reading},
            "gender": "Male" if gender == "M" else "Female",
            "applied_traditional": apply_trad
        }
    }

@app.get("/api/dictionary")
@limiter.limit("30/minute")
def dictionary_endpoint(request: Request, q: str = ""):
    results = dict_db.search(q)
    return results

@app.get("/api/faq")
@limiter.limit("20/minute")
def faq_endpoint(request: Request):
    return FAQ_DB

@app.post("/api/bazi")
@limiter.limit("15/minute")
def bazi_endpoint(request: Request, req: BaziRequest):
    try:
        now_kst = datetime.utcnow() + timedelta(hours=9)
        today_str = now_kst.strftime("%Y-%m-%d")
        cache_key = get_cache_key(req.dict(), today_str)
        
        if cache_key in BAZI_CACHE:
            logger.info("🔥 Bazi Cache Hit! CPU 연산 생략.")
            return BAZI_CACHE[cache_key]

        try:
            longitude = float(req.longitude) if req.longitude else 127.0
        except ValueError:
            longitude = 127.0
            
        try:
            dt_input = datetime.strptime(req.datetime_str, "%Y-%m-%d %H:%M")
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=f"날짜 형식이 올바르지 않습니다: {str(ve)}")
        
        if dt_input.year <= 1582:
            raise HTTPException(status_code=400, detail="1582년 10월 이전의 날짜는 연산이 불가능합니다.")
        
        if req.timezone != 9:
            dt_kst_base = dt_input - timedelta(hours=req.timezone) + timedelta(hours=9)
        else:
            dt_kst_base = dt_input
            
        dt_kst, is_dst_applied = adjust_korean_dst(dt_kst_base)
        
        cal = KoreanLunarCalendar()
        if req.calendar_type.value in ["lunar", "lunar_leap"]:
            is_leap = (req.calendar_type.value == "lunar_leap")
            if cal.setLunarDate(dt_kst.year, dt_kst.month, dt_kst.day, is_leap):
                dt_kst = datetime(cal.solarYear, cal.solarMonth, cal.solarDay, dt_kst.hour, dt_kst.minute)
            else:
                raise HTTPException(status_code=400, detail="유효하지 않은 음력 날짜입니다.")
        else:
            cal.setSolarDate(dt_kst.year, dt_kst.month, dt_kst.day)

        real_lunar_m = cal.lunarMonth
        real_lunar_d = cal.lunarDay
            
        astro_res = astro.calculate_bazi(
            dt_kst, req.gender.value, longitude, 
            apply_true_solar=False if req.unknown_time else req.apply_true_solar, 
            apply_yaja=req.apply_yaja
        )
        
        partner_info = None
        if req.partner_datetime_str:
            try:
                p_lon = float(req.partner_longitude) if req.partner_longitude else 127.0
            except ValueError:
                p_lon = 127.0

            p_dt_input = datetime.strptime(req.partner_datetime_str, "%Y-%m-%d %H:%M")
            if p_dt_input.year <= 1582:
                raise HTTPException(status_code=400, detail="파트너의 생년월일이 1582년 이전이므로 연산이 불가능합니다.")

            if req.partner_timezone != 9:
                p_dt_kst_base = p_dt_input - timedelta(hours=req.partner_timezone) + timedelta(hours=9)
            else:
                p_dt_kst_base = p_dt_input
                
            p_dt_kst, _ = adjust_korean_dst(p_dt_kst_base)
                
            if req.partner_calendar_type.value in ["lunar", "lunar_leap"]:
                p_cal = KoreanLunarCalendar()
                p_is_leap = (req.partner_calendar_type.value == "lunar_leap")
                if p_cal.setLunarDate(p_dt_kst.year, p_dt_kst.month, p_dt_kst.day, p_is_leap):
                    partner_dt = datetime(p_cal.solarYear, p_cal.solarMonth, p_cal.solarDay, p_dt_kst.hour, p_dt_kst.minute)
                else:
                    partner_dt = p_dt_kst
            else:
                partner_dt = p_dt_kst
                
            temp_cal = KoreanLunarCalendar()
            temp_cal.setSolarDate(partner_dt.year, partner_dt.month, partner_dt.day)
            p_lunar_month = temp_cal.lunarMonth
                
            partner_info = {
                "dt": partner_dt, 
                "gender": req.partner_gender.value if req.partner_gender else None, 
                "longitude": p_lon, 
                "unknown_time": req.partner_unknown_time,
                "lunar_month": p_lunar_month
            }

        final_result = build_bridge_response(
            dt_kst, astro_res, req.gender.value, req.daewun_num, partner_info, 
            req.apply_traditional_lunar, req.lunar_month, req.unknown_time, 
            real_lunar_m, real_lunar_d, is_dst_applied
        )

        BAZI_CACHE[cache_key] = final_result
        return final_result

    except HTTPException as http_exc:
        logger.warning(f"Validation Error: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Backend Server Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="서버 내부 연산 중 예기치 않은 오류가 발생했습니다.")

@app.post("/api/calendar")
@limiter.limit("5/minute")
def calendar_endpoint(request: Request, req: CalendarRequest):
    try:
        now_kst = datetime.utcnow() + timedelta(hours=9)
        today_str = now_kst.strftime("%Y-%m-%d")
        
        cache_seed = req.dict()
        cache_key = get_cache_key(cache_seed, today_str + f"_{req.target_year}_{req.target_month}")
        
        if cache_key in CALENDAR_CACHE:
            logger.info("📅 Calendar Cache Hit! 한 달 치 궤도 연산 생략.")
            return CALENDAR_CACHE[cache_key]

        try:
            longitude = float(req.longitude) if req.longitude else 127.0
        except ValueError:
            longitude = 127.0
            
        try:
            dt_input = datetime.strptime(req.datetime_str, "%Y-%m-%d %H:%M")
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=f"날짜 형식이 올바르지 않습니다: {str(ve)}")
        
        if dt_input.year <= 1582:
            raise HTTPException(status_code=400, detail="1582년 이전은 연산할 수 없습니다.")
        
        if req.timezone != 9:
            dt_kst_base = dt_input - timedelta(hours=req.timezone) + timedelta(hours=9)
        else:
            dt_kst_base = dt_input
            
        dt_kst, _ = adjust_korean_dst(dt_kst_base)
        
        cal = KoreanLunarCalendar()
        if req.calendar_type.value in ["lunar", "lunar_leap"]:
            is_leap = (req.calendar_type.value == "lunar_leap")
            if cal.setLunarDate(dt_kst.year, dt_kst.month, dt_kst.day, is_leap):
                dt_kst = datetime(cal.solarYear, cal.solarMonth, cal.solarDay, dt_kst.hour, dt_kst.minute)
            else:
                raise HTTPException(status_code=400, detail="유효하지 않은 음력 날짜입니다.")
        else:
            cal.setSolarDate(dt_kst.year, dt_kst.month, dt_kst.day)
            
        astro_res = astro.calculate_bazi(
            dt_kst, req.gender.value, longitude, 
            apply_true_solar=False if req.unknown_time else req.apply_true_solar, 
            apply_yaja=req.apply_yaja
        )
        
        bazi_raw = astro_res.get("bazi", {})
        y_stem, y_branch = bazi_raw.get("year_pillar", ["-", "-"])[0], bazi_raw.get("year_pillar", ["-", "-"])[1]
        m_stem, m_branch = bazi_raw.get("month_pillar", ["-", "-"])[0], bazi_raw.get("month_pillar", ["-", "-"])[1]
        d_stem, d_branch = bazi_raw.get("day_pillar", ["-", "-"])[0], bazi_raw.get("day_pillar", ["-", "-"])[1]
        day_master = d_stem
        
        if req.unknown_time:
            h_stem, h_branch = "-", "-"
        else:
            h_stem, h_branch = bazi_raw.get("hour_pillar", ["-", "-"])[0], bazi_raw.get("hour_pillar", ["-", "-"])[1]

        def get_tg(stem_or_branch):
            if stem_or_branch == "-": return "-"
            try:
                return mech.get_ten_god(day_master, stem_or_branch)
            except Exception:
                return "-"

        bazi_for_engine = {
            "year": {"stem": y_stem, "branch": y_branch, "stem_tg": get_tg(y_stem), "branch_tg": get_tg(y_branch)},
            "month": {"stem": m_stem, "branch": m_branch, "stem_tg": get_tg(m_stem), "branch_tg": get_tg(m_branch)},
            "day": {"stem": d_stem, "branch": d_branch, "stem_tg": "일간", "branch_tg": get_tg(d_branch)},
            "hour": {"stem": h_stem, "branch": h_branch, "stem_tg": get_tg(h_stem), "branch_tg": get_tg(h_branch)}
        }
        
        try:
            strength = yong.determine_strength(bazi_for_engine)
            yongshin_data = yong.determine_yongshin(bazi_for_engine, strength)
            y_str = str(yongshin_data.get("yongshin", ""))
            h_str = str(yongshin_data.get("huishin", ""))
            g_str = str(yongshin_data.get("gishin", ""))
        except Exception:
            y_str, h_str, g_str = "", "", ""

        days_in_month = calendar.monthrange(req.target_year, req.target_month)[1]
        days_array = []

        for day in range(1, days_in_month + 1):
            try:
                target_dt = datetime(req.target_year, req.target_month, day, 12, 0)
                daily_astro = astro.calculate_bazi(target_dt, req.gender.value)
                
                iljin_stem = daily_astro.get("bazi", {}).get("day_pillar", ["-", "-"])[0]
                iljin_branch = daily_astro.get("bazi", {}).get("day_pillar", ["-", "-"])[1]
                iljin_full = f"{iljin_stem}{iljin_branch}"
                
                iljin_tg = get_tg(iljin_branch)
                branch_elem = unse._get_element(iljin_branch) if hasattr(unse, '_get_element') else ""
                
                status = "평(平)"
                advice = "평온하고 무난한 하루입니다. 특별한 정곡 없이 일상을 유지하십시오."
                
                if branch_elem in y_str or branch_elem in h_str or iljin_tg in y_str or iljin_tg in h_str:
                    status = "길(吉)"
                    advice = "수호신의 기운이 돕는 길일입니다. 중요한 계약이나 만남을 추진하기에 매우 좋습니다."
                elif branch_elem in g_str or iljin_tg in g_str:
                    status = "흉(凶)"
                    advice = "기운이 탁해지고 판단력이 흐려지는 날입니다. 중요한 결정은 미루고 수성하십시오."

                days_array.append({
                    "date": target_dt.strftime("%Y-%m-%d"),
                    "iljin": iljin_full,
                    "iljin_tg": iljin_tg,
                    "status": status,
                    "advice": advice
                })
            except Exception:
                continue

        final_calendar_result = {
            "user_info": {
                "day_master": day_master,
                "yongshin": y_str,
                "gishin": g_str
            },
            "calendar_data": {
                "year": req.target_year,
                "month": req.target_month,
                "days": days_array
            }
        }

        CALENDAR_CACHE[cache_key] = final_calendar_result
        return final_calendar_result

    except HTTPException as http_exc:
        logger.warning(f"Validation Error: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Calendar Engine Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="캘린더 연산 중 예기치 않은 오류가 발생했습니다.")    

@app.get("/")
@limiter.limit("100/minute")
def read_root(request: Request):
    return {"message": "마스터 브릿지 API 가동 중 (Phase 5: Safely Restored and Ultimate Bulletproof)"}