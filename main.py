import calendar
import os
import json
import hashlib
import logging
from enum import Enum
from typing import Optional, Union, Dict, Any, List
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
# 🌟 코어 엔진 Import
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

# 🚨 [V2.0 신규 혼택 엔진 로드]
try:
    from logic_hongtaek import MacroGunghapEngine, TaegilEngine, MicroBaziEngine, IchingOracleEngine, UltimateHongtaekEngine
    macro_eng = MacroGunghapEngine()
    taegil_eng = TaegilEngine()
    micro_eng = MicroBaziEngine()
    iching_eng = IchingOracleEngine()
    hongtaek_engine = UltimateHongtaekEngine(macro_eng, taegil_eng, micro_eng, iching_eng)
    HONGTAEK_AVAILABLE = True
    logging.info("✅ V2.0 Hongtaek Engine Loaded Successfully.")
except ImportError as e:
    HONGTAEK_AVAILABLE = False
    hongtaek_engine = None
    logging.warning(f"⚠️ V2.0 Hongtaek Engine Not Found. Fallback to V1 only. Error: {e}")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Myeongri Master Bridge API", version="4.5.0")

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

# ==========================================
# 1. API Request 스키마 정의
# ==========================================
class BaziRequest(BaseModel):
    datetime_str: str = Field(..., description="YYYY-MM-DD HH:MM 형태의 날짜")
    calendar_type: CalendarTypeEnum = Field(CalendarTypeEnum.solar)
    gender: GenderEnum
    longitude: Union[float, str, None] = 127.0
    timezone: int = 9
    unknown_time: bool = False
    apply_true_solar: bool = True
    apply_yaja: bool = True
    daewun_num: int = 1

class CalendarRequest(BaseModel):
    datetime_str: str
    calendar_type: CalendarTypeEnum = CalendarTypeEnum.solar
    gender: GenderEnum
    longitude: Union[float, str, None] = 127.0
    timezone: int = 9
    unknown_time: bool = False
    apply_true_solar: bool = True
    apply_yaja: bool = True
    target_year: int = Field(default_factory=lambda: (datetime.utcnow() + timedelta(hours=9)).year)
    target_month: int = Field(default_factory=lambda: (datetime.utcnow() + timedelta(hours=9)).month)

# 🚨 [V2.0 신규] 혼택 전용 Request 스키마 독립
class HongtaekRequest(BaseModel):
    m_datetime_str: str = Field(..., description="신랑 생년월일시 (YYYY-MM-DD HH:MM)")
    m_calendar_type: CalendarTypeEnum = CalendarTypeEnum.solar
    m_gender: GenderEnum = GenderEnum.M
    m_longitude: float = 127.0
    m_timezone: int = 9
    m_unknown_time: bool = False
    
    f_datetime_str: str = Field(..., description="신부 생년월일시 (YYYY-MM-DD HH:MM)")
    f_calendar_type: CalendarTypeEnum = CalendarTypeEnum.solar
    f_gender: GenderEnum = GenderEnum.F
    f_longitude: float = 127.0
    f_timezone: int = 9
    f_unknown_time: bool = False
    
    target_wedding_date: Optional[str] = Field(None, description="혼택 스캔용 지정 날짜 (YYYY-MM-DD)")

# ==========================================
# 2. 공통 헬퍼 함수
# ==========================================
def adjust_korean_dst(dt: datetime) -> tuple[datetime, bool]:
    dst_ranges = [
        (datetime(1987, 5, 10, 2), datetime(1987, 10, 11, 3)), 
        (datetime(1988, 5, 8, 2), datetime(1988, 10, 9, 3))
    ]
    for start, end in dst_ranges:
        if start <= dt < end:
            return dt - timedelta(hours=1), True
    return dt, False

