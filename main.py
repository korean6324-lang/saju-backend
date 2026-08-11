from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# 1. core_astro.py에서 CoreAstroEngine 클래스 불러오기
from core_astro import CoreAstroEngine

app = FastAPI()

# 2. CORS 설정 (Vercel 프론트엔드 접속 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. 엔진 객체를 서버 시작 시 한 번만 생성해 둡니다.
engine = CoreAstroEngine()

# 4. 프론트엔드에서 호출하는 API 주소 (POST /api/bazi)
@app.post("/api/bazi")
async def bazi_endpoint(request: Request):
    try:
        # 프론트엔드에서 보낸 JSON 데이터 받기
        user_data = await request.json()
        
        # ⚠️ 프론트엔드에서 넘겨주는 데이터 키(Key) 이름에 맞게 수정이 필요할 수 있습니다.
        # 일단 일반적인 형태로 작성해 두었습니다.
        birth_date_str = user_data.get("birth_date") # 예: "1946-12-07T04:30:00"
        gender_str = user_data.get("gender")         # 예: "남성" 또는 "M"
        
        # 문자열을 파이썬 datetime 객체로 변환
        dt_kst = datetime.fromisoformat(birth_date_str)
        
        # 5. 생성해둔 엔진 객체를 통해 계산 함수 호출!
        # (기본값으로 설정된 longitude, apply_true_solar 등은 생략해도 자동으로 적용됩니다)
        result = engine.calculate_bazi(dt_kst=dt_kst, gender=gender_str)
        
        return result

    except Exception as e:
        return {"status": "error", "message": str(e)}

# Render 환경 헬스체크용 (서버가 켜졌는지 확인하는 용도)
@app.get("/")
def read_root():
    return {"message": "Saju Backend is successfully running with CoreAstroEngine!"}