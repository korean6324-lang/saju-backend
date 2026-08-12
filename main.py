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

    y = split_pillar(bazi_raw.get("year_pillar"))
    m = split_pillar(bazi_raw.get("month_pillar"))
    d = split_pillar(bazi_raw.get("day_pillar"))
    h = split_pillar(bazi_raw.get("hour_pillar"))

    # 🚨 핵심: 프론트엔드가 강제로 몇 번을 꺼내든 절대 에러가 나지 않도록
    # 텅 빈 가짜 기둥(Dummy)을 20개 생성해서 배열을 꽉꽉 채워줍니다!
    dummy_pillar = {"stem": "", "branch": "", "hidden_stems": []}
    dummy_list = [dummy_pillar] * 20

    all_pillars = {
        "year": y, "month": m, "day": d, "hour": h, "time": h,
        "year_pillar": y, "month_pillar": m, "day_pillar": d, "hour_pillar": h,
        
        # 가짜 기둥 20개가 들어있는 배열 투척
        "daewun": dummy_list, 
        "sewun": dummy_list, 
        "wolun": dummy_list, 
        "timeline": dummy_list,
        
        # 혹시 4기둥 전체를 배열로 요구할 경우를 대비한 세트
        "pillars": [y, m, d, h]
    }

    formatted = {
        "bazi": all_pillars,
        "origin_time": engine_result.get("origin_time"),
        "corrected_time": engine_result.get("corrected_time"),
        "gender": engine_result.get("gender")
    }
    
    # 최상단에도 동일하게 복사
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
        
        # 파트너 데이터가 있을 경우에도 똑같이 가짜 기둥 20개 세트를 줍니다.
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