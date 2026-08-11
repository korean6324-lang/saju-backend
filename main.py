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
            return {"stem": "", "branch": "", "hidden_stems": []}
        branch_char = pillar_str[1]
        return {
            "stem": pillar_str[0], 
            "branch": branch_char,
            "hidden_stems": JIJANGGAN.get(branch_char, [])
        }

    # 4개의 기둥을 예쁘게 분리
    year_data = split_pillar(bazi_raw.get("year_pillar"))
    month_data = split_pillar(bazi_raw.get("month_pillar"))
    day_data = split_pillar(bazi_raw.get("day_pillar"))
    hour_data = split_pillar(bazi_raw.get("hour_pillar"))
    dummy = {"stem": "", "branch": "", "hidden_stems": []}

    formatted = {
        # 🚨 프론트엔드가 어떤 이름으로 부르든 다 대답할 수 있도록 모든 이름을 등록해둡니다!
        "bazi": {
            "year": year_data,
            "month": month_data,
            "day": day_data,
            "hour": hour_data,
            "time": hour_data,
            "year_pillar": year_data,
            "month_pillar": month_data,
            "day_pillar": day_data,
            "hour_pillar": hour_data,
            "time_pillar": hour_data,
            "daewun": dummy # 혹시 대운(daewun)을 찾을 경우를 대비한 빈 서랍
        },
        "origin_time": engine_result.get("origin_time"),
        "corrected_time": engine_result.get("corrected_time"),
        "gender": engine_result.get("gender")
    }
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