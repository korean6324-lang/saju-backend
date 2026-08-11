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
        
        datetime_str = user_data.get("datetime_str")
        gender = user_data.get("gender")
        longitude = user_data.get("longitude", 127.0)
        apply_true_solar = user_data.get("apply_true_solar", True)
        apply_yaja = user_data.get("apply_yaja", True)
        
        dt_kst = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        
        # 엔진 계산 실행
        result = engine.calculate_bazi(
            dt_kst=dt_kst,
            gender=gender,
            longitude=longitude,
            apply_true_solar=apply_true_solar,
            apply_yaja=apply_yaja
        )
        
        # 🚨 추가된 탐지기: 계산 결과를 Render 로그에 출력합니다!
        print("🔥 엔진 계산 결과 확인 🔥", flush=True)
        print(result, flush=True)
        
        # 파트너 궁합 처리
        partner_datetime_str = user_data.get("partner_datetime_str")
        if partner_datetime_str:
            partner_gender = user_data.get("partner_gender")
            partner_dt_kst = datetime.strptime(partner_datetime_str, "%Y-%m-%d %H:%M")
            
            partner_result = engine.calculate_bazi(
                dt_kst=partner_dt_kst,
                gender=partner_gender,
                longitude=longitude,
                apply_true_solar=apply_true_solar,
                apply_yaja=apply_yaja
            )
            result["partner"] = partner_result

        return result

    except Exception as e:
        print("Backend Error:", str(e), flush=True)
        return {"status": "error", "message": str(e)}

@app.get("/")
def read_root():
    return {"message": "Backend is successfully running!"}