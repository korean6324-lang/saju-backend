# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Any

from core_astro import core_astro_service
from core_mechanics import core_mechanics_service
from logic_dynamics import logic_dynamics_service
from logic_fengshui import logic_fengshui_service
from db_dictionary import db_dictionary_service

app = FastAPI(title="초정밀 사주·풍수명리 B2B 백엔드 엔진")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserBirthInput(BaseModel):
    birth_dt: datetime = Field(..., description="생년월일시 (KST 기준)")
    gender: str = Field(..., description="성별 ('M' 또는 'F')")
    is_lunar: bool = Field(default=False, description="음력 여부")
    is_leap_month: bool = Field(default=False, description="윤달 여부")

class FengShuiMatchInput(BaseModel):
    my_birth_year: int = Field(..., description="본인의 출생 연도 (입춘 기준)")
    my_gender: str = Field(..., description="본인 성별 ('M' 또는 'F')")
    target_gua: int = Field(..., description="상대방의 본명궁 번호 (1~9)")

@app.post("/api/v1/engine/full-analysis")
async def get_full_analysis(user_info: UserBirthInput) -> Dict[str, Any]:
    try:
        # [Step 1] 원국 추출
        bazi = core_astro_service.calculate_bazi(user_info.birth_dt, user_info.is_lunar, user_info.is_leap_month)
        pillars_list = [bazi["year_pillar"], bazi["month_pillar"], bazi["day_pillar"], bazi["hour_pillar"]]
        stems = [p[0] for p in pillars_list]
        branches = [p[1] for p in pillars_list]
        
        # [Step 2] 십성, 12운성, 통근 분석
        pillar_analysis = core_mechanics_service.analyze_pillars_full(stems, branches)
        tonggeun_data = core_mechanics_service.analyze_tonggeun(stems, branches)
        
        # [Step 3] 역동성 및 신살 스캔 (★ 가짜 데이터 삭제, 실시간 스캔 적용)
        heoja_list = logic_dynamics_service.scan_heoja_gonghyeop(branches)
        clash_data = logic_dynamics_service.analyze_clash(branches)
        detected_shinsals = logic_dynamics_service.scan_special_shinsal(pillars_list)
        
        # [Step 4] 풍수 본명궁 도출
        bonmyeonggung = logic_fengshui_service.calculate_bonmyeonggung(user_info.birth_dt.year, user_info.gender)
        
        # [Step 5] 전문가 처방 DB 매핑 (★ 스캔된 진짜 신살만 처방)
        prescription_data = db_dictionary_service.diagnose_salsal(detected_shinsals)
        
        return {
            "status": "success",
            "request_timestamp": datetime.now().isoformat(),
            "data": {
                "bazi_pillars": bazi,
                "mechanics": {
                    "pillar_analysis": pillar_analysis,
                    "tonggeun": tonggeun_data,
                    "heoja_gonghyeop": heoja_list,
                    "clash_analysis": clash_data
                },
                "fengshui_profile": bonmyeonggung,
                "expert_prescription": prescription_data
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"엔진 연산 에러: {str(e)}")

@app.post("/api/v1/fengshui/match")
async def get_fengshui_match(match_info: FengShuiMatchInput) -> Dict[str, Any]:
    my_profile = logic_fengshui_service.calculate_bonmyeonggung(match_info.my_birth_year, match_info.my_gender)
    match_result = logic_fengshui_service.evaluate_match_and_direction(my_profile["gua_number"], match_info.target_gua)
    return {"my_profile": my_profile, "target_gua": match_info.target_gua, "match_analysis": match_result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)