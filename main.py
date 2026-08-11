from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# 명리 엔진 불러오기
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

@app.post("/api/bazi")
async def bazi_endpoint(request: Request):
    try:
        # 1. 프론트엔드에서 보낸 JSON 데이터 받기
        user_data = await request.json()
        
        # 2. 정확한 Key 이름으로 데이터 뽑아내기
        datetime_str = user_data.get("datetime_str")         # 예: "1946-12-07 04:30"
        gender = user_data.get("gender")                     # 예: "M"
        longitude = user_data.get("longitude", 127.0)        # 예: 127
        apply_true_solar = user_data.get("apply_true_solar", True)
        apply_yaja = user_data.get("apply_yaja", True)
        
        # 3. 날짜 문자열("YYYY-MM-DD HH:MM")을 파이썬 datetime 객체로 안전하게 변환
        dt_kst = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        
        # 4. 엔진에 데이터 넣고 계산하기!
        result = engine.calculate_bazi(
            dt_kst=dt_kst,
            gender=gender,
            longitude=longitude,
            apply_true_solar=apply_true_solar,
            apply_yaja=apply_yaja
        )
        
        # 5. 계산된 결과를 프론트엔드에 응답
        return result

    except Exception as e:
        # 백엔드 로그 확인을 위한 에러 출력
        print("Backend Error:", str(e), flush=True)
        return {"status": "error", "message": str(e)}

@app.get("/")
def read_root():
    return {"message": "Backend is successfully running!"}