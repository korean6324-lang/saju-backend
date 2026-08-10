import ephem
import datetime
import itertools
import math
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional
from korean_lunar_calendar import KoreanLunarCalendar

# ==========================================
# 1. FastAPI 인스턴스 및 CORS 설정
# ==========================================
app = FastAPI(title="초정밀 사주 명리 API 서버 (진기 당령 법칙 적용 최종본)", version="5.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 2. Pydantic 스키마 (요청/응답 모델)
# ==========================================
class SajuRequest(BaseModel):
    year: int = Field(..., description="태어난 연도")
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    hour: int = Field(0, ge=0, le=23)
    minute: int = Field(0, ge=0, le=59)
    gender: str = Field(..., description="성별 (M 또는 F)")
    is_lunar: bool = Field(False)
    is_leap_month: bool = Field(False)
    is_time_unknown: bool = Field(False) 

class RectifyRequest(BaseModel):
    year: int
    month: int
    day: int
    is_lunar: bool = False
    is_leap_month: bool = False
    q1_trait: str  
    q2_time: str   

class RectifyResponse(BaseModel):
    estimated_hour: int
    estimated_pillar: str
    reason: str

class PillarData(BaseModel):
    ganji: List[str]
    sipseong: List[str]
    jijanggan: List[str] = []
    sinsal: List[str] = []
    shipi: str = ""
    is_gongmang: bool = False

class PillarsResponse(BaseModel):
    년주: PillarData
    월주: PillarData
    일주: PillarData
    시주: PillarData

class DaewunData(BaseModel):
    age: int
    start_date: str
    ganji: List[str]
    sipseong: List[str]
    jijanggan: List[str] = []
    shipi: str = ""
    is_gongmang: bool = False

class SeunData(BaseModel):
    year: int
    age: int
    ganji: List[str]
    sipseong: List[str]
    jijanggan: List[str] = []
    shipi: str = ""
    is_gongmang: bool = False

class WolunData(BaseModel):
    month: int
    ganji: List[str]
    sipseong: List[str]
    jijanggan: List[str]
    shipi: str
    is_gongmang: bool
    is_current: bool

class IljinData(BaseModel):
    date: str
    ganji: List[str]
    sipseong: List[str]
    jijanggan: List[str]
    sinsal: List[str]
    shipi: str
    is_gongmang: bool

class InterpretationData(BaseModel):
    five_elements_desc: str  
    movement_luck: str       
    job_wealth_desc: str     
    lucky_color: str         
    lucky_direction: str     
    lucky_item: str          

class RelationData(BaseModel):
    name: str          
    type: str          
    positions: List[str] 
    description: str   

class GyeokgukData(BaseModel):
    name: str
    description: str

class YongshinData(BaseModel):
    strength: str       
    yong_hee: List[str] 
    gi_gu: List[str]    
    description: str
    special_type: str = "" 
    special_desc: str = "" 

class JohuData(BaseModel):
    yong_hee: List[str]
    description: str

class DynamicRelationData(BaseModel):
    un_type: str
    name: str
    type: str          
    target_pillar: str
    description: str

class SajuResponse(BaseModel):
    pillars: PillarsResponse
    elements_ratio: Dict[str, float]
    daewun: List[DaewunData]
    interpretation: InterpretationData  
    relations: List[RelationData]
    seun: List[SeunData]
    wolun: List[WolunData] 
    iljin: IljinData  
    gyeokguk: GyeokgukData
    yongshin: YongshinData
    johu: JohuData
    dynamic_relations: List[DynamicRelationData]

class PersonSaju(BaseModel):
    year: int
    month: int
    day: int
    hour: int = 12
    minute: int = 0
    gender: str = "M"
    is_lunar: bool = False
    is_leap_month: bool = False
    is_time_unknown: bool = False

class GunghapRequest(BaseModel):
    me: PersonSaju
    partner: PersonSaju

class GunghapResponse(BaseModel):
    score: int
    element_complement: str
    heavenly_desc: str
    earthly_desc: str
    summary: str


# ==========================================
# 3. 사주 명리 계산 엔진 
# ==========================================
CHEONGAN = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
JIJI = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]
GAPJA_60 = [CHEONGAN[i % 10] + JIJI[i % 12] for i in range(60)]

STEM_ELEM = {"갑": "목", "을": "목", "병": "화", "정": "화", "무": "토", "기": "토", "경": "금", "신": "금", "임": "수", "계": "수"}
ELEMENT_CYCLE = ["목", "화", "토", "금", "수"]
STEM_YINYANG = {"갑": "+", "을": "-", "병": "+", "정": "-", "무": "+", "기": "-", "경": "+", "신": "-", "임": "+", "계": "-"}
BRANCH_YINYANG = {"자": "-", "축": "-", "인": "+", "묘": "-", "진": "+", "사": "+", "오": "-", "미": "-", "신": "+", "유": "-", "술": "+", "해": "+"}
BRANCH_ELEM = {"자": "수", "축": "토", "인": "목", "묘": "목", "진": "토", "사": "화", "오": "화", "미": "토", "신": "금", "유": "금", "술": "토", "해": "수"}

JIJANGGAN_DAYS = {
    "자": [("임", 10), ("계", 20)], "축": [("계", 9),  ("신", 3),  ("기", 18)], "인": [("무", 7),  ("병", 7),  ("갑", 16)],
    "묘": [("갑", 10), ("을", 20)], "진": [("을", 9),  ("계", 3),  ("무", 18)], "사": [("무", 7),  ("경", 7),  ("병", 16)],
    "오": [("병", 10), ("기", 9),  ("정", 11)], "미": [("정", 9),  ("을", 3),  ("기", 18)], "신": [("무", 7),  ("임", 7),  ("경", 16)],
    "유": [("경", 10), ("신", 20)], "술": [("신", 9),  ("정", 3),  ("무", 18)], "해": [("무", 7),  ("갑", 7),  ("임", 16)]
}

MONTH_RULES = [
    {"deg": 315, "branch_idx": 2, "y_offset": 0, "m_start": 2}, {"deg": 345, "branch_idx": 3, "y_offset": 0, "m_start": 3},
    {"deg": 15,  "branch_idx": 4, "y_offset": 0, "m_start": 4}, {"deg": 45,  "branch_idx": 5, "y_offset": 0, "m_start": 5},
    {"deg": 75,  "branch_idx": 6, "y_offset": 0, "m_start": 6}, {"deg": 105, "branch_idx": 7, "y_offset": 0, "m_start": 7},
    {"deg": 135, "branch_idx": 8, "y_offset": 0, "m_start": 8}, {"deg": 165, "branch_idx": 9, "y_offset": 0, "m_start": 9},
    {"deg": 195, "branch_idx": 10,"y_offset": 0, "m_start": 10}, {"deg": 225, "branch_idx": 11,"y_offset": 0, "m_start": 11},
    {"deg": 255, "branch_idx": 0, "y_offset": 0, "m_start": 12}, {"deg": 285, "branch_idx": 1, "y_offset": 1, "m_start": 1}
]

