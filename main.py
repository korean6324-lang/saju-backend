# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Any

# MSA 모듈 임포트
from core_astro import core_astro_service
from core_mechanics import core_mechanics_service
from logic_dynamics import logic_dynamics_service
from logic_fengshui import logic_fengshui_service
from db_dictionary import db_dictionary_service

app = FastAPI(
    title="초정밀 사주·풍수명리 B2B 백엔드 엔진",
    description="NASA 천체력 기반 및 한문-한글 융합 메타데이터를 제공하는 전문가용 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class UserBirthInput(BaseModel):
    birth_dt: datetime = Field(..., description="생년월일시 (KST 기준)")
    gender: str = Field(..., description="성별 ('M' 또는 'F')")
    is_lunar: bool = Field(default=False, description="음력 여부")
    is_leap_month: bool = Field(default=False, description="윤달 여부")

class FengShuiMatchInput(BaseModel):
    my_birth_year: int = Field(..., description="본인의 출생 연도 (입춘 기준)")
    my_gender: str = Field(..., description="본인 성별 ('M' 또는 'F')")
    partner_birth_year: int = Field(..., description="상대방의 출생 연도")
    partner_gender: str = Field(..., description="상대방 성별 ('M' 또는 'F')")

# --- API Endpoints ---

@app.post("/api/v1/engine/full-analysis", summary="명리·풍수 풀스택 종합 분석기")
async def get_full_analysis(user_info: UserBirthInput) -> Dict[str, Any]:
    """모든 MSA 모듈을 관통하여 종합 결과를 반환하는 마스터 엔드포인트"""
    try:
        # [Step 1] Core Astro: 원국 추출
        bazi = core_astro_service.calculate_bazi(
            user_info.birth_dt, 
            user_info.is_lunar, 
            user_info.is_leap_month
        )
        
        pillars_list = [bazi["year_pillar"], bazi["month_pillar"], bazi["day_pillar"], bazi["hour_pillar"]]
        stems = [p[0] for p in pillars_list]
        branches = [p[1] for p in pillars_list]
        
        # [Step 2] Root & Mechanics: 십성, 12운성, 통근 분석
        pillar_analysis = core_mechanics_service.analyze_pillars_full(stems, branches)
        tonggeun_data = core_mechanics_service.analyze_tonggeun(stems, branches)
        
        # [Step 3] Career & Fortune: 격국(직업) 및 조후 용신(개운법) 도출
        gyeok_yong_data = core_mechanics_service.analyze_gyeokguk_and_yongshin(stems, branches)
        
        career_and_fortune = {
            "gyeokguk": {
                "name": gyeok_yong_data["gyeokguk"],
                "description": db_dictionary_service.gyeokguk_db.get(gyeok_yong_data["gyeokguk"], "전문가 심층 분석 필요")
            },
            "yongshin": {
                "element": gyeok_yong_data["yongshin_element"],
                "remedy": db_dictionary_service.yongshin_db.get(gyeok_yong_data["yongshin_element"])
            }
        }
        
        # [Step 4] Advanced Dynamics: 허자, 충, 흉살 스캔
        heoja_list = logic_dynamics_service.scan_heoja_gonghyeop(branches)
        clash_data = logic_dynamics_service.analyze_clash(branches)
        detected_shinsals = logic_dynamics_service.scan_special_shinsal(pillars_list)
        
        # [Step 5] Feng Shui: 삼원갑자 본명궁 도출
        bonmyeonggung = logic_fengshui_service.calculate_bonmyeonggung(user_info.birth_dt.year, user_info.gender)
        
        # [Step 6] Expert DB: 스캔된 흉살에 대한 전문가 처방
        prescription_data = db_dictionary_service.diagnose_salsal(detected_shinsals)
        
        # 최종 B2B JSON 조립
        return {
            "status": "success",
            "request_timestamp": datetime.now().isoformat(),
            "data": {
                "bazi_pillars": bazi,
                "mechanics": {
                    "pillar_analysis": pillar_analysis,
                    "tonggeun": tonggeun_data,
                    "heoja_gonghyeop": heoja_list,
                    "clash_analysis": clash_data,
                    "career_and_fortune": career_and_fortune  # 프론트엔드로 직업/행운 데이터 전송
                },
                "fengshui_profile": bonmyeonggung,
                "expert_prescription": prescription_data
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"엔진 연산 에러: {str(e)}")

@app.post("/api/v1/fengshui/match", summary="구성기학 8대 길흉 궁합 크로스매칭")
async def get_fengshui_match(match_info: FengShuiMatchInput) -> Dict[str, Any]:
    """나와 상대방의 본명궁을 도출하고 8대 길흉 궁합을 계산합니다."""
    my_profile = logic_fengshui_service.calculate_bonmyeonggung(match_info.my_birth_year, match_info.my_gender)
    partner_profile = logic_fengshui_service.calculate_bonmyeonggung(match_info.partner_birth_year, match_info.partner_gender)
    
    match_result = logic_fengshui_service.evaluate_match_and_direction(my_profile["gua_number"], partner_profile["gua_number"])
    
    return {
        "my_profile": my_profile, 
        "partner_profile": partner_profile, 
        "match_analysis": match_result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)