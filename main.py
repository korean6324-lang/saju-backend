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

@app.post("/api/bazi")
async def bazi_endpoint(request: Request):
    try:
        user_data = await request.json()
        
        # 1. 본인 데이터 변수
        datetime_str = user_data.get("datetime_str")
        gender = user_data.get("gender")
        longitude = user_data.get("longitude", 127.0)
        apply_true_solar = user_data.get("apply_true_solar", True)
        apply_yaja = user_data.get("apply_yaja", True)
        
        # 2. 본인 사주 계산
        dt_kst = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        result = engine.calculate_bazi(
            dt_kst=dt_kst,
            gender=gender,
            longitude=longitude,
            apply_true_solar=apply_true_solar,
            apply_yaja=apply_yaja
        )
        
        # 3. 파트너 궁합 데이터가 있는지 확인하고, 있으면 파트너 사주도 계산!
        partner_datetime_str = user_data.get("partner_datetime_str")
        if partner_datetime_str:
            partner_gender = user_data.get("partner_gender")
            partner_dt_kst = datetime.strptime(partner_datetime_str, "%Y-%m-%d %H:%M")
            
            # 파트너 사주 계산 (동일한 환경 변수 적용)
            partner_result = engine.calculate_bazi(
                dt_kst=partner_dt_kst,
                gender=partner_gender,
                longitude=longitude,
                apply_true_solar=apply_true_solar,
                apply_yaja=apply_yaja
            )
            
            # 🚨 프론트엔드가 파트너 데이터를 찾을 수 있도록 "partner"라는 방에 넣어줍니다.
            result["partner"] = partner_result

        return result

    except Exception as e:
        print("Backend Error:", str(e), flush=True)
        return {"status": "error", "message": str(e)}

@app.get("/")
def read_root():
    return {"message": "Backend is successfully running!"}