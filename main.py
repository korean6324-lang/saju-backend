from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from korean_lunar_calendar import KoreanLunarCalendar 

# ==========================================
# 🌟 모든 엔진 총동원 (10개의 심장)
# ==========================================
from core_astro import CoreAstroEngine
from core_mechanics import MechanicsEngine
from dictionary import DictionaryEngine
from logic_dynamics import DynamicsEngine
from logic_fengshui import FengShuiEngine
from logic_gunghap import GunghapEngine
from logic_practical import PracticalEngine
from logic_unse import UnseEngine
from logic_yongshin import YongshinEngine
from logic_classical import ClassicalEngine 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
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

def build_full_response(dt_kst, astro_res, gender, daewun_num=1, partner_info=None, apply_trad=False, lunar_m=None, unknown_time=False):
    bazi_raw = astro_res.get("bazi", {})
    
    y_stem, y_branch = bazi_raw["year_pillar"][0], bazi_raw["year_pillar"][1]
    m_stem, m_branch = bazi_raw["month_pillar"][0], bazi_raw["month_pillar"][1]
    d_stem, d_branch = bazi_raw["day_pillar"][0], bazi_raw["day_pillar"][1]
    
    if unknown_time:
        h_stem, h_branch = "-", "-"
    else:
        h_stem, h_branch = bazi_raw["hour_pillar"][0], bazi_raw["hour_pillar"][1]
    
    if apply_trad and lunar_m:
        trad_m_stem, trad_m_branch = mech.get_traditional_month_pillar(y_stem, lunar_m)
        if trad_m_stem and trad_m_branch:
            m_stem, m_branch = trad_m_stem, trad_m_branch

    day_master = d_stem

    def get_pillar(stem, branch):
        if stem == "-" or branch == "-":
            return {"stem": "-", "branch": "-", "stem_tg": "-", "branch_tg": "-", "napeum": "-"}
        return {
            "stem": stem, "branch": branch,
            "stem_tg": mech.get_ten_god(day_master, stem),
            "branch_tg": mech.get_ten_god(day_master, branch),
            "napeum": mech.get_napeum(stem, branch)
        }

    bazi = {
        "year": get_pillar(y_stem, y_branch),
        "month": get_pillar(m_stem, m_branch),
        "day": get_pillar(d_stem, d_branch),
        "hour": get_pillar(h_stem, h_branch)
    }

    hidden_stems = {
        "year": mech.get_hidden_stems(y_branch), 
        "month": mech.get_hidden_stems(m_branch),
        "day": mech.get_hidden_stems(d_branch), 
        "hour": {"initial": ["-"], "middle": ["-"], "main": ["-"]} if unknown_time else mech.get_hidden_stems(h_branch)
    }
    
    gongmang = mech.get_gongmang(d_stem, d_branch)
    
    valid_stems = [s for s in [y_stem, m_stem, d_stem, h_stem] if s != "-"]
    valid_branches = [b for b in [y_branch, m_branch, d_branch, h_branch] if b != "-"]
    
    elements_dist = mech.get_five_elements_distribution(valid_stems, valid_branches)
    
    tonggeun_branches = {"year": y_branch, "month": m_branch, "day": d_branch}
    if not unknown_time:
        tonggeun_branches["hour"] = h_branch
    tonggeun = mech.check_tonggeun(day_master, tonggeun_branches)

    geokguk = yong.determine_geokguk(bazi, hidden_stems)
    strength = yong.determine_strength(bazi)
    yongshin_data = yong.determine_yongshin(bazi, strength)

    career = prac.analyze_career(geokguk, yongshin_data)
    health_raw = prac.analyze_health(elements_dist)
    
    elements_imbalance = []
    for h in health_raw:
        if h["element"] != "종합":
            elements_imbalance.append({
                "element": h["element"],
                "type": h["status"].split(" ")[0],
                "count": elements_dist.get(h["element"], 0),
                "desc": h["advice"]
            })

    special_stars = dyn.scan_special_stars(
        {"year": y_stem, "month": m_stem, "day": d_stem, "hour": h_stem},
        {"year": y_branch, "month": m_branch, "day": d_branch, "hour": h_branch}
    )
    disasters = dyn.scan_disasters(valid_branches)

    daewun_raw = mech.get_daewun_sequence(gender, y_stem, m_stem, m_branch, int(daewun_num), 10)
    sewun_raw = mech.get_sewun_sequence(datetime.now().year - 4, 10)

    for dw in daewun_raw["timeline"]:
        dw["stem_tg"] = mech.get_ten_god(day_master, dw["stem"])
        dw["branch_tg"] = mech.get_ten_god(day_master, dw["branch"])
    
    for sw in sewun_raw:
        sw["stem_tg"] = mech.get_ten_god(day_master, sw["stem"])
        sw["branch_tg"] = mech.get_ten_god(day_master, sw["branch"])

    now_astro = astro.calculate_bazi(datetime.now(), gender)
    now_y, now_y_b = now_astro["bazi"]["year_pillar"][0], now_astro["bazi"]["year_pillar"][1]
    now_m, now_m_b = now_astro["bazi"]["month_pillar"][0], now_astro["bazi"]["month_pillar"][1]
    now_d, now_d_b = now_astro["bazi"]["day_pillar"][0], now_astro["bazi"]["day_pillar"][1]

    unse_data = {
        "year": {
            **unse.analyze_sewun(bazi, now_y_b, mech.get_ten_god(day_master, now_y_b), yongshin_data),
            "stem": now_y, "branch": now_y_b
        },
        "month": {
            "month_num": datetime.now().month, "stem": now_m, "branch": now_m_b,
            "data": unse.analyze_wolgeon(bazi, now_m_b, mech.get_ten_god(day_master, now_m_b), yongshin_data)
        },
        "day": {
            "day_num": datetime.now().day, "stem": now_d, "branch": now_d_b,
            "data": unse.analyze_iljin(bazi, now_d_b, mech.get_ten_god(day_master, now_d_b), yongshin_data)
        }
    }

    # 🚨 [글로벌 파트너 엔진 가동]
    gunghap_data = None
    if partner_info:
        p_dt = partner_info["dt"]
        p_gender = partner_info["gender"]
        p_lon = partner_info["longitude"]
        p_unk_time = partner_info["unknown_time"]
        
        my_year = dt_kst.year
        p_year = p_dt.year
        
        # 파트너 시간 모름 체크 시 진태양시 보정(균시차) 생략
        p_apply_true_solar = False if p_unk_time else True
        
        p_astro = astro.calculate_bazi(p_dt, p_gender, p_lon, p_apply_true_solar, True)
        p_day_branch = p_astro["bazi"]["day_pillar"][1]

        my_star = ghap.get_bonmyeongseong(my_year, gender)
        p_star = ghap.get_bonmyeongseong(p_year, p_gender)
        
        # 🚨 남녀(Gender) 인자 100% 매칭: 남극녀/여극남의 팩트폭행 도출
        gunghap_data = {
            "my_samwon": ghap.get_samwon_gapja(my_year),
            "my_star": my_star,
            "partner_samwon": ghap.get_samwon_gapja(p_year),
            "partner_star": p_star,
            "gugung": ghap.get_gugung_compatibility(my_star["number"], gender, p_star["number"], p_gender),
            "inner": ghap.get_inner_compatibility(d_branch, p_day_branch)
        }

    classical_stars_branches = {"year": y_branch, "month": m_branch, "day": d_branch}
    if not unknown_time:
        classical_stars_branches["hour"] = h_branch
        
    classical_stars = clas.get_four_pillars_stars(classical_stars_branches)
    
    # 🚨 본인의 성별(Gender) 인자 완벽하게 전달 (배우자궁, 자식궁 남녀 분리 해석)
    classical_reading = clas.generate_classical_reading(bazi, disasters, yongshin_data, gender)

    metadata = {}
    terms_to_fetch = set([
        "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸",
        "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥",
        "비견", "겁재", "식신", "상관", "편재", "정재", "편관", "정관", "편인", "정인", "공망"
    ])
    for p in bazi.values():
        terms_to_fetch.add(p['stem_tg'])
        terms_to_fetch.add(p['branch_tg'])

    for term in terms_to_fetch:
        if term and term != "일간" and term != "-":
            metadata[term] = mech.get_metadata(term)

    def get_napeum_desc(pillar_type, napeum_full):
        if not napeum_full or napeum_full == "-" or napeum_full == "알수없음":
            return "납음오행 정보가 없습니다."
        core_name = napeum_full[:3]
        base_desc = NAPEUM_RICH_DESC.get(core_name, "신비로운 파동을 지닌 기운입니다.")
        
        if pillar_type == "year":
            return f"{base_desc} 초년과 조상궁에 이 웅장한 파동이 깃들어 있습니다."
        elif pillar_type == "month":
            return f"{base_desc} 청년기와 사회적 성취(직업)에 이 파동이 핵심적으로 작용합니다."
        elif pillar_type == "day":
            return f"{base_desc} 중년기와 본인/배우자의 내면 깊은 곳에 이 파동이 흐르고 있습니다."
        else:
            return f"{base_desc} 말년과 자식궁, 그리고 남모르는 비밀스러운 영혼의 파동입니다."

    napeum_reading = [
        {"pillar": "연주 (초년)", "full": bazi["year"]["napeum"], "desc": get_napeum_desc("year", bazi["year"]["napeum"])},
        {"pillar": "월주 (청년)", "full": bazi["month"]["napeum"], "desc": get_napeum_desc("month", bazi["month"]["napeum"])},
        {"pillar": "일주 (중년)", "full": bazi["day"]["napeum"], "desc": get_napeum_desc("day", bazi["day"]["napeum"])},
    ]
    if not unknown_time:
        napeum_reading.append({"pillar": "시주 (말년)", "full": bazi["hour"]["napeum"], "desc": get_napeum_desc("hour", bazi["hour"]["napeum"])})

    return {
        "origin_time": astro_res["origin_time"],
        "corrected_time": "시간 모름 (보정 생략)" if unknown_time else astro_res["corrected_time"],
        "gender": "Male" if gender == "M" else "Female",
        "applied_traditional": apply_trad,
        "bazi": bazi,
        "mechanics": {
            "hidden_stems": hidden_stems,
            "gongmang": gongmang,
            "elements_dist": elements_dist,
            "tonggeun": tonggeun,
            "metadata": metadata
        },
        "yongshin": {
            "geokguk": geokguk,
            "strength": strength,
            "yongshin": yongshin_data
        },
        "practical": {
            "career": career,
            "health": health_raw
        },
        "elements_imbalance": elements_imbalance,
        "dynamics": {
            "special_stars": special_stars,
            "disasters": disasters
        },
        "unse": unse_data,
        "napeum_reading": napeum_reading,
        "timeline": {
            "daewun": daewun_raw,
            "sewun": sewun_raw
        },
        "gunghap": gunghap_data,
        "classical": {
            "stars": classical_stars,
            "reading": classical_reading
        }
    }


