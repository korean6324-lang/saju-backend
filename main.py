from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from korean_lunar_calendar import KoreanLunarCalendar # 🚨 누락되었던 핵심! 음력/양력 변환 모듈

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

# 팩토리(엔진) 인스턴스화
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

def build_full_response(dt_kst, astro_res, gender, daewun_num=1, partner_dt=None, partner_gender=None, apply_trad=False, lunar_m=None):
    bazi_raw = astro_res.get("bazi", {})
    
    y_stem, y_branch = bazi_raw["year_pillar"][0], bazi_raw["year_pillar"][1]
    m_stem, m_branch = bazi_raw["month_pillar"][0], bazi_raw["month_pillar"][1]
    d_stem, d_branch = bazi_raw["day_pillar"][0], bazi_raw["day_pillar"][1]
    h_stem, h_branch = bazi_raw["hour_pillar"][0], bazi_raw["hour_pillar"][1]
    
    # 🚨 고법 둔월법 강제 적용 (복구 완료)
    if apply_trad and lunar_m:
        trad_m_stem, trad_m_branch = mech.get_traditional_month_pillar(y_stem, lunar_m)
        if trad_m_stem and trad_m_branch:
            m_stem, m_branch = trad_m_stem, trad_m_branch

    day_master = d_stem

    # ----------------------------------------------------
    # 1. Bazi & Mechanics
    # ----------------------------------------------------
    def get_pillar(stem, branch):
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
        "year": mech.get_hidden_stems(y_branch), "month": mech.get_hidden_stems(m_branch),
        "day": mech.get_hidden_stems(d_branch), "hour": mech.get_hidden_stems(h_branch)
    }
    gongmang = mech.get_gongmang(d_stem, d_branch)
    elements_dist = mech.get_five_elements_distribution([y_stem, m_stem, d_stem, h_stem], [y_branch, m_branch, d_branch, h_branch])
    tonggeun = mech.check_tonggeun(day_master, {"year": y_branch, "month": m_branch, "day": d_branch, "hour": h_branch})

    # ----------------------------------------------------
    # 2. Yongshin
    # ----------------------------------------------------
    geokguk = yong.determine_geokguk(bazi, hidden_stems)
    strength = yong.determine_strength(bazi)
    yongshin_data = yong.determine_yongshin(bazi, strength)

    # ----------------------------------------------------
    # 3. Practical
    # ----------------------------------------------------
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

    # ----------------------------------------------------
    # 4. Dynamics
    # ----------------------------------------------------
    special_stars = dyn.scan_special_stars(
        {"year": y_stem, "month": m_stem, "day": d_stem, "hour": h_stem},
        {"year": y_branch, "month": m_branch, "day": d_branch, "hour": h_branch}
    )
    disasters = dyn.scan_disasters([y_branch, m_branch, d_branch, h_branch])

    # ----------------------------------------------------
    # 5. Timeline
    # ----------------------------------------------------
    daewun_raw = mech.get_daewun_sequence(gender, y_stem, m_stem, m_branch, int(daewun_num), 10)
    sewun_raw = mech.get_sewun_sequence(datetime.now().year - 4, 10)

    for dw in daewun_raw["timeline"]:
        dw["stem_tg"] = mech.get_ten_god(day_master, dw["stem"])
        dw["branch_tg"] = mech.get_ten_god(day_master, dw["branch"])
    
    for sw in sewun_raw:
        sw["stem_tg"] = mech.get_ten_god(day_master, sw["stem"])
        sw["branch_tg"] = mech.get_ten_god(day_master, sw["branch"])

    # ----------------------------------------------------
    # 6. Unse
    # ----------------------------------------------------
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

    # ----------------------------------------------------
    # 7. Gunghap
    # ----------------------------------------------------
    gunghap_data = None
    if partner_dt and partner_gender:
        my_year = dt_kst.year
        p_year = partner_dt.year
        p_astro = astro.calculate_bazi(partner_dt, partner_gender)
        p_day_branch = p_astro["bazi"]["day_pillar"][1]

        my_star = ghap.get_bonmyeongseong(my_year, gender)
        p_star = ghap.get_bonmyeongseong(p_year, partner_gender)
        
        gunghap_data = {
            "my_samwon": ghap.get_samwon_gapja(my_year),
            "my_star": my_star,
            "partner_samwon": ghap.get_samwon_gapja(p_year),
            "partner_star": p_star,
            "gugung": ghap.get_gugung_compatibility(my_star["number"], p_star["number"]),
            "inner": ghap.get_inner_compatibility(d_branch, p_day_branch)
        }

    # ----------------------------------------------------
    # 8. Classical
    # ----------------------------------------------------
    classical_stars = clas.get_four_pillars_stars({
        "year": y_branch, "month": m_branch, "day": d_branch, "hour": h_branch
    })
    classical_reading = clas.generate_classical_reading(bazi, disasters, yongshin_data)

    # ----------------------------------------------------
    # 9. Metadata
    # ----------------------------------------------------
    metadata = {}
    terms_to_fetch = {y_stem, y_branch, m_stem, m_branch, d_stem, d_branch, h_stem, h_branch}
    for p in bazi.values():
        terms_to_fetch.add(p['stem_tg'])
        terms_to_fetch.add(p['branch_tg'])
    for g in gongmang:
        terms_to_fetch.add(g)

    for term in terms_to_fetch:
        if term and term != "일간" and term != "-":
            metadata[term] = mech.get_metadata(term)
    metadata["공망"] = mech.get_metadata("공망")

    # ----------------------------------------------------
    # 🌟 10. 마스터 JSON 반환
    # ----------------------------------------------------
    return {
        "origin_time": astro_res["origin_time"],
        "corrected_time": astro_res["corrected_time"],
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
        "napeum_reading": [
            {"pillar": "연주", "full": bazi["year"]["napeum"], "desc": "초년과 조상의 파동"},
            {"pillar": "월주", "full": bazi["month"]["napeum"], "desc": "청년과 부모/사회의 파동"},
            {"pillar": "일주", "full": bazi["day"]["napeum"], "desc": "중년과 본인/배우자의 파동"},
            {"pillar": "시주", "full": bazi["hour"]["napeum"], "desc": "말년과 자식/비밀의 파동"}
        ],
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
        calendar_type = user_data.get("calendar_type", "solar") # 🚨 음/양력 식별
        gender = user_data.get("gender")
        longitude = float(user_data.get("longitude", 127.0))
        apply_true_solar = user_data.get("apply_true_solar", True)
        apply_yaja = user_data.get("apply_yaja", True)
        daewun_num = user_data.get("daewun_num", 1)
        
        apply_trad = user_data.get("apply_traditional_lunar", False) # 🚨 고법 둔월법
        lunar_m = user_data.get("lunar_month")
        
        dt_input = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        
        # 🚨 [가장 중요한 핵심] 음력 날짜를 진짜 양력으로 변환!
        if calendar_type in ["lunar", "lunar_leap"]:
            cal = KoreanLunarCalendar()
            is_leap = (calendar_type == "lunar_leap")
            if cal.setLunarDate(dt_input.year, dt_input.month, dt_input.day, is_leap):
                dt_kst = datetime(cal.solarYear, cal.solarMonth, cal.solarDay, dt_input.hour, dt_input.minute)
            else:
                return {"status": "error", "message": "유효하지 않은 음력 날짜입니다."}
        else:
            dt_kst = dt_input
            
        # 완벽하게 변환된 양력 시간으로 천문 엔진 가동 (진태양시 보정 완벽 적용)
        astro_res = astro.calculate_bazi(dt_kst, gender, longitude, apply_true_solar, apply_yaja)
        
        partner_dt = None
        partner_gender = user_data.get("partner_gender")
        p_dt_str = user_data.get("partner_datetime_str")
        p_calendar_type = user_data.get("partner_calendar_type", "solar")
        
        # 파트너 음/양력 변환도 완벽 복구
        if p_dt_str:
            p_dt_input = datetime.strptime(p_dt_str, "%Y-%m-%d %H:%M")
            if p_calendar_type in ["lunar", "lunar_leap"]:
                p_cal = KoreanLunarCalendar()
                p_is_leap = (p_calendar_type == "lunar_leap")
                if p_cal.setLunarDate(p_dt_input.year, p_dt_input.month, p_dt_input.day, p_is_leap):
                    partner_dt = datetime(p_cal.solarYear, p_cal.solarMonth, p_cal.solarDay, p_dt_input.hour, p_dt_input.minute)
                else:
                    partner_dt = p_dt_input
            else:
                partner_dt = p_dt_input

        final_result = build_full_response(dt_kst, astro_res, gender, daewun_num, partner_dt, partner_gender, apply_trad, lunar_m)

        return final_result

    except Exception as e:
        print("Backend Error:", str(e), flush=True)
        return {"status": "error", "message": str(e)}

@app.get("/")
def read_root():
    return {"message": "마스터 엔진 가동 중 (음/양력 변환 및 고법 둔월법 적용 완료)"}