SAMHAP = [{"chars": {"해", "묘", "미"}, "elem": "목"}, {"chars": {"인", "오", "술"}, "elem": "화"}, {"chars": {"사", "유", "축"}, "elem": "금"}, {"chars": {"신", "자", "진"}, "elem": "수"}]
BANGHAP = [{"chars": {"인", "묘", "진"}, "elem": "목"}, {"chars": {"사", "오", "미"}, "elem": "화"}, {"chars": {"신", "유", "술"}, "elem": "금"}, {"chars": {"해", "자", "축"}, "elem": "수"}]
BANHAP = [{"chars": {"해", "묘"}, "elem": "목"}, {"chars": {"묘", "미"}, "elem": "목"}, {"chars": {"인", "오"}, "elem": "화"}, {"chars": {"오", "술"}, "elem": "화"}, {"chars": {"사", "유"}, "elem": "금"}, {"chars": {"유", "축"}, "elem": "금"}, {"chars": {"신", "자"}, "elem": "수"}, {"chars": {"자", "진"}, "elem": "수"}]
CHEONGAN_HAP = {"갑기": "토", "기갑": "토", "을경": "금", "경을": "금", "병신": "수", "신병": "수", "정임": "목", "임정": "목", "무계": "화", "계무": "화"}
HAPHWA_CONDITIONS = {"토": ["진", "술", "축", "미", "오", "사"], "금": ["신", "유", "술", "진", "축"], "수": ["해", "자", "축", "신", "진"], "목": ["인", "묘", "진", "해", "미"], "화": ["사", "오", "미", "인", "술"]}
CHEONGAN_CHUNG = [{"갑", "경"}, {"을", "신"}, {"병", "임"}, {"정", "계"}]
JIJI_YUKHAP = {"자축": "토", "축자": "토", "인해": "목", "해인": "목", "묘술": "화", "술묘": "화", "진유": "금", "유진": "금", "사신": "수", "신사": "수", "오미": "화", "미오": "화"}
JIJI_CHUNG = [{"자", "오"}, {"축", "미"}, {"인", "신"}, {"묘", "유"}, {"진", "술"}, {"사", "해"}]
JIJI_WONJIN = [{"자", "미"}, {"축", "오"}, {"인", "유"}, {"묘", "신"}, {"진", "해"}, {"사", "술"}]
JIJI_HYUNG_PAIRS = [{"인", "사"}, {"사", "신"}, {"인", "신"}, {"축", "술"}, {"술", "미"}, {"축", "미"}, {"자", "묘"}]
JIJI_JAHYUNG = ["진", "오", "유", "해"]
JIJI_GWIMUN = [{"자", "유"}, {"축", "오"}, {"인", "미"}, {"묘", "신"}, {"진", "해"}, {"사", "술"}]
SHIPY_UNSEONG = ["장생", "목욕", "관대", "건록", "제왕", "쇠", "병", "사", "묘", "절", "태", "양"]

def get_sun_longitude_ephem(dt: datetime.datetime) -> float:
    utc_dt = dt - datetime.timedelta(hours=9)
    sun = ephem.Sun()
    sun.compute(utc_dt)
    eq = ephem.Equatorial(sun.a_ra, sun.a_dec, epoch=utc_dt)
    ecl = ephem.Ecliptic(eq)
    return math.degrees(ecl.lon)

def find_jeolgi_time_ephem(target_year: int, target_degree: float, search_start_month: int, search_start_day: int) -> datetime.datetime:
    start_dt = datetime.datetime(target_year, search_start_month, search_start_day, 0, 0, 0)
    left, right = start_dt, start_dt + datetime.timedelta(days=16)
    for _ in range(50):
        mid = left + (right - left) / 2
        diff = get_sun_longitude_ephem(mid) - target_degree
        if diff > 180: diff -= 360
        elif diff < -180: diff += 360
        if diff < 0: left = mid
        else: right = mid
    return (left + (right - left) / 2).replace(microsecond=0)

def get_sipseong(day_stem: str, target_char: str, is_branch: bool = False) -> str:
    if day_stem == "?" or target_char == "?": return "-"
    my_elem, target_elem = STEM_ELEM[day_stem], (BRANCH_ELEM[target_char] if is_branch else STEM_ELEM[target_char])
    diff = (ELEMENT_CYCLE.index(target_elem) - ELEMENT_CYCLE.index(my_elem)) % 5
    is_same_yy = (STEM_YINYANG[day_stem] == (BRANCH_YINYANG[target_char] if is_branch else STEM_YINYANG[target_char]))
    if diff == 0:   return "비견" if is_same_yy else "겁재"
    elif diff == 1: return "식신" if is_same_yy else "상관"
    elif diff == 2: return "편재" if is_same_yy else "정재"
    elif diff == 3: return "편관" if is_same_yy else "정관"
    elif diff == 4: return "편인" if is_same_yy else "정인"

def get_12sinsal(ref_branch: str, target_branch: str) -> str:
    if ref_branch == "?" or target_branch == "?": return "-"
    if ref_branch in ["해", "묘", "미"]: start = "해"
    elif ref_branch in ["인", "오", "술"]: start = "인"
    elif ref_branch in ["사", "유", "축"]: start = "사"
    elif ref_branch in ["신", "자", "진"]: start = "신"
    else: start = "자"
    return ["지살", "년살(도화살)", "월살", "망신살", "장성살", "반안살", "역마살", "육해살", "화개살", "겁살", "재살", "천살"][(JIJI.index(target_branch) - JIJI.index(start)) % 12]

