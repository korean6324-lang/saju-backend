from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from core_astro import CoreAstroEngine

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = CoreAstroEngine()

# 🎁 프론트엔드가 좋아하는 모양으로 데이터를 변환해주는 함수
def format_bazi_data(engine_result):
    bazi = engine_result.get("bazi", {})
    
    # '丙戌' 같은 2글자를 { stem: '丙', branch: '戌' } 로 쪼개는 기능
    def split_pillar(pillar_str):
        if not pillar_str or len(pillar_str) < 2:
            return {"stem": "", "branch": ""}
        return {"stem": pillar_str[0], "branch": pillar_str[1]}

    # 프론트엔드가 찾는 year, month, day, hour 이름으로 덮어씌움
    formatted = {
        "year": split_pillar(bazi.get("year_pillar")),
        "month": split_pillar(bazi.get("month_pillar")),
        "day": split_pillar(bazi.get("day_pillar")),
        "hour": split_pillar(bazi.get("hour_pillar")),
        
        # 엔진에서 나온 다른 정보들도 혹시 모르니 그대로 전달
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
        
        # 1. 본인 사주 계산
        raw_result = engine.calculate_bazi(
            dt_kst=dt_kst,
            gender=gender,
            longitude=longitude,
            apply_true_solar=apply_true_solar,
            apply_yaja=apply_yaja
        )
        
        # 2. 본인 결과 예쁘게 포장하기
        final_result = format_bazi_data(raw_result)
        
        # 3. 파트너(궁합) 데이터가 있으면 똑같이 계산하고 포장하기
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
            # 프론트엔드가 찾을 수 있게 "partner" 방에 넣어줌
            final_result["partner"] = format_bazi_data(raw_partner_result)

        return final_result

    except Exception as e:
        print("Backend Error:", str(e), flush=True)
        return {"status": "error", "message": str(e)}

@app.get("/")
def read_root():
    return {"message": "Backend is successfully running with perfect data format!"}