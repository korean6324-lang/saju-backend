# main.py
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# ==========================================
# 1. 명리/혼택 11대 마스터 엔진 Import
# 🚨 [수정 완료] 알려주신 실제 파일명(core_*)으로 import 경로 변경
# ==========================================
from core_astro import CoreAstroEngine
from core_mechanics import MechanicsEngine
from logic_yongshin import YongshinEngine
from logic_dynamics import DynamicsEngine
from logic_secret import SecretEngine
from logic_classical import ClassicalEngine
from logic_practical import PracticalEngine
from logic_dangsaju import DangsajuEngine
from logic_gunghap import FengShuiHontaekEngine # 풍수+혼택 결합 업그레이드 엔진
from logic_unse import UnseEngine
from dictionary import DictionaryEngine

# ==========================================
# 2. FastAPI 어플리케이션 및 미들웨어 설정
# ==========================================
app = FastAPI(
    title="명리 & 혼택촬요 마스터 API 서버", 
    description="사주, 풍수, 혼택, 운세 종합 분석 오케스트레이터",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 상용화 시 "https://your-frontend-domain.com" 으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 3. 글로벌 엔진 인스턴스화 (Stateless 싱글톤)
# ==========================================
astro_engine = CoreAstroEngine()
mechanics_engine = MechanicsEngine()
yongshin_engine = YongshinEngine()
dynamics_engine = DynamicsEngine()
secret_engine = SecretEngine()
classical_engine = ClassicalEngine()
practical_engine = PracticalEngine()
dangsaju_engine = DangsajuEngine()
hontaek_engine = FengShuiHontaekEngine()
unse_engine = UnseEngine()
dict_engine = DictionaryEngine()

# ==========================================
# 4. Pydantic DTO (Data Transfer Objects) - API 규격
# ==========================================
class UserInfo(BaseModel):
    name: str = Field(..., example="홍길동")
    gender: str = Field(..., pattern="^[MF]$", example="M", description="M: 남성, F: 여성")
    birth_date: str = Field(..., example="1990-05-15 14:30", description="YYYY-MM-DD HH:MM")
    is_lunar: bool = Field(False, description="음력 여부")
    current_age: int = Field(..., example=35)

class SajuRequest(BaseModel):
    user: UserInfo

class GunghapRequest(BaseModel):
    groom: UserInfo
    bride: UserInfo
    target_date: Optional[str] = Field(None, example="2026-10-20 12:00", description="혼례 희망일(택일)")

# ==========================================
# 5. 데이터 브리지 헬퍼 함수 (엔진 간 파이프라인 연결용)
# ==========================================
def _build_formatted_bazi(bazi_chars: dict, day_stem: str) -> dict:
    """AstroEngine의 8글자 텍스트를 다른 엔진들이 읽을 수 있는 표준 Dict로 변환"""
    pillars = ["year", "month", "day", "hour"]
    formatted = {}
    
    for pillar in pillars:
        pillar_chars = bazi_chars.get(f"{pillar}_pillar", "--")
        stem = pillar_chars[0] if len(pillar_chars) == 2 else "-"
        branch = pillar_chars[1] if len(pillar_chars) == 2 else "-"
        
        formatted[pillar] = {
            "stem": stem,
            "branch": branch,
            "stem_tg": mechanics_engine.get_ten_god(day_stem, stem) if stem != "-" else "-",
            "branch_tg": mechanics_engine.get_ten_god(day_stem, branch) if branch != "-" else "-",
            "wunseong": mechanics_engine.get_12wunseong(day_stem, branch) if branch != "-" else "-"
        }
    return formatted

def _get_year_from_date(date_str: str) -> int:
    """날짜 문자열에서 연도(int) 추출"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        return dt.year
    except:
        return 1984 # 파싱 실패 시 기본값 보호

# ==========================================
# 6. API 엔드포인트 라우팅
# ==========================================

@app.post("/api/v1/saju")
async def get_personal_saju(req: SajuRequest):
    """
    [개인 사주 종합 파이프라인] 
    11개 엔진을 순차적으로 통과시키며 종합 명리 분석 JSON을 구성합니다.
    """
    try:
        # [Step 1] 시간 변환 및 8글자 추출 (CoreAstroEngine)
        dt = datetime.strptime(req.user.birth_date, "%Y-%m-%d %H:%M")
        astro_res = astro_engine.calculate_bazi(dt, req.user.gender)
        bazi_chars = astro_res.get("bazi", {})
        
        # [Step 2] 데이터 구조화 및 기초 명리 연산 (MechanicsEngine)
        day_stem = bazi_chars.get("day_pillar", "--")[0]
        formatted_bazi = _build_formatted_bazi(bazi_chars, day_stem)
        
        stems_list = [formatted_bazi[p]["stem"] for p in formatted_bazi]
        branches_list = [formatted_bazi[p]["branch"] for p in formatted_bazi]
        
        element_dist = mechanics_engine.get_five_elements_distribution(stems_list, branches_list)
        hidden_stems = {p: mechanics_engine.get_hidden_stems(formatted_bazi[p]["branch"]) for p in formatted_bazi}
        
        # [Step 3] 강약, 용신, 격국 판별 (YongshinEngine)
        strength_data = yongshin_engine.determine_strength(formatted_bazi)
        yongshin_data = yongshin_engine.determine_yongshin(formatted_bazi, strength_data)
        geokguk_data = yongshin_engine.determine_geokguk(formatted_bazi, hidden_stems)
        
        # [Step 4] 동적 상호작용 및 숨은 흉살 (DynamicsEngine & SecretEngine)
        branches_dict = {p: formatted_bazi[p]["branch"] for p in formatted_bazi}
        stems_dict = {p: formatted_bazi[p]["stem"] for p in formatted_bazi}
        
        special_stars = dynamics_engine.scan_special_stars(stems_dict, branches_dict)
        disasters = dynamics_engine.scan_disasters(branches_list)
        
        # 대운 배열 추출 (천극지충 분석용)
        month_stem = formatted_bazi["month"]["stem"]
        month_branch = formatted_bazi["month"]["branch"]
        daewun_data = mechanics_engine.get_daewun_sequence(req.user.gender, formatted_bazi["year"]["stem"], month_stem, month_branch)
        
        secret_data = secret_engine.get_secrets(formatted_bazi, daewun_data, req.user.current_age)
        
        # [Step 5] 실용 분석 (PracticalEngine) - 직업 및 건강/식이요법
        health_data = practical_engine.analyze_health(element_dist)
        career_data = practical_engine.analyze_career(geokguk_data, yongshin_data)

        # 최종 JSON 조합
        return {
            "status": "success",
            "metadata": {
                "name": req.user.name,
                "gender": "건명(남성)" if req.user.gender == 'M' else "곤명(여성)",
                "corrected_time": astro_res.get("corrected_time")
            },
            "bazi_matrix": formatted_bazi,
            "elements_distribution": element_dist,
            "core_analysis": {
                "strength": strength_data,
                "yongshin": yongshin_data,
                "geokguk": geokguk_data
            },
            "practical_analysis": {
                "health": health_data,
                "career": career_data
            },
            "dynamics_and_secrets": {
                "special_stars": special_stars,
                "disasters": disasters,
                "secrets": secret_data
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"사주 파이프라인 연산 중 오류 발생: {str(e)}")


@app.post("/api/v1/gunghap")
async def get_hontaek_gunghap(req: GunghapRequest):
    """
    [혼택촬요 종합 궁합/택일 파이프라인]
    신랑과 신부의 명식을 대조하고, 혼택촬요 비전을 통해 길흉을 도출합니다.
    """
    try:
        # [Step 1] 신랑/신부 사주 명식 추출
        m_dt = datetime.strptime(req.groom.birth_date, "%Y-%m-%d %H:%M")
        f_dt = datetime.strptime(req.bride.birth_date, "%Y-%m-%d %H:%M")
        
        m_bazi_res = astro_engine.calculate_bazi(m_dt, "M").get("bazi", {})
        f_bazi_res = astro_engine.calculate_bazi(f_dt, "F").get("bazi", {})

        # [Step 2] 혼택촬요 - 동서명합 (대유년법 8유성) 판별
        m_year = _get_year_from_date(req.groom.birth_date)
        f_year = _get_year_from_date(req.bride.birth_date)
        
        dongseo_gunghap = hontaek_engine.evaluate_hontaek_gunghap(m_year, f_year)
        
        # [Step 3] 혼택촬요 - 특수격국 (천지합덕, 교귀격, 교록격) 스캔
        m_day_stem = m_bazi_res.get("day_pillar", "--")[0]
        m_day_branch = m_bazi_res.get("day_pillar", "--")[1]
        f_day_stem = f_bazi_res.get("day_pillar", "--")[0]
        f_day_branch = f_bazi_res.get("day_pillar", "--")[1]
        
        special_gunghap = hontaek_engine.analyze_special_gunghap(
            m_day_stem, m_day_branch, f_day_stem, f_day_branch
        )
        
        # [Step 4] 혼택촬요 - 풍수 방위 개운법 (신랑 가장 기준)
        m_honmyeong = hontaek_engine.calculate_honmyeong_gung(m_year, "M")
        fengshui_dirs = hontaek_engine.get_auspicious_directions(m_honmyeong.get("number", 1))

        # [Step 5] 택일(擇日) 검증 - 입력된 경우 가취길월 및 고진과숙 필터 구동
        taekil_result = None
        if req.target_date:
            t_dt = datetime.strptime(req.target_date, "%Y-%m-%d %H:%M")
            t_bazi = astro_engine.calculate_bazi(t_dt, "M").get("bazi", {})
            t_day_branch = t_bazi.get("day_pillar", "--")[1]
            
            # 신부 띠(연지) 도출
            f_year_branch = f_bazi_res.get("year_pillar", "--")[1]
            m_year_branch = m_bazi_res.get("year_pillar", "--")[1]
            
            # 가취길월 검증
            gachwi_month = hontaek_engine.get_gachwi_gilwol(f_year_branch)
            # 고진과숙 검증
            gojin_gwasuk = hontaek_engine.check_taekil_gojin_gwasuk(m_year_branch, f_year_branch, t_day_branch)
            
            taekil_result = {
                "target_date": req.target_date,
                "gachwi_gilwol_eval": gachwi_month,
                "gojin_gwasuk_filter": gojin_gwasuk
            }

        return {
            "status": "success",
            "hontaek_summary": {
                "dongseo_gunghap": dongseo_gunghap,
                "special_gunghap": special_gunghap
            },
            "fengshui_advice": {
                "base_gung": m_honmyeong,
                "directions": fengshui_dirs
            },
            "taekil_validation": taekil_result if taekil_result else "택일 희망일이 입력되지 않았습니다."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"궁합/혼택 연산 중 오류 발생: {str(e)}")


@app.get("/api/v1/dictionary")
async def search_dictionary(query: str, category: Optional[str] = None):
    """
    [백과사전 검색 API]
    """
    try:
        if category:
            results = dict_engine.get_by_category(category)
        else:
            results = dict_engine.search(query)
        return {"status": "success", "count": len(results), "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)