def get_special_sinsal(day_stem: str, branch: str, ganji_str: str) -> List[str]:
    sinsal = []
    if day_stem == "?" or branch == "?": return []
    cheoneul_map = {"갑": ["축", "미"], "무": ["축", "미"], "경": ["축", "미"], "을": ["자", "신"], "기": ["자", "신"], "병": ["해", "유"], "정": ["해", "유"], "신": ["인", "오"], "임": ["묘", "사"], "계": ["묘", "사"]}
    if branch in cheoneul_map.get(day_stem, []): sinsal.append("천을귀인")
    hongyeom_map = {"갑": ["오"], "을": ["오"], "병": ["인"], "정": ["미"], "무": ["진"], "기": ["진"], "경": ["술"], "신": ["유"], "임": ["자"], "계": ["신"]}
    if branch in hongyeom_map.get(day_stem, []): sinsal.append("홍염살")
    if ganji_str in ["갑진", "을미", "병술", "정축", "무진", "임술", "계축"]: sinsal.append("백호대살")
    if ganji_str in ["무술", "경술", "경진", "임진"]: sinsal.append("괴강살")
    return sinsal

def get_shipi_unseong(day_stem: str, target_branch: str) -> str:
    if day_stem == "?" or target_branch == "?": return "-"
    start_idx = JIJI.index({"갑": "해", "을": "오", "병": "인", "정": "유", "무": "인", "기": "유", "경": "사", "신": "자", "임": "신", "계": "묘"}[day_stem])
    target_idx = JIJI.index(target_branch)
    step = (target_idx - start_idx) % 12 if STEM_YINYANG[day_stem] == "+" else (start_idx - target_idx) % 12
    return SHIPY_UNSEONG[step]

def get_gongmang(day_stem: str, day_branch: str) -> List[str]:
    if day_stem == "?" or day_branch == "?": return []
    offset = (JIJI.index(day_branch) - CHEONGAN.index(day_stem)) % 12
    return [JIJI[(offset - 2) % 12], JIJI[(offset - 1) % 12]]

def get_iljin(target_date: datetime.date, user_day_stem: str, user_day_branch: str, gongmang_list: List[str]) -> dict:
    delta_days = (target_date - datetime.date(2000, 1, 1)).days
    stem, branch = CHEONGAN[(4 + delta_days) % 10], JIJI[(6 + delta_days) % 12]
    sinsal_list = [get_12sinsal(user_day_branch, branch)] + get_special_sinsal(user_day_stem, branch, stem + branch) if user_day_branch != "?" else []
    return {"date": target_date.strftime("%Y년 %m월 %d일"), "ganji": [stem, branch], "sipseong": [get_sipseong(user_day_stem, stem, False), get_sipseong(user_day_stem, branch, True)], "jijanggan": [gan[0] for gan in JIJANGGAN_DAYS[branch]], "sinsal": sinsal_list, "shipi": get_shipi_unseong(user_day_stem, branch), "is_gongmang": branch in gongmang_list}