def get_time_index(hour: int) -> int:
    return ((hour + 1) // 2) % 12 + 1

def parse_and_adjust_dt(dt_str: str, tz: int, cal_type: str, unk_time: bool) -> tuple[datetime, int, int, bool]:
    try:
        dt_input = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"날짜 형식이 올바르지 않습니다: {str(ve)}")
    
    if dt_input.year <= 1582:
        raise HTTPException(status_code=400, detail="1582년 이전 날짜는 연산이 불가합니다.")
    
    dt_kst_base = dt_input - timedelta(hours=tz) + timedelta(hours=9) if tz != 9 else dt_input
    dt_kst, is_dst = adjust_korean_dst(dt_kst_base)
    
    cal = KoreanLunarCalendar()
    if cal_type in ["lunar", "lunar_leap"]:
        is_leap_req = (cal_type == "lunar_leap")
        if cal.setLunarDate(dt_kst.year, dt_kst.month, dt_kst.day, is_leap_req):
            dt_kst = datetime(cal.solarYear, cal.solarMonth, cal.solarDay, dt_kst.hour, dt_kst.minute)
        else:
            raise HTTPException(status_code=400, detail="유효하지 않은 음력 날짜입니다.")
    else:
        cal.setSolarDate(dt_kst.year, dt_kst.month, dt_kst.day)

    return dt_kst, cal.lunarMonth, cal.lunarDay, is_dst