# ==========================================
# 🚀 API 엔드포인트
# ==========================================
@app.get("/api/dictionary")
def dictionary_endpoint(q: str = ""):
    return dict_db.search(q)

@app.post("/api/bazi")
async def bazi_endpoint(request: Request):
    try:
        user_data = await request.json()
        
        datetime_str = user_data.get("datetime_str")
        calendar_type = user_data.get("calendar_type", "solar")
        gender = user_data.get("gender")
        
        longitude = float(user_data.get("longitude", 127.0))
        timezone = int(user_data.get("timezone", 9)) 
        unknown_time = user_data.get("unknown_time", False)
        
        apply_true_solar = False if unknown_time else user_data.get("apply_true_solar", True)
        apply_yaja = user_data.get("apply_yaja", True)
        daewun_num = user_data.get("daewun_num", 1)
        
        apply_trad = user_data.get("apply_traditional_lunar", False)
        lunar_m = user_data.get("lunar_month")
        
        dt_input = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        
        if timezone != 9:
            dt_input = dt_input - timedelta(hours=timezone) + timedelta(hours=9)
        
        if calendar_type in ["lunar", "lunar_leap"]:
            cal = KoreanLunarCalendar()
            is_leap = (calendar_type == "lunar_leap")
            if cal.setLunarDate(dt_input.year, dt_input.month, dt_input.day, is_leap):
                dt_kst = datetime(cal.solarYear, cal.solarMonth, cal.solarDay, dt_input.hour, dt_input.minute)
            else:
                return {"status": "error", "message": "유효하지 않은 음력 날짜입니다."}
        else:
            dt_kst = dt_input
            
        astro_res = astro.calculate_bazi(dt_kst, gender, longitude, apply_true_solar, apply_yaja)
        
        partner_info = None
        p_dt_str = user_data.get("partner_datetime_str")
        
        if p_dt_str:
            p_calendar_type = user_data.get("partner_calendar_type", "solar")
            p_gender = user_data.get("partner_gender")
            p_lon = float(user_data.get("partner_longitude", 127.0))
            p_tz = int(user_data.get("partner_timezone", 9))
            p_unk_time = user_data.get("partner_unknown_time", False)
            
            p_dt_input = datetime.strptime(p_dt_str, "%Y-%m-%d %H:%M")
            
            if p_tz != 9:
                p_dt_input = p_dt_input - timedelta(hours=p_tz) + timedelta(hours=9)
                
            if p_calendar_type in ["lunar", "lunar_leap"]:
                p_cal = KoreanLunarCalendar()
                p_is_leap = (p_calendar_type == "lunar_leap")
                if p_cal.setLunarDate(p_dt_input.year, p_dt_input.month, p_dt_input.day, p_is_leap):
                    partner_dt = datetime(p_cal.solarYear, p_cal.solarMonth, p_cal.solarDay, p_dt_input.hour, p_dt_input.minute)
                else:
                    partner_dt = p_dt_input
            else:
                partner_dt = p_dt_input
                
            partner_info = {
                "dt": partner_dt,
                "gender": p_gender,
                "longitude": p_lon,
                "unknown_time": p_unk_time
            }

        final_result = build_full_response(dt_kst, astro_res, gender, daewun_num, partner_info, apply_trad, lunar_m, unknown_time)

        return final_result

    except Exception as e:
        print("Backend Error:", str(e), flush=True)
        return {"status": "error", "message": str(e)}

@app.get("/")
def read_root():
    return {"message": "마스터 엔진 가동 중 (남녀 분리 팩트폭행 엔진 탑재 완벽 대응)"}