# 🌟 [엔진 핵심 수술 부위] 사주 원국 추출 함수 - 명리학 진기(進氣) 버퍼 적용
def get_saju_pillars(birth_dt, is_time_unknown: bool):
    base_date = datetime.date(2000, 1, 1)
    delta_days = (birth_dt.date() - base_date).days
    day_stem_idx = (4 + delta_days) % 10
    day_branch_idx = (6 + delta_days) % 12
    day_pillar = [CHEONGAN[day_stem_idx], JIJI[day_branch_idx]]
    
    if is_time_unknown:
        time_pillar = ["?", "?"]
    else:
        time_mins = birth_dt.hour * 60 + birth_dt.minute
        time_branch_idx = 0 if time_mins >= 23 * 60 + 30 or time_mins < 1 * 60 + 30 else ((time_mins - 90) // 120 + 1) % 12
        time_stem_idx = (((day_stem_idx % 5) * 2 + time_branch_idx) % 10)
        time_pillar = [CHEONGAN[time_stem_idx], JIJI[time_branch_idx]]
        
    # 🌟 진기(進氣) 임계시간 세팅
    # 36 * 3600초 (약 1.5일): 기운이 교차하는 시점의 특수성을 고려하여, 
    # 천문학적 입절 시간 기준 36시간 전부터 이미 다가오는 새로운 달/해의 기운이 당령한 것으로 간주합니다.
    JIN_GI_SECONDS = 36 * 3600
    effective_birth_dt = birth_dt + datetime.timedelta(seconds=JIN_GI_SECONDS)
    
    ipchun_time = find_jeolgi_time_ephem(birth_dt.year, 315, 2, 1)
    
    # 년주 교차점(입춘) 진기 판별
    if effective_birth_dt >= ipchun_time:
        saju_year = birth_dt.year
    else:
        saju_year = birth_dt.year - 1
        
    year_delta = saju_year - 1984
    
    current_month_idx = 0
    for i, rule in enumerate(MONTH_RULES):
        jeolgi_dt = find_jeolgi_time_ephem(saju_year + rule["y_offset"], rule["deg"], rule["m_start"], 1)
        
        # 월주 교차점(12절기) 진기 정밀 판별
        # 출생 시간에 진기 버퍼를 더한 값(effective_birth_dt)이 입절 시점을 넘겼다면 월주 변경
        if effective_birth_dt >= jeolgi_dt:
            current_month_idx = i
        else:
            break
            
    year_pillar = [CHEONGAN[year_delta % 10], JIJI[year_delta % 12]]
    month_pillar = [CHEONGAN[((year_delta % 10 % 5) * 2 + 2 + current_month_idx) % 10], JIJI[MONTH_RULES[current_month_idx]["branch_idx"]]]
    
    day_stem, day_branch = day_pillar[0], day_pillar[1]
    gongmang_list = get_gongmang(day_stem, day_branch)
    
    def build_pillar_data(stem, branch, is_day=False):
        if stem == "?" or branch == "?": 
            return {"ganji": ["?", "?"], "sipseong": ["-", "-"], "jijanggan": [], "sinsal": [], "shipi": "-", "is_gongmang": False}
        return {
            "ganji": [stem, branch],
            "sipseong": ["일간" if is_day else get_sipseong(day_stem, stem, False), get_sipseong(day_stem, branch, True)],
            "jijanggan": [gan[0] for gan in JIJANGGAN_DAYS[branch]],
            "sinsal": [get_12sinsal(day_branch, branch)] + get_special_sinsal(day_stem, branch, stem + branch), 
            "shipi": get_shipi_unseong(day_stem, branch), "is_gongmang": branch in gongmang_list
        }
    
    return {
        "년주": build_pillar_data(year_pillar[0], year_pillar[1]), 
        "월주": build_pillar_data(month_pillar[0], month_pillar[1]),
        "일주": build_pillar_data(day_pillar[0], day_pillar[1], is_day=True), 
        "시주": build_pillar_data(time_pillar[0], time_pillar[1]),
        "_meta": {"current_month_idx": current_month_idx, "saju_year": saju_year, "gongmang_list": gongmang_list}
    }


def analyze_elements_precision(pillars_dict):
    elements = {"목": 0.0, "화": 0.0, "토": 0.0, "금": 0.0, "수": 0.0}
    for key, pillar_data in pillars_dict.items():
        if key == "_meta" or pillar_data["ganji"][0] == "?": continue
        elements[STEM_ELEM[pillar_data["ganji"][0]]] += 10.0
        for j_stem, days in JIJANGGAN_DAYS[pillar_data["ganji"][1]]: elements[STEM_ELEM[j_stem]] += (30.0 if key == "월주" else 10.0) * (days / 30.0)
    return {k: round(v, 1) for k, v in elements.items()}

def generate_elements_interpretation(elements_ratio: Dict[str, float]) -> str:
    sorted_elements = sorted(elements_ratio.items(), key=lambda x: x[1], reverse=True)
    primary, p_val = sorted_elements[0]
    secondary, s_val = sorted_elements[1]
    traits = {"목": "성장과 추진력, 기획력이 뛰어나며 뻗어나가는 기상이 있습니다.", "화": "열정적이고 예의가 바르며, 자기 표현력과 확산하는 에너지가 강합니다.", "토": "중재와 포용력이 뛰어나며, 흔들림 없는 안정감과 신용을 중시합니다.", "금": "결단력과 원칙을 중시하며, 맺고 끊음이 확실한 기질이 있습니다.", "수": "지혜롭고 유연하며, 상황에 맞게 대처하는 수용성이 뛰어납니다."}
    return f"분석된 원국 내에서 {primary} 기운({p_val}%)과 {secondary} 기운({s_val}%)이 가장 강하게 발현되고 있습니다. 특히 주된 기운인 '{primary}'의 영향으로 {traits[primary]}"

def check_movement_luck(pillars_dict) -> str:
    found_yeokma = [pillars_dict[p]["ganji"][1] for p in ["년주", "월주", "일주", "시주"] if pillars_dict[p]["ganji"][1] in ["인", "신", "사", "해"]]
    if len(found_yeokma) >= 2: return f"사주 지지에 이동과 변화를 상징하는 역마의 글자({', '.join(set(found_yeokma))})가 강하게 자리 잡고 있습니다. 활동 반경이 넓어지는 역동적인 명식입니다."
    elif len(found_yeokma) == 1: return f"사주에 역마의 글자({found_yeokma[0]})가 존재하여, 정체된 환경보다는 적절한 변화가 긍정적인 활력을 줍니다."
    return "원국 자체는 안정을 추구하는 기운이 강하며, 큰 이동수는 대운이나 세운에서 역마나 충(沖)이 들어올 때 발생합니다."

def determine_gyeokguk(day_stem: str, month_branch: str, other_stems: List[str]) -> dict:
    if day_stem == "?" or month_branch == "?": return {"name": "미상", "description": "시간 모름으로 인해 격국을 정확히 판별하기 어렵습니다."}
    jijanggan = JIJANGGAN_DAYS[month_branch]
    target_stem = jijanggan[-1][0] if month_branch in ["자", "오", "묘", "유"] else next((g[0] for g in reversed(jijanggan) if g[0] in other_stems), jijanggan[-1][0])
    gyeok_map = {"비견": {"name": "건록격(建祿格)", "description": "주관이 뚜렷하고 독립심이 강해 자수성가하는 명입니다."}, "겁재": {"name": "양인격(羊刃格)", "description": "강력한 카리스마와 승부욕을 지녔습니다. 불굴의 의지로 난관을 돌파합니다."}, "식신": {"name": "식신격(食神格)", "description": "온화하고 베푸는 성향으로 한 분야를 깊이 파고드는 장인 정신과 창의력이 뛰어납니다."}, "상관": {"name": "상관격(傷官格)", "description": "비상한 두뇌와 뛰어난 언변, 화려한 표현력을 가집니다. 혁신가 기질이 있습니다."}, "편재": {"name": "편재격(偏財格)", "description": "스케일이 크고 사업 수완이 뛰어나며 공간 지각력과 인맥 관리에 능합니다."}, "정재": {"name": "정재격(正財格)", "description": "성실하고 치밀하며 신용을 중시합니다. 안정적인 재물 축적에 능합니다."}, "편관": {"name": "편관격(偏官格)", "description": "강한 인내심과 돌파력, 영웅호걸의 기질을 가집니다. 권력과 명예를 중시합니다."}, "정관": {"name": "정관격(正官格)", "description": "합리적이고 원칙을 중시하며 책임감이 강해 조직 내에서 안정적인 발전을 이룹니다."}, "편인": {"name": "편인격(偏印格)", "description": "비상한 직관력과 독특한 아이디어를 가집니다. 전문 기술, 예술 등에 탁월합니다."}, "정인": {"name": "정인격(正印格)", "description": "학구열이 높고 도덕적이며 수용력이 뛰어납니다. 인자한 성품으로 학문/문서 운이 좋습니다."}}
    return gyeok_map.get(get_sipseong(day_stem, target_stem, is_branch=False), {"name": "알수없음", "description": "격국 산출 불가"})

def determine_yongshin(day_stem: str, elements_ratio: Dict[str, float]) -> dict:
    if day_stem == "?": return {"strength": "-", "yong_hee": [], "gi_gu": [], "description": "시간 미상으로 완벽한 억부용신 산출이 제한됩니다.", "special_type": "", "special_desc": ""}
    my_elem, mother_elem = STEM_ELEM[day_stem], {"목": "수", "화": "목", "토": "화", "금": "토", "수": "금"}[STEM_ELEM[day_stem]]
    my_force = elements_ratio.get(my_elem, 0.0) + elements_ratio.get(mother_elem, 0.0)
    supporting, draining = [my_elem, mother_elem], [e for e in ["목", "화", "토", "금", "수"] if e not in [my_elem, mother_elem]]
    strength, desc = ("신강(身强)", f"일간({my_elem})의 기운이 {round(my_force, 1)}%로 매우 강한 사주입니다.") if my_force > 50.0 else ("신약(身弱)", f"일간({my_elem})의 기운이 {round(my_force, 1)}%로 다소 약한 사주입니다.")
    e1, v1 = sorted(elements_ratio.items(), key=lambda x: x[1], reverse=True)[0]
    e2, v2 = sorted(elements_ratio.items(), key=lambda x: x[1], reverse=True)[1]
    special_type, special_desc = "", ""
    if v1 >= 60.0: special_type, special_desc = "병약용신(病藥用神)", f"사주에 '{e1}' 기운이 {v1}%로 극단적으로 태과하여 병(病)이 되었습니다. 이를 제어하는 '{{'목': '금', '화': '수', '토': '목', '금': '화', '수': '토'}[e1]}' 기운이 절실히 필요합니다."
    elif v1 + v2 >= 75.0 and {e1, e2} in [{"수", "화"}, {"목", "토"}, {"화", "금"}, {"토", "수"}, {"금", "목"}]: 
        special_type, special_desc = "통관용신(通關用神)", f"사주 내에 '{e1}'과 '{e2}'이 상극하며 싸우고 있습니다. 두 기운을 소통시키는 '{{frozenset(['수', '화']): '목', frozenset(['목', '토']): '화', frozenset(['화', '금']): '토', frozenset(['토', '수']): '금', frozenset(['금', '목']): '수'}[frozenset([e1, e2])]}' 기운이 중요합니다."
    return {"strength": strength, "yong_hee": draining if strength == "신강(身强)" else supporting, "gi_gu": supporting if strength == "신강(身强)" else draining, "description": desc, "special_type": special_type, "special_desc": special_desc}

def determine_johu(month_branch: str) -> dict:
    if month_branch == "?": return {"yong_hee": [], "description": "태어난 달을 알 수 없어 조후 용신을 산출할 수 없습니다."}
    if month_branch in ["해", "자", "축"]: return {"yong_hee": ["화", "목"], "description": "한겨울(해/자/축월)에 태어나 몹시 춥습니다. 만물을 녹여줄 따뜻한 '화(火)' 기운이 조후 용신입니다."}
    elif month_branch in ["사", "오", "미"]: return {"yong_hee": ["수", "금"], "description": "한여름(사/오/미월)에 태어나 몹시 덥습니다. 열기를 식혀줄 시원한 '수(水)' 기운이 조후 용신입니다."}
    elif month_branch in ["인", "묘", "진"]: return {"yong_hee": ["화", "수"], "description": "만물이 생동하는 봄(인/묘/진월)에 태어났습니다. 새싹이 자라기 위한 '화(火)'와 '수(水)' 기운이 조화롭게 필요합니다."}
    elif month_branch in ["신", "유", "술"]: return {"yong_hee": ["수", "화"], "description": "서늘한 가을(신/유/술월)에 태어났습니다. 결실을 씻을 '수(水)'와 단련할 '화(火)' 기운이 온도를 맞춰줍니다."}
    return {"yong_hee": [], "description": ""}

def generate_job_wealth_desc(gyeokguk_name: str, elements_ratio: Dict[str, float]) -> str:
    if "건록격" in gyeokguk_name or "양인격" in gyeokguk_name: return "전문직, 독립적인 사업, 혹은 자신의 전문 기술을 활용하는 분야에서 재물을 축적하기 유리합니다. 조직 생활보다는 본인의 주도권이 있는 환경이 좋습니다."
    elif "식신격" in gyeokguk_name or "상관격" in gyeokguk_name: return "창의적인 아이디어, 교육, 예술, 요식업, 말하는 직업 등에서 뛰어난 능력을 발휘합니다. 자신의 재능을 세상에 표현하는 것이 곧 재물로 연결되는 구조입니다."
    elif "정재격" in gyeokguk_name or "편재격" in gyeokguk_name: return "재물 감각이 매우 뛰어납니다. 안정적인 금융, 회계, 부동산 관리부터 스케일이 큰 사업과 무역까지 돈의 흐름을 읽고 창출하는 능력이 탁월합니다."
    elif "정관격" in gyeokguk_name or "편관격" in gyeokguk_name: return "조직 관리, 공직, 대기업, 법조계 등 명예와 권한이 주어지는 곳에서 능력을 인정받습니다. 높은 직위와 명예를 얻으면 재물은 자연스럽게 따라오는 명입니다."
    elif "정인격" in gyeokguk_name or "편인격" in gyeokguk_name: return "문서운과 라이센스(자격증), 지식 기반의 직업군에 유리합니다. 학자, 연구원, 부동산 임대업 등 정신적인 영역이나 특수 자격을 통한 재물 창출이 좋습니다."
    return "사주 원국의 오행 분포를 고루 활용하여 자신만의 길을 개척하는 흐름입니다."

def get_lucky_elements(primary_yongshin: str) -> dict:
    return {"목": {"color": "푸른색, 초록색 계열", "direction": "동쪽", "item": "식물 기르기, 등산, 산책, 나무 소재의 인테리어 소품"}, "화": {"color": "붉은색, 핑크색 계열", "direction": "남쪽", "item": "밝은 조명, 햇볕 쬐기, 심장이 뛰는 유산소 운동, 화려한 악세서리"}, "토": {"color": "노란색, 갈색, 베이지색", "direction": "중앙 (거주지의 중심)", "item": "도자기, 흙이나 흙길 걷기(어싱), 찜질, 안정감 있는 가구 배치"}, "금": {"color": "흰색, 은색, 메탈 컬러", "direction": "서쪽", "item": "금속성 악세서리(시계, 반지), 정리정돈, 웨이트 트레이닝, 거울 활용"}, "수": {"color": "검은색, 짙은 네이비색", "direction": "북쪽", "item": "물가(강/바다) 산책, 수영, 반신욕, 어항이나 가습기 배치"}}.get(primary_yongshin, {"color": "자유로운 배색", "direction": "유연한 방향", "item": "스스로 편안함을 느끼는 취미 생활"})

def add_years(dt: datetime.datetime, years: int) -> datetime.datetime:
    try: return dt.replace(year=dt.year + years)
    except ValueError: return dt.replace(year=dt.year + years, day=28) 

def calculate_daewun(birth_dt, gender, year_stem, month_ganji, day_stem, current_month_idx, saju_year, gongmang_list):
    is_forward = (STEM_YINYANG[year_stem] == "+") == (gender.upper() == "M")
    current_rule, next_rule = MONTH_RULES[current_month_idx], MONTH_RULES[(current_month_idx + 1) % 12]
    prev_jeolgi = find_jeolgi_time_ephem(saju_year + current_rule["y_offset"], current_rule["deg"], current_rule["m_start"], 1)
    next_jeolgi = find_jeolgi_time_ephem(saju_year + next_rule["y_offset"], next_rule["deg"], next_rule["m_start"], 1)
    diff_days = ((next_jeolgi - birth_dt).total_seconds() if is_forward else (birth_dt - prev_jeolgi).total_seconds()) / 86400
    daewun_age, first_gyoun_dt = max(1, round(diff_days / 3.0)), birth_dt + datetime.timedelta(days=diff_days * 121.75)
    month_idx = GAPJA_60.index(month_ganji[0] + month_ganji[1])
    return [{"age": daewun_age + (i - 1) * 10, "start_date": add_years(first_gyoun_dt, (i - 1) * 10).strftime("%Y.%m.%d"), "ganji": list(GAPJA_60[(month_idx + (i if is_forward else -i)) % 60]), "sipseong": [get_sipseong(day_stem, GAPJA_60[(month_idx + (i if is_forward else -i)) % 60][0], False), get_sipseong(day_stem, GAPJA_60[(month_idx + (i if is_forward else -i)) % 60][1], True)], "jijanggan": [gan[0] for gan in JIJANGGAN_DAYS[GAPJA_60[(month_idx + (i if is_forward else -i)) % 60][1]]], "shipi": get_shipi_unseong(day_stem, GAPJA_60[(month_idx + (i if is_forward else -i)) % 60][1]), "is_gongmang": GAPJA_60[(month_idx + (i if is_forward else -i)) % 60][1] in gongmang_list} for i in range(1, 11)]

def calculate_seun(birth_year: int, day_stem: str, start_year: int, count: int, gongmang_list: List[str]) -> List[dict]:
    return [{"year": y, "age": y - birth_year + 1, "ganji": list(GAPJA_60[(y - 4) % 60]), "sipseong": [get_sipseong(day_stem, GAPJA_60[(y - 4) % 60][0], False), get_sipseong(day_stem, GAPJA_60[(y - 4) % 60][1], True)], "jijanggan": [gan[0] for gan in JIJANGGAN_DAYS[GAPJA_60[(y - 4) % 60][1]]], "shipi": get_shipi_unseong(day_stem, GAPJA_60[(y - 4) % 60][1]), "is_gongmang": GAPJA_60[(y - 4) % 60][1] in gongmang_list} for y in range(start_year, start_year + count)]

def analyze_relations(pillars_dict) -> List[dict]:
    relations, positions = [], ["년주", "월주", "일주", "시주"]
    stems, branches = [pillars_dict[p]["ganji"][0] for p in positions], [pillars_dict[p]["ganji"][1] for p in positions]
    found_3hap = set()
    for i, j, k in itertools.combinations(range(4), 3):
        if "?" in (branches[i], branches[j], branches[k]): continue
        subset = {branches[i], branches[j], branches[k]}
        for sh in SAMHAP:
            if subset == sh["chars"]: relations.append({"name": f"{''.join(subset)}삼합", "type": "지지삼합", "positions": [positions[i], positions[j], positions[k]], "description": f"지지에 강력한 {sh['elem']} 기운 국(局) 형성."}); found_3hap.update([i, j, k])
        for bh in BANGHAP:
            if subset == bh["chars"]: relations.append({"name": f"{''.join(subset)}방합", "type": "지지방합", "positions": [positions[i], positions[j], positions[k]], "description": f"같은 계절의 혈연적 {bh['elem']} 기운 결속력."}); found_3hap.update([i, j, k])
    for i, j in itertools.combinations(range(4), 2):
        s1, s2, b1, b2 = stems[i], stems[j], branches[i], branches[j]
        if "?" not in (s1, s2):
            if s1 + s2 in CHEONGAN_HAP: relations.append({"name": f"{s1}{s2}합", "type": "천간합", "positions": [positions[i], positions[j]], "description": f"천간 '{s1}'과 '{s2}' 합."})
            elif {s1, s2} in CHEONGAN_CHUNG: relations.append({"name": f"{s1}{s2}충", "type": "천간충", "positions": [positions[i], positions[j]], "description": f"천간 '{s1}'과 '{s2}' 충돌."})
        if "?" not in (b1, b2):
            if b1 + b2 in JIJI_YUKHAP: relations.append({"name": f"{b1}{b2}합", "type": "지지육합", "positions": [positions[i], positions[j]], "description": f"지지 '{b1}'과 '{b2}' 육합."})
            if {b1, b2} in JIJI_CHUNG: relations.append({"name": f"{b1}{b2}충", "type": "지지충", "positions": [positions[i], positions[j]], "description": f"지지 '{b1}'과 '{b2}' 충돌."})
            if {b1, b2} in JIJI_WONJIN: relations.append({"name": f"{b1}{b2}원진", "type": "지지원진", "positions": [positions[i], positions[j]], "description": f"'{b1}'과 '{b2}' 원진살."})
            if {b1, b2} in JIJI_HYUNG_PAIRS: relations.append({"name": f"{b1}{b2}형", "type": "지지형", "positions": [positions[i], positions[j]], "description": f"'{b1}'과 '{b2}' 형살."})
    return relations

def analyze_dynamic_relations(pillars_dict, daewun_list, seun_list, current_year, iljin_ganji=None, wolun_ganji=None) -> List[dict]:
    relations, positions = [], ["년주", "월주", "일주", "시주"]
    stems, branches = [pillars_dict[p]["ganji"][0] for p in positions], [pillars_dict[p]["ganji"][1] for p in positions]
    current_age = next((s["age"] for s in seun_list if s["year"] == current_year), 1)
    current_daewun = next((d for d in reversed(daewun_list) if d["age"] <= current_age), None)
    current_seun = next((s for s in seun_list if s["year"] == current_year), None)
    
    for un_label, un_ganji in filter(lambda x: x[1], [("현재 대운", current_daewun["ganji"] if current_daewun else None), (f"{current_year}년 세운", current_seun["ganji"] if current_seun else None), ("이달의 월운", wolun_ganji), ("오늘 일진", iljin_ganji)]):
        u_stem, u_branch = un_ganji[0], un_ganji[1]
        for i, j in itertools.combinations(range(4), 2):
            if "?" in (branches[i], branches[j]): continue
            subset = {u_branch, branches[i], branches[j]}
            if len(subset) == 3:
                for sh in SAMHAP:
                    if subset == sh["chars"]: relations.append({"un_type": un_label, "name": f"{''.join(subset)}삼합", "type": "지지삼합", "target_pillar": f"{positions[i]}·{positions[j]}", "description": f"운의 '{u_branch}'이 원국의 '{branches[i]}', '{branches[j]}'와 삼합을 이룹니다."})
        for idx, pos in enumerate(positions):
            p_stem, p_branch = stems[idx], branches[idx]
            if p_stem != "?" and u_stem + p_stem in CHEONGAN_HAP: relations.append({"un_type": un_label, "name": f"{u_stem}{p_stem}합", "type": "천간합", "target_pillar": pos, "description": f"천간 '{u_stem}'과 원국 {pos}의 '{p_stem}' 합."})
            if p_stem != "?" and {u_stem, p_stem} in CHEONGAN_CHUNG: relations.append({"un_type": un_label, "name": f"{u_stem}{p_stem}충", "type": "천간충", "target_pillar": pos, "description": f"천간 '{u_stem}'과 원국 {pos}의 '{p_stem}' 충."})
            if p_branch != "?" and u_branch + p_branch in JIJI_YUKHAP: relations.append({"un_type": un_label, "name": f"{u_branch}{p_branch}합", "type": "지지합", "target_pillar": pos, "description": f"지지 '{u_branch}'과 원국 {pos}의 '{p_branch}' 합."})
            if p_branch != "?" and {u_branch, p_branch} in JIJI_CHUNG: relations.append({"un_type": un_label, "name": f"{u_branch}{p_branch}충", "type": "지지충", "target_pillar": pos, "description": f"지지 '{u_branch}'과 원국 {pos}의 '{p_branch}' 충."})
    return relations

# ==========================================
# 4. API 엔드포인트
# ==========================================

@app.post("/api/rectify_time", response_model=RectifyResponse)
def rectify_time_api(request: RectifyRequest):
    try:
        calc_year, calc_month, calc_day = request.year, request.month, request.day
        if request.is_lunar:
            calendar = KoreanLunarCalendar()
            if not calendar.setLunarDate(request.year, request.month, request.day, request.is_leap_month): raise ValueError("유효하지 않은 음력 날짜입니다.")
            calc_year, calc_month, calc_day = calendar.solarYear, calendar.solarMonth, calendar.solarDay
            
        birth_date = datetime.date(calc_year, calc_month, calc_day)
        day_stem_idx = (4 + (birth_date - datetime.date(2000, 1, 1)).days) % 10
        day_stem = CHEONGAN[day_stem_idx]
        
        target_sipseongs = {"A": ["비견", "겁재"], "B": ["식신", "상관"], "C": ["정재", "편재"], "D": ["정관", "편관"], "E": ["정인", "편인"]}.get(request.q1_trait, [])
        target_branches = {"A": [2, 3, 4], "B": [5, 6, 7], "C": [8, 9, 10], "D": [11, 0, 1]}.get(request.q2_time, [])
        
        best_score, best_branch_idx, best_stem = -1, 0, ""
        for branch_idx in range(12):
            stem = CHEONGAN[(((day_stem_idx % 5) * 2 + branch_idx) % 10)]
            score = (3 if branch_idx in target_branches else 0) + (2 if get_sipseong(day_stem, stem, False) in target_sipseongs else 0) + (1 if get_sipseong(day_stem, JIJI[branch_idx], True) in target_sipseongs else 0)
            if score > best_score: best_score, best_branch_idx, best_stem = score, branch_idx, stem
                
        return RectifyResponse(estimated_hour=[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22][best_branch_idx], estimated_pillar=f"{best_stem}{JIJI[best_branch_idx]}", reason=f"명리학적 역산 결과, '{best_stem}{JIJI[best_branch_idx]}({JIJI[best_branch_idx]}시)'에 태어나셨을 확률이 가장 높습니다.")
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/saju", response_model=SajuResponse)
def calculate_saju_api(request: SajuRequest):
    try:
        calc_year, calc_month, calc_day = request.year, request.month, request.day
        if request.is_lunar:
            calendar = KoreanLunarCalendar()
            if not calendar.setLunarDate(request.year, request.month, request.day, request.is_leap_month): raise ValueError("유효하지 않은 음력 날짜입니다.")
            calc_year, calc_month, calc_day = calendar.solarYear, calendar.solarMonth, calendar.solarDay
        birth_dt = datetime.datetime(calc_year, calc_month, calc_day, request.hour if not request.is_time_unknown else 12, request.minute if not request.is_time_unknown else 0)
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))
    
    try:
        pillars_data = get_saju_pillars(birth_dt, request.is_time_unknown)
        meta, gongmang_list = pillars_data.pop("_meta"), pillars_data["_meta"]["gongmang_list"] if "_meta" in pillars_data else get_gongmang(pillars_data["일주"]["ganji"][0], pillars_data["일주"]["ganji"][1])
        elements_ratio = analyze_elements_precision(pillars_data)
        daewun_list = calculate_daewun(birth_dt, request.gender, pillars_data["년주"]["ganji"][0], pillars_data["월주"]["ganji"], pillars_data["일주"]["ganji"][0], meta["current_month_idx"], meta["saju_year"], gongmang_list)
        current_year = datetime.datetime.now().year
        seun_list = calculate_seun(birth_dt.year, pillars_data["일주"]["ganji"][0], current_year - 2, 10, gongmang_list)
        
        day_stem, day_branch = pillars_data["일주"]["ganji"][0], pillars_data["일주"]["ganji"][1]
        iljin_info = get_iljin(datetime.datetime.now().date(), day_stem, day_branch, gongmang_list)
        
        now_dt = datetime.datetime.now()
        curr_saju_year = current_year if now_dt >= find_jeolgi_time_ephem(current_year, 315, 2, 1) else current_year - 1
        curr_m_idx = next((i for i, r in reversed(list(enumerate(MONTH_RULES))) if now_dt >= find_jeolgi_time_ephem(curr_saju_year + r["y_offset"], r["deg"], r["m_start"], 1)), 0)
        current_wolun_ganji = [CHEONGAN[(((curr_saju_year - 1984) % 10 % 5) * 2 + 2 + curr_m_idx) % 10], JIJI[MONTH_RULES[curr_m_idx]["branch_idx"]]]
        wolun_list = [{"month": m, "ganji": [CHEONGAN[(((curr_saju_year - 1984) % 10 % 5) * 2 + 2 + i) % 10], JIJI[(i + 2) % 12]], "sipseong": [get_sipseong(day_stem, CHEONGAN[(((curr_saju_year - 1984) % 10 % 5) * 2 + 2 + i) % 10], False), get_sipseong(day_stem, JIJI[(i + 2) % 12], True)], "jijanggan": [g[0] for g in JIJANGGAN_DAYS[JIJI[(i + 2) % 12]]], "shipi": get_shipi_unseong(day_stem, JIJI[(i + 2) % 12]), "is_gongmang": JIJI[(i + 2) % 12] in gongmang_list, "is_current": (CHEONGAN[(((curr_saju_year - 1984) % 10 % 5) * 2 + 2 + i) % 10] == current_wolun_ganji[0] and JIJI[(i + 2) % 12] == current_wolun_ganji[1])} for i, m in enumerate([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1])]
        
        gyeokguk_info = determine_gyeokguk(day_stem, pillars_data["월주"]["ganji"][1], [pillars_data["년주"]["ganji"][0], pillars_data["월주"]["ganji"][0]] + ([] if request.is_time_unknown else [pillars_data["시주"]["ganji"][0]]))
        yongshin_info = determine_yongshin(day_stem, elements_ratio)
        johu_info = determine_johu(pillars_data["월주"]["ganji"][1])
        
        primary_yongshin_elem = johu_info["yong_hee"][0] if johu_info["yong_hee"] else (yongshin_info["yong_hee"][0] if yongshin_info["yong_hee"] else None)
        lucky_info = get_lucky_elements(primary_yongshin_elem)

        interpretation_data = InterpretationData(five_elements_desc=generate_elements_interpretation(elements_ratio), movement_luck=check_movement_luck(pillars_data), job_wealth_desc=generate_job_wealth_desc(gyeokguk_info["name"], elements_ratio), lucky_color=lucky_info["color"], lucky_direction=lucky_info["direction"], lucky_item=lucky_info["item"])
        
        return SajuResponse(pillars=pillars_data, elements_ratio=elements_ratio, daewun=daewun_list, interpretation=interpretation_data, relations=analyze_relations(pillars_data), seun=seun_list, wolun=wolun_list, iljin=IljinData(**iljin_info), gyeokguk=GyeokgukData(**gyeokguk_info), yongshin=YongshinData(**yongshin_info), johu=JohuData(**johu_info), dynamic_relations=analyze_dynamic_relations(pillars_data, daewun_list, seun_list, current_year, iljin_info["ganji"], current_wolun_ganji))
    except Exception as e: raise HTTPException(status_code=500, detail=f"서버 내부 연산 오류: {str(e)}")