# ==========================================
# 3. Builder 패턴 적용 (V1 레거시 파이프라인)
# ==========================================
class BaziResponseBuilder:
    def __init__(self, dt_kst, astro_res, gender, unknown_time, daewun_num=1, real_lunar_m=None, real_lunar_d=None, is_dst=False):
        self.dt_kst = dt_kst
        self.astro_res = astro_res
        self.gender = gender
        self.unknown_time = unknown_time
        self.daewun_num = daewun_num
        self.real_lunar_m = real_lunar_m
        self.real_lunar_d = real_lunar_d
        self.is_dst = is_dst
        self.bazi_data = {}
        self.hidden_stems = {}
        self.destiny_data = {}
        self.unse_data = {}
        
        try:
            self.bazi_raw = astro_res.get("bazi", {})
            self.day_master = self.bazi_raw.get("day_pillar", ["-", "-"])[0]
            if self.day_master == "-":
                raise ValueError("일간(Day Master)이 추출되지 않았습니다.")
        except Exception as e:
            logger.error(f"코어 명식 추출 실패: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="명식 기초 데이터 연산에 실패했습니다.")

    def _build_bazi_data(self):
        try:
            y_s, y_b = self.bazi_raw.get("year_pillar", ["-", "-"])
            m_s, m_b = self.bazi_raw.get("month_pillar", ["-", "-"])
            d_s, d_b = self.bazi_raw.get("day_pillar", ["-", "-"])
            h_s, h_b = ("-", "-") if self.unknown_time else self.bazi_raw.get("hour_pillar", ["-", "-"])
            
            def get_tg(stem_or_branch):
                return "-" if stem_or_branch == "-" else mech.get_ten_god(self.day_master, stem_or_branch)

            self.bazi_data = {
                "year": {"stem": y_s, "stem_tg": get_tg(y_s), "branch": y_b, "branch_tg": get_tg(y_b), "napeum": mech.get_napeum(y_s, y_b)},
                "month": {"stem": m_s, "stem_tg": get_tg(m_s), "branch": m_b, "branch_tg": get_tg(m_b), "napeum": mech.get_napeum(m_s, m_b)},
                "day": {"stem": d_s, "stem_tg": "일간", "branch": d_b, "branch_tg": get_tg(d_b), "napeum": mech.get_napeum(d_s, d_b)},
                "hour": {"stem": h_s, "stem_tg": get_tg(h_s), "branch": h_b, "branch_tg": get_tg(h_b), "napeum": mech.get_napeum(h_s, h_b)}
            }
            
            self.bazi_for_engine = {k: {"stem": v["stem"], "branch": v["branch"]} for k, v in self.bazi_data.items()}
            
            self.hidden_stems = {
                "year": mech.get_hidden_stems(y_b), "month": mech.get_hidden_stems(m_b), "day": mech.get_hidden_stems(d_b),
                "hour": {"initial": ["-"], "middle": ["-"], "main": ["-"]} if self.unknown_time else mech.get_hidden_stems(h_b)
            }
        except Exception as e:
            logger.error(f"명식 조립 및 지장간/십성 계산 중 치명적 오류: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="명식 기초 데이터 연산 실패")

    def _analyze_destiny(self):
        try:
            strength = yong.determine_strength(self.bazi_for_engine)
            self.destiny_data['strength'] = strength
            self.destiny_data['geokguk'] = yong.determine_geokguk(self.bazi_for_engine, self.hidden_stems)
            self.destiny_data['yongshin'] = yong.determine_yongshin(self.bazi_for_engine, strength)
        except Exception as e:
            logger.error(f"격국/용신 연산 오류: {e}", exc_info=True)
            self.destiny_data['strength'] = self.destiny_data['geokguk'] = self.destiny_data['yongshin'] = {}

        try:
            valid_stems = [p["stem"] for p in self.bazi_for_engine.values() if p["stem"] != "-"]
            valid_branches = [p["branch"] for p in self.bazi_for_engine.values() if p["branch"] != "-"]
            self.destiny_data['elements_dist'] = mech.get_five_elements_distribution(valid_stems, valid_branches)
            self.destiny_data['career'] = prac.analyze_career(self.destiny_data['geokguk'], self.destiny_data['yongshin'])
            self.destiny_data['health'] = prac.analyze_health(self.destiny_data['elements_dist'], gender=self.gender)
            self.destiny_data['special_stars'] = dyn.scan_special_stars({k:v["stem"] for k,v in self.bazi_for_engine.items()}, {k:v["branch"] for k,v in self.bazi_for_engine.items()})
            self.destiny_data['disasters'] = dyn.scan_disasters(valid_branches)
            
            tonggeun_branches = {"year": valid_branches[0] if len(valid_branches)>0 else "-", "month": valid_branches[1] if len(valid_branches)>1 else "-", "day": valid_branches[2] if len(valid_branches)>2 else "-"}
            if not self.unknown_time and len(valid_branches)>3: tonggeun_branches["hour"] = valid_branches[3]
            self.destiny_data['tonggeun'] = mech.check_tonggeun(self.day_master, tonggeun_branches)
        except Exception as e:
            logger.error(f"오행/신살 연산 오류: {e}", exc_info=True)

    def _analyze_unse_and_timeline(self):
        try:
            now_kst = datetime.utcnow() + timedelta(hours=9)
            now_astro = astro.calculate_bazi(now_kst, self.gender)
            now_y_b, now_m_b, now_d_b = [now_astro.get("bazi", {}).get(p, ["-", "-"])[1] for p in ["year_pillar", "month_pillar", "day_pillar"]]
            
            self.unse_data = {
                "year": {**unse.analyze_sewun(self.bazi_for_engine, now_y_b, mech.get_ten_god(self.day_master, now_y_b), self.destiny_data.get('yongshin',{})), "branch": now_y_b},
                "month": {"month_num": now_kst.month, "branch": now_m_b, "data": unse.analyze_wolgeon(self.bazi_for_engine, now_m_b, mech.get_ten_god(self.day_master, now_m_b), self.destiny_data.get('yongshin',{}))},
                "day": {"day_num": now_kst.day, "branch": now_d_b, "data": unse.analyze_iljin(self.bazi_for_engine, now_d_b, mech.get_ten_god(self.day_master, now_d_b), self.destiny_data.get('yongshin',{}))}
            }
        except Exception as e:
            logger.error(f"실시간 운세 연산 오류: {e}", exc_info=True)
            self.unse_data = None

        try:
            daewun_raw = mech.get_daewun_sequence(self.gender, self.bazi_data["year"]["stem"], self.bazi_data["month"]["stem"], self.bazi_data["month"]["branch"], int(self.daewun_num), 10)
            self.destiny_data['daewun'] = daewun_raw if isinstance(daewun_raw, dict) else {"timeline": daewun_raw}
            self.destiny_data['sewun'] = mech.get_sewun_sequence(datetime.utcnow().year + 5, 10)
            self.destiny_data['secrets'] = sec.get_secrets(self.bazi_for_engine, self.destiny_data['daewun'])
        except Exception as e:
            logger.error(f"대운/세운 연산 오류: {e}", exc_info=True)

    def build(self) -> dict:
        """최종 V1 개인 사주 JSON 조립"""
        logger.info("Starting Bazi pipeline assembly...")
        self._build_bazi_data()
        self._analyze_destiny()
        self._analyze_unse_and_timeline()
        
        my_star = ghap.get_bonmyeongseong(self.dt_kst.year, self.gender)
        try:
            fengshui_honmyeong = feng.calculate_honmyeong_gung(self.dt_kst.year, self.gender)
            fengshui_dirs = feng.get_auspicious_directions(fengshui_honmyeong.get("number", 1))
            fengshui_data = {"honmyeong": fengshui_honmyeong, "directions": fengshui_dirs}
        except Exception as e:
            logger.error(f"풍수 연산 오류: {e}", exc_info=True)
            fengshui_data = None

        return {
            "metadata": {
                "origin_kst": self.astro_res.get("origin_time", ""),
                "true_solar_time": self.astro_res.get("corrected_time", "") if not self.unknown_time else "시간 모름 (보정 생략)",
                "is_dst_applied": self.is_dst
            },
            "bazi_data": self.bazi_data,
            "hidden_stems": self.hidden_stems,
            "analysis_result": {
                "my_star": my_star, 
                "strength": self.destiny_data.get('strength', {}),
                "geokguk": self.destiny_data.get('geokguk', {}),
                "yongshin": self.destiny_data.get('yongshin', {}),
                "mechanics": {
                    "gongmang": mech.get_gongmang(self.day_master, self.bazi_data["day"]["branch"]),
                    "elements_dist": self.destiny_data.get('elements_dist', {}),
                    "tonggeun": self.destiny_data.get('tonggeun')
                },
                "practical": {"career": self.destiny_data.get('career',{}), "health": self.destiny_data.get('health',[])},
                "dynamics": {"special_stars": self.destiny_data.get('special_stars',[]), "disasters": self.destiny_data.get('disasters',[])},
                "unse": self.unse_data,
                "timeline": {"daewun": self.destiny_data.get('daewun',{}), "sewun": self.destiny_data.get('sewun',[])},
                "secret_readings": self.destiny_data.get('secrets'),
                "fengshui": fengshui_data,
                "ideal_partner": ghap.get_ideal_partner(self.bazi_for_engine, self.destiny_data.get('yongshin',{}), my_star.get("number",1), self.gender)
            }
        }

# ==========================================
# 4. 엔드포인트 라우팅
# ==========================================

# 🚨 [V2.0 전용 독립 엔드포인트 신설]
@app.post("/api/hongtaek")
@limiter.limit("15/minute")
def hongtaek_endpoint(request: Request, req: HongtaekRequest):
    """
    V1 레거시에 얽매이지 않고, 순수한 ExplainableNode를 포함한 
    UltimateHongtaekResponse 객체를 100% 직렬화하여 반환합니다.
    """
    if not HONGTAEK_AVAILABLE or hongtaek_engine is None:
        logger.error("V2.0 혼택 엔진 모듈 로드 실패")
        raise HTTPException(status_code=503, detail="V2.0 혼택 엔진이 오프라인 상태입니다.")

    try:
        m_dt_kst, _, _, _ = parse_and_adjust_dt(req.m_datetime_str, req.m_timezone, req.m_calendar_type.value, req.m_unknown_time)
        f_dt_kst, _, _, _ = parse_and_adjust_dt(req.f_datetime_str, req.f_timezone, req.f_calendar_type.value, req.f_unknown_time)
        
        m_astro = astro.calculate_bazi(m_dt_kst, req.m_gender.value, req.m_longitude, not req.m_unknown_time)
        f_astro = astro.calculate_bazi(f_dt_kst, req.f_gender.value, req.f_longitude, not req.f_unknown_time)
        
        target_branch = None
        if req.target_wedding_date:
            try:
                tw_dt = datetime.strptime(req.target_wedding_date, "%Y-%m-%d")
                tw_astro = astro.calculate_bazi(tw_dt, "M") 
                target_branch = tw_astro.get("bazi", {}).get("day_pillar", ["-", "-"])[1]
            except Exception as e:
                logger.error(f"택일 날짜 파싱 실패: {e}", exc_info=True)

        m_data = {
            "year": m_dt_kst.year, "month": m_dt_kst.month, "day": m_dt_kst.day,
            "time_index": get_time_index(m_dt_kst.hour) if not req.m_unknown_time else 1,
            "branch": m_astro.get("bazi", {}).get("year_pillar", ["-", "-"])[1],
            "day_pillar": {"간": m_astro.get("bazi", {}).get("day_pillar", ["-", "-"])[0], "지": m_astro.get("bazi", {}).get("day_pillar", ["-", "-"])[1]}
        }
        f_data = {
            "year": f_dt_kst.year, "month": f_dt_kst.month, "day": f_dt_kst.day,
            "time_index": get_time_index(f_dt_kst.hour) if not req.f_unknown_time else 1,
            "branch": f_astro.get("bazi", {}).get("year_pillar", ["-", "-"])[1],
            "day_pillar": {"간": f_astro.get("bazi", {}).get("day_pillar", ["-", "-"])[0], "지": f_astro.get("bazi", {}).get("day_pillar", ["-", "-"])[1]}
        }

        # V2.0 룰 엔진 가동
        report_obj = hongtaek_engine.generate_full_report(m_data, f_data, target_branch)
        
        # Data Contract 손실 없이 Pydantic 100% 직렬화 반환
        return report_obj.model_dump() if hasattr(report_obj, 'model_dump') else report_obj.dict()

    except Exception as e:
        logger.error(f"혼택 파이프라인 치명적 오류: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="혼택 엔진 연산 중 시스템 오류가 발생했습니다.")


@app.post("/api/bazi")
@limiter.limit("15/minute")
def bazi_endpoint(request: Request, req: BaziRequest):
    """개인 사주 조회 (V1 레거시 통합 파이프라인)"""
    try:
        now_kst = datetime.utcnow() + timedelta(hours=9)
        cache_key = get_cache_key(req.dict(), now_kst.strftime("%Y-%m-%d"))
        if cache_key in BAZI_CACHE: 
            return BAZI_CACHE[cache_key]

        dt_kst, real_lunar_m, real_lunar_d, is_dst = parse_and_adjust_dt(req.datetime_str, req.timezone, req.calendar_type.value, req.unknown_time)
        
        try:
            astro_res = astro.calculate_bazi(dt_kst, req.gender.value, float(req.longitude) if req.longitude else 127.0, not req.unknown_time, req.apply_yaja)
        except Exception as e:
            logger.error(f"Core Astro Engine Error: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="사주 명식 코어 연산 중 오류가 발생했습니다.")
        
        # Builder를 통한 개인 파이프라인 조립
        builder = BaziResponseBuilder(dt_kst, astro_res, req.gender.value, req.unknown_time, req.daewun_num, real_lunar_m, real_lunar_d, is_dst)
        final_result = builder.build()

        BAZI_CACHE[cache_key] = final_result
        return final_result

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"Backend Server Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="서버 내부 연산 중 예기치 않은 오류가 발생했습니다.")

@app.post("/api/calendar")
@limiter.limit("5/minute")
def calendar_endpoint(request: Request, req: CalendarRequest):
    try:
        now_kst = datetime.utcnow() + timedelta(hours=9)
        cache_key = get_cache_key(req.dict(), now_kst.strftime("%Y-%m-%d") + f"_{req.target_year}_{req.target_month}")
        if cache_key in CALENDAR_CACHE: return CALENDAR_CACHE[cache_key]

        dt_kst, _, _, _ = parse_and_adjust_dt(req.datetime_str, req.timezone, req.calendar_type.value, req.unknown_time)
            
        astro_res = astro.calculate_bazi(dt_kst, req.gender.value, 127.0, apply_true_solar=False, apply_yaja=True)
        bazi_raw = astro_res.get("bazi", {})
        day_master = bazi_raw.get("day_pillar", ["-", "-"])[0]
        
        y_str, h_str, g_str = "", "", ""
        try:
            bazi_for_engine = {"year": {"stem": bazi_raw.get("year_pillar", ["-", "-"])[0], "branch": bazi_raw.get("year_pillar", ["-", "-"])[1]},
                               "month": {"stem": bazi_raw.get("month_pillar", ["-", "-"])[0], "branch": bazi_raw.get("month_pillar", ["-", "-"])[1]},
                               "day": {"stem": day_master, "branch": bazi_raw.get("day_pillar", ["-", "-"])[1]},
                               "hour": {"stem": bazi_raw.get("hour_pillar", ["-", "-"])[0], "branch": bazi_raw.get("hour_pillar", ["-", "-"])[1]}}
            strength = yong.determine_strength(bazi_for_engine)
            yongshin_data = yong.determine_yongshin(bazi_for_engine, strength)
            y_str, h_str, g_str = str(yongshin_data.get("yongshin", "")), str(yongshin_data.get("huishin", "")), str(yongshin_data.get("gishin", ""))
        except Exception as e: 
            logger.error(f"Calendar yongshin error: {e}", exc_info=True)

        days_in_month = calendar.monthrange(req.target_year, req.target_month)[1]
        days_array = []

        for day in range(1, days_in_month + 1):
            try:
                target_dt = datetime(req.target_year, req.target_month, day, 12, 0)
                daily_astro = astro.calculate_bazi(target_dt, req.gender.value)
                iljin_branch = daily_astro.get("bazi", {}).get("day_pillar", ["-", "-"])[1]
                iljin_tg = mech.get_ten_god(day_master, iljin_branch)
                
                status, advice = "평(平)", "평온하고 무난한 하루입니다."
                if iljin_tg in y_str or iljin_tg in h_str: status, advice = "길(吉)", "수호신의 기운이 돕는 길일입니다."
                elif iljin_tg in g_str: status, advice = "흉(凶)", "기운이 탁해지고 판단력이 흐려지는 날입니다."

                days_array.append({
                    "date": target_dt.strftime("%Y-%m-%d"),
                    "iljin": f"{daily_astro.get('bazi', {}).get('day_pillar', ['-', '-'])[0]}{iljin_branch}",
                    "iljin_tg": iljin_tg,
                    "status": status, "advice": advice
                })
            except Exception as e:
                logger.error(f"Calendar daily iteration error: {e}", exc_info=True)
                continue

        final_calendar_result = {"user_info": {"day_master": day_master, "yongshin": y_str, "gishin": g_str}, "calendar_data": {"year": req.target_year, "month": req.target_month, "days": days_array}}
        CALENDAR_CACHE[cache_key] = final_calendar_result
        return final_calendar_result

    except HTTPException as http_exc: raise http_exc
    except Exception as e:
        logger.error(f"Calendar Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="캘린더 연산 중 오류가 발생했습니다.")    

@app.get("/api/dictionary")
@limiter.limit("30/minute")
def dictionary_endpoint(request: Request, q: str = ""):
    return dict_db.search(q)

@app.get("/api/faq")
@limiter.limit("20/minute")
def faq_endpoint(request: Request):
    return FAQ_DB

@app.get("/")
@limiter.limit("100/minute")
def read_root(request: Request):
    return {"message": "Myeongri Master Bridge API (V4.5 Refactored & Decoupled with V2.0 Hongtaek)"}