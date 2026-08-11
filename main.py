from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# 1. core_astro.py에서 명리 계산 함수 불러오기
from core_astro import calculate_bazi

app = FastAPI()

# 2. CORS 설정 (Vercel 프론트엔드에서 접속할 수 있도록 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (보안을 위해 나중에 Vercel 주소로 변경해도 됩니다)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. 프론트엔드에서 호출하는 API 주소 (POST /api/bazi)
@app.post("/api/bazi")
async def bazi_endpoint(request: Request):
    try:
        # 프론트엔드에서 보낸 입력 데이터(생년월일 등)를 JSON 형태로 받기
        user_data = await request.json()
        
        # 4. 명리 엔진(core_astro.py)에 데이터 전달 및 계산
        # (만약 calculate_bazi 함수가 딕셔너리를 통째로 받지 않고 개별 변수를 받는다면 수정이 필요할 수 있습니다)
        result = calculate_bazi(user_data)
        
        # 계산된 결과를 프론트엔드로 반환
        return result

    except Exception as e:
        # 에러 발생 시 프론트엔드에서 확인할 수 있도록 에러 메시지 반환
        return {"status": "error", "message": str(e)}

# Render 환경 헬스체크용 (선택 사항)
@app.get("/")
def read_root():
    return {"message": "Saju Backend is running!"}