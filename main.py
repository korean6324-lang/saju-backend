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

# 🚀 [수정됨] 궁합 입력 모델 (상대방 정보 추가)
class FengShuiMatchInput(BaseModel):
    my_birth_year: int = Field(..., description="본인의 출생 연도")
    my_gender: str = Field(..., description="본인 성별 ('M' 또는 'F')")
    partner_birth_year: int = Field(..., description="상대방의 출생 연도")
    partner_gender: str = Field(..., description="상대방 성별 ('M' 또는 'F')")

@app.post("/api/v1/engine/full-analysis")
async def get_full_analysis(user_info: UserBirthInput) -> Dict[str, Any]:
    try:
        bazi = core_astro_service.calculate_bazi(user_info.birth_dt, user_info.is_lunar, user_info.is_leap_month)
        pillars_list = [bazi["year_pillar"], bazi["month_pillar"], bazi["day_pillar"], bazi["hour_pillar"]]
        stems = [p[0] for p in pillars_list]
        branches = [p[1] for p in pillars_list]
        
        pillar_analysis = core_mechanics_service.analyze_pillars_full(stems, branches)
        tonggeun_data = core_mechanics_service.analyze_tonggeun(stems, branches)
        
        heoja_list = logic_dynamics_service.scan_heoja_gonghyeop(branches)
        clash_data = logic_dynamics_service.analyze_clash(branches)
        detected_shinsals = logic_dynamics_service.scan_special_shinsal(pillars_list)
        
        bonmyeonggung = logic_fengshui_service.calculate_bonmyeonggung(user_info.birth_dt.year, user_info.gender)
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

# 🚀 [수정됨] 궁합 정밀 크로스매칭 API
@app.post("/api/v1/fengshui/match")
async def get_fengshui_match(match_info: FengShuiMatchInput) -> Dict[str, Any]:
    # 1. 나의 본명궁 도출
    my_profile = logic_fengshui_service.calculate_bonmyeonggung(match_info.my_birth_year, match_info.my_gender)
    # 2. 상대방의 본명궁 도출
    partner_profile = logic_fengshui_service.calculate_bonmyeonggung(match_info.partner_birth_year, match_info.partner_gender)
    
    # 3. 8대 길흉 궁합 매칭
    match_result = logic_fengshui_service.evaluate_match_and_direction(my_profile["gua_number"], partner_profile["gua_number"])
    
    return {
        "my_profile": my_profile, 
        "partner_profile": partner_profile, 
        "match_analysis": match_result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)