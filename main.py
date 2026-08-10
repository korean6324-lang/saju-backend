# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Any, Optional

# --- MSA 내부 모듈 임포트 ---
# (앞서 Phase 1~5에서 개발된 싱글톤 인스턴스들을 끌어옵니다)
from core_astro import core_astro_service
from core_mechanics import core_mechanics_service
from logic_dynamics import logic_dynamics_service
from logic_fengshui import logic_fengshui_service
from db_dictionary import db_dictionary_service

# --- FastAPI 앱 초기화 및 메타데이터 ---
app = FastAPI(
    title="초정밀 사주·풍수명리 B2B 백엔드 엔진",
    description="NASA 천체력 기반 진기(進氣) 보정 및 한문-한글 융합 메타데이터를 제공하는 전문가용 API",
    version="1.0.0"
)

# CORS 설정 (프론트엔드 도메인 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실무 적용 시 실제 B2B 클라이언트 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Request Models ---
class UserBirthInput(BaseModel):
    birth_dt: datetime = Field(..., description="생년월일시 (KST 기준)")
    gender: str = Field(..., description="성별 ('M' 또는 'F')")
    is_lunar: bool = Field(default=False, description="음력 여부")
    is_leap_month: bool = Field(default=False, description="윤달 여부")

class FengShuiMatchInput(BaseModel):
    my_birth_year: int = Field(..., description="본인의 출생 연도 (입춘 기준)")
    my_gender: str = Field(..., description="본인 성별 ('M' 또는 'F')")
    target_gua: int = Field(..., description="상대방의 본명궁 번호 또는 목적지 방위 번호 (1~9)")

# --- API Endpoints ---

@app.post("/api/v1/engine/full-analysis", summary="명리·풍수 풀스택 종합 분석기")
async def get_full_analysis(user_info: UserBirthInput) -> Dict[str, Any]:
    """
    생년월일시 하나로 사주 원국, 통근 강도, 허자, 풍수 본명궁, 흉액 처방까지 
    모든 MSA 모듈을 관통하여 종합 결과를 반환하는 마스터 엔드포인트입니다.
    """
    try:
        # [Step 1] Core Astro: 초정밀 사주 원국 추출 (음력/윤달 변환 및 교접기/진기 특수 보정 포함)
        bazi = core_astro_service.calculate_bazi(
            user_info.birth_dt, 
            user_info.is_lunar, 
            user_info.is_leap_month
        )
        stems = [bazi["year_pillar"][0], bazi["month_pillar"][0], bazi["day_pillar"][0], bazi["hour_pillar"][0]]
        branches = [bazi["year_pillar"][1], bazi["month_pillar"][1], bazi["day_pillar"][1], bazi["hour_pillar"][1]]
        
        # [Step 2] Root & Mechanics: 통근 및 지장간 분석
        tonggeun_data = core_mechanics_service.analyze_tonggeun(stems, branches)
        
        # [Step 3] Advanced Dynamics: 보이지 않는 기운(허자) 및 충(沖) 분석
        heoja_list = logic_dynamics_service.scan_heoja_gonghyeop(branches)
        clash_data = logic_dynamics_service.analyze_clash(branches)
        
        # [Step 4] Feng Shui: 삼원갑자 본명궁 도출
        bonmyeonggung = logic_fengshui_service.calculate_bonmyeonggung(user_info.birth_dt.year, user_info.gender)
        
        # [Step 5] Expert DB: 흉액 직언 및 개운법 (임시로 충(沖) 데이터를 신살로 가정하여 테스트)
        # 실제 환경에서는 별도의 신살 스캐너를 거친 리스트가 주입됩니다.
        mock_sals = ["백호대살", "천라지망"] 
        prescription_data = db_dictionary_service.diagnose_salsal(mock_sals)
        
        # 최종 B2B 반환 JSON 조립
        return {
            "status": "success",
            "request_timestamp": datetime.now().isoformat(),
            "data": {
                "bazi_pillars": bazi,
                "mechanics": {
                    "tonggeun": tonggeun_data,
                    "heoja_gonghyeop": heoja_list,
                    "clash_analysis": clash_data
                },
                "fengshui_profile": bonmyeonggung,
                "expert_prescription": prescription_data
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"엔진 연산 중 치명적 오류 발생: {str(e)}")

@app.post("/api/v1/fengshui/match", summary="구성기학 8대 길흉 궁합 및 방위 연산")
async def get_fengshui_match(match_info: FengShuiMatchInput) -> Dict[str, Any]:
    """본명궁과 특정 방위(또는 타인)의 구궁 크로스매칭을 수행합니다."""
    my_profile = logic_fengshui_service.calculate_bonmyeonggung(
        match_info.my_birth_year, 
        match_info.my_gender
    )
    
    match_result = logic_fengshui_service.evaluate_match_and_direction(
        my_profile["gua_number"], 
        match_info.target_gua
    )
    
    return {
        "my_profile": my_profile,
        "target_gua": match_info.target_gua,
        "match_analysis": match_result
    }

if __name__ == "__main__":
    import uvicorn
    # 로컬 개발 서버 실행: uvicorn main:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)