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

# 프론트엔드가 요구하는 지장간(초기, 중기, 정기) 구조
JIJANGGAN = {
    '子': (['壬'], [], ['癸']), '丑': (['癸'], ['辛'], ['己']), 
    '寅': (['戊'], ['丙'], ['甲']), '卯': (['甲'], [], ['乙']),
    '辰': (['乙'], ['癸'], ['戊']), '巳': (['戊'], ['庚'], ['丙']), 
    '午': (['丙'], ['己'], ['丁']), '未': (['丁'], ['乙'], ['己']),
    '申': (['戊'], ['壬'], ['庚']), '酉': (['庚'], [], ['辛']), 
    '戌': (['辛'], ['丁'], ['戊']), '亥': (['戊'], ['甲'], ['壬'])
}

def format_bazi_data(engine_result):
    bazi_raw = engine_result.get("bazi", {})
    
    # 1. 4기둥 파싱 (프론트엔드는 stem, branch, stem_tg, branch_tg, napeum 을 찾음)
    def parse_pillar(pillar_str):
        if not pillar_str or len(pillar_str) < 2:
            return {"stem": "-", "branch": "-", "stem_tg": "-", "branch_tg": "-", "napeum": "-"}
        return {
            "stem": pillar_str[0],
            "branch": pillar_str[1],
            "stem_tg": "-",   # 아직 엔진에 십신 로직이 없으므로 빈칸 처리
            "branch_tg": "-", # 아직 엔진에 십신 로직이 없으므로 빈칸 처리
            "napeum": "-"     # 납음오행 빈칸 처리
        }

    # 2. 지장간 파싱 (프론트엔드는 initial, middle, main 배열을 찾음)
    def get_hidden(pillar_str):
        if not pillar_str or len(pillar_str) < 2:
            return {"initial": [], "middle": [], "main": []}
        branch = pillar_str[1]
        jig = JIJANGGAN.get(branch, ([], [], []))
        return {"initial": jig[0], "middle": jig[1], "main": jig[2]}

    y_raw = bazi_raw.get("year_pillar", "")
    m_raw = bazi_raw.get("month_pillar", "")
    d_raw = bazi_raw.get("day_pillar", "")
    h_raw = bazi_raw.get("hour_pillar", "")

    # 🚨 프론트엔드가 요구하는 거대한 JSON 뼈대를 완벽하게 맞춰서 리턴합니다!
    return {
        "origin_time": engine_result.get("origin_time", ""),
        "corrected_time": engine_result.get("corrected_time", ""),
        "gender": engine_result.get("gender", ""),
        "bazi": {
            "year": parse_pillar(y_raw),
            "month": parse_pillar(m_raw),
            "day": parse_pillar(d_raw),
            "hour": parse_pillar(h_raw)
        },
        "mechanics": {
            "hidden_stems": {
                "year": get_hidden(y_raw),
                "month": get_hidden(m_raw),
                "day": get_hidden(d_raw),
                "hour": get_hidden(h_raw)
            },
            "gongmang": [], # 프론트엔드가 배열로 기대함 (.includes)
            "tonggeun": {"total_power": 0, "has_root": False}, # 통근력 체크용
            "elements_dist": {"목": 0, "화": 0, "토": 0, "금": 0, "수": 0},
            "metadata": {}
        },
        "timeline": {
            "daewun": {
                "direction": "순행",
                "timeline": [] # 대운 차트는 비워둠
            },
            "sewun": [] # 세운 차트 비워둠
        }
        # gunghap, yongshin, classical 등은 필수가 아니므로(프론트가 예외처리 해둠) 생략!
    }

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
        
        raw_result = engine.calculate_bazi(
            dt_kst=dt_kst,
            gender=gender,
            longitude=longitude,
            apply_true_solar=apply_true_solar,
            apply_yaja=apply_yaja
        )
        
        final_result = format_bazi_data(raw_result)
        
        # 파트너 궁합은 현재 엔진에 없으므로 생략해도 프론트엔드가 뻗지 않습니다.
        
        return final_result

    except Exception as e:
        print("Backend Error:", str(e), flush=True)
        return {"status": "error", "message": str(e)}

@app.get("/")
def read_root():
    return {"message": "Backend is perfectly matched with Frontend!"}