from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from core_astro import CoreAstroEngine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = CoreAstroEngine()

JIJANGGAN = {
    '子': ['壬', '癸'], '丑': ['癸', '辛', '己'], '寅': ['戊', '丙', '甲'], '卯': ['甲', '乙'],
    '辰': ['乙', '癸', '戊'], '巳': ['戊', '庚', '丙'], '午': ['丙', '己', '丁'], '未': ['丁', '乙', '己'],
    '申': ['戊', '壬', '庚'], '酉': ['庚', '辛'], '戌': ['辛', '丁', '戊'], '亥': ['戊', '甲', '壬']
}

def format_bazi_data(engine_result):
    bazi_raw = engine_result.get("bazi", {})
    
    def split_pillar(pillar_str):
        if not pillar_str or len(pillar_str) < 2:
            stem, branch_char, stems = "", "", []
        else:
            stem = pillar_str[0]
            branch_char = pillar_str[1]
            stems = JIJANGGAN.get(branch_char, [])
        
        base = {"stem": stem, "branch": branch_char, "hidden_stems": stems}
        # 🚨 프론트엔드가 객체 안의 객체(.pillar.hidden_stems)를 찾을 때를 대비한 2중 방어막!
        base["pillar"] = {"stem": stem, "branch": branch_char, "hidden_stems": stems}
        base["ganji"] = {"stem": stem, "branch": branch_char, "hidden_stems": stems}
        return base

    y = split_pillar(bazi_raw.get("year_pillar"))
    m = split_pillar(bazi_raw.get("month_pillar"))
    d = split_pillar(bazi_raw.get("day_pillar"))
    h = split_pillar(bazi_raw.get("hour_pillar"))

    # 텅 빈 가짜 객체(Dummy)에도 동일한 2중 방어막 적용
    dummy = split_pillar("")
    dummy_list = [dummy] * 20

    all_pillars = {
        "year": y, "month": m, "day": d, "hour": h, "time": h, "date": d,
        "year_pillar": y, "month_pillar": m, "day_pillar": d, "hour_pillar": h,
        "yearPillar": y, "monthPillar": m, "dayPillar": d, "hourPillar": h,
        "nyeon": y, "wol": m, "il": d, "si": h,
        "daewun": dummy_list, "sewun": dummy_list, "wolun": dummy_list, "timeline": dummy_list,
        "pillars": [y, m, d, h]
    }

    formatted = {
        "bazi": all_pillars,
        "origin_time": engine_result.get("origin_time"),
        "corrected_time": engine_result.get("corrected_time"),
        "gender": engine_result.get("gender")
    }
    
    formatted.update(all_pillars)
    return formatted

@app.post("/api/bazi")
async def bazi_endpoint(request: Request):
    try:
        user_data = await request.json()
        
        datetime_str = user_data.get("datetime_str")
        gender = user_data.get("gender")
        longitude = user_data.get("longitude", 127.0)
        apply_true_solar = user_data.get("apply_true_solar", True)
        apply_yaja = user_data.get("apply_yaja", True)
        
        dt_kst = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        
        raw_result = engine.calculate_bazi(
            dt_kst=dt_kst,
            gender=gender,
            longitude=longitude,
            apply_true_solar=apply_true_solar,
            apply_yaja=apply_yaja
        )
        final_result = format_bazi_data(raw_result)
        
        partner_datetime_str = user_data.get("partner_datetime_str")
        if partner_datetime_str:
            partner_gender = user_data.get("partner_gender")
            partner_dt_kst = datetime.strptime(partner_datetime_str, "%Y-%m-%d %H:%M")
            
            raw_partner_result = engine.calculate_bazi(
                dt_kst=partner_dt_kst,
                gender=partner_gender,
                longitude=longitude,
                apply_true_solar=apply_true_solar,
                apply_yaja=apply_yaja
            )
            final_result["partner"] = format_bazi_data(raw_partner_result)

        return final_result

    except Exception as e:
        print("Backend Error:", str(e), flush=True)
        return {"status": "error", "message": str(e)}

@app.get("/")
def read_root():
    return {"message": "Backend is successfully running!"}