@app.post("/api/gunghap", response_model=GunghapResponse)
def calculate_gunghap_api(request: GunghapRequest):
    try:
        def get_person_data(person: PersonSaju):
            calc_y, calc_m, calc_d = person.year, person.month, person.day
            if person.is_lunar:
                calendar = KoreanLunarCalendar()
                calendar.setLunarDate(person.year, person.month, person.day, person.is_leap_month)
                calc_y, calc_m, calc_d = calendar.solarYear, calendar.solarMonth, calendar.solarDay
            pillars = get_saju_pillars(datetime.datetime(calc_y, calc_m, calc_d, person.hour if not person.is_time_unknown else 12, person.minute if not person.is_time_unknown else 0), person.is_time_unknown)
            pillars.pop("_meta")
            return {"pillars": pillars, "elements": analyze_elements_precision(pillars), "yongshin": determine_yongshin(pillars["일주"]["ganji"][0], analyze_elements_precision(pillars))}

        me_data, partner_data = get_person_data(request.me), get_person_data(request.partner)
        me_day_stem, me_day_branch = me_data["pillars"]["일주"]["ganji"]
        pt_day_stem, pt_day_branch = partner_data["pillars"]["일주"]["ganji"]

        score = 50 
        me_strongest, pt_strongest = sorted(me_data["elements"].items(), key=lambda x: x[1], reverse=True)[0][0], sorted(partner_data["elements"].items(), key=lambda x: x[1], reverse=True)[0][0]
        
        complement_points = (15 if pt_strongest in me_data["yongshin"]["yong_hee"] else 0) + (15 if me_strongest in partner_data["yongshin"]["yong_hee"] else 0)
        element_desc = "최고의 오행 궁합입니다! 내가 부족한 기운을 상대가 채워주는 '천생연분' 보완 관계입니다." if complement_points == 30 else ("서로의 부족한 기운을 채워주는 좋은 보완 관계입니다." if complement_points == 15 else "두 분의 기운이 서로 비슷하여 공감대가 잘 형성되지만, 보완성은 다소 평범합니다.")
        score += complement_points

        heavenly_desc = "서로의 생각과 가치관이 무난하게 융화됩니다."
        if me_day_stem != "?" and pt_day_stem != "?":
            if me_day_stem + pt_day_stem in CHEONGAN_HAP or pt_day_stem + me_day_stem in CHEONGAN_HAP: score += 15; heavenly_desc = "천간이 합(合)을 이루어 정신적으로 강하게 끌리는 훌륭한 유대감을 가집니다."
            elif {me_day_stem, pt_day_stem} in CHEONGAN_CHUNG: score -= 10; heavenly_desc = "천간이 충(沖)을 이루어 가치관의 대립이 발생할 수 있습니다."
            elif me_day_stem == pt_day_stem: score += 5; heavenly_desc = "서로의 마음을 잘 이해하는 편안함이 있습니다."

        earthly_desc = "현실적인 환경과 일상생활 패턴이 어우러집니다."
        if me_day_branch != "?" and pt_day_branch != "?":
            if me_day_branch + pt_day_branch in JIJI_YUKHAP or pt_day_branch + me_day_branch in JIJI_YUKHAP: score += 20; earthly_desc = "배우자 자리가 육합을 이루어 속궁합이 매우 뛰어난 결속력을 가집니다."
            elif any({me_day_branch, pt_day_branch}.issubset(sh["chars"]) for sh in SAMHAP + BANHAP): score += 15; earthly_desc = "배우자 자리가 방합/삼합으로 엮여 같은 목표를 공유할 때 관계가 돈독해집니다."
            elif {me_day_branch, pt_day_branch} in JIJI_CHUNG: score -= 15; earthly_desc = "배우자 자리가 충(沖)을 이룹니다. 환경적 마찰이 생기기 쉬우니 각자의 영역을 존중해야 합니다."
            elif {me_day_branch, pt_day_branch} in JIJI_WONJIN: score -= 10; earthly_desc = "배우자 자리에 원진살이 작용하여 애증의 끈이 있으니 감정 소모에 유의하세요."

        score = max(0, min(100, score)) 
        summary = "완벽한 찰떡궁합입니다!" if score >= 90 else ("아주 좋은 궁합입니다." if score >= 75 else ("무난하고 평탄한 궁합입니다." if score >= 60 else "노력과 이해가 필요한 궁합입니다."))
        return GunghapResponse(score=score, element_complement=element_desc, heavenly_desc=heavenly_desc, earthly_desc=earthly_desc, summary=summary)
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)