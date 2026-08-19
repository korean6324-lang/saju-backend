import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from korean_lunar_calendar import KoreanLunarCalendar

# ==========================================
# 1. 명리/혼택 11대 마스터 엔진 Import
# ==========================================
from core_astro import CoreAstroEngine
from core_mechanics import MechanicsEngine
from logic_yongshin import YongshinEngine
from logic_dynamics import DynamicsEngine
from logic_secret import SecretEngine
from logic_classical import ClassicalEngine
from logic_dangsaju import DangsajuEngine
from logic_unse import UnseEngine
from dictionary import DictionaryEngine

# ==========================================
# 🚨 12운성 해설 DB (누락된 설명 복원)
# ==========================================
WUNSEONG_DESC = {
    "장생": "만물이 태어나듯 새로운 시작과 후원, 성장의 에너지가 솟아나는 길한 시기입니다.",
    "목욕": "호기심과 매력이 발산되는 시기. 구설수나 감정의 기복, 사치와 유흥을 경계해야 합니다.",
    "관대": "사회적 자립과 발전을 이루는 시기. 자신감이 넘치나 아집으로 인한 마찰을 주의해야 합니다.",
    "건록": "경험이 쌓여 독자적인 성취와 재물을 얻는 튼튼한 시기입니다. 독립과 자수성가에 유리합니다.",
    "제왕": "에너지가 최정점에 달하는 시기. 강력한 리더십을 발휘하지만, 꺾임을 대비해 겸손해야 합니다.",
    "쇠": "정점을 지나 서서히 물러나는 시기. 경험과 노련함으로 안정을 추구하고 타협하는 것이 좋습니다.",
    "병": "기운이 쇠약해지고 멈추는 시기. 육체적/정신적 휴식이 필요하며 무리한 계획은 금물입니다.",
    "사": "활동이 정지되고 고요해지는 시기. 내면적 성찰, 연구, 정신적 활동에 적합합니다.",
    "묘": "기운이 갇히고 갈무리되는 시기. 재물의 축적(저축)에는 유리하나, 답답함과 단절을 느낄 수 있습니다.",
    "절": "모든 기운이 끊어지고 완전히 새로운 시작을 준비하는 절대 무(無)의 상태. 과거를 청산하고 전환점을 맞이합니다.",
    "태": "새로운 생명이 잉태되듯, 조심스럽게 새로운 계획이나 아이디어가 싹트는 시기입니다.",
    "양": "안전한 환경에서 보호받으며 자라나는 시기. 무리한 확장보다 내실과 안정이 중요합니다."
}

# ==========================================
# 🚨 1-1. 업그레이드된 PracticalEngine 내재화
# ==========================================
class PracticalEngine:
    def __init__(self):
        self.health_map = {
            "목": {"organ": "간, 담낭, 신경계", "weak": "만성 피로, 신경쇠약, 우울증, 시력 저하", "excess": "간 수치 상승, 근육 뭉침, 분노 조절 어려움", "diet": "신맛 나는 음식(모과, 유자, 녹색 채소)이 약이 되며, 과음을 피해야 합니다.", "marriage_focus": "목(木) 기운이 불안정하면 신경질과 짜증이 잦아져 부부싸움의 원인이 됩니다. 부부가 함께 등산이나 산책을 하며 스트레스를 푸는 것이 좋습니다."},
            "화": {"organ": "심장, 소장, 혈관", "weak": "수족냉증, 저혈압, 무기력, 심장 두근거림", "excess": "고혈압, 심혈관 질환, 다혈질, 불면증", "diet": "쓴맛 나는 음식(수수, 홍삼, 붉은색 과일)이 좋으며, 카페인과 맵고 짠 음식을 줄여야 합니다.", "marriage_focus": "화(火) 기운이 넘치면 감정의 기복이 심해 부부간에 돌이킬 수 없는 폭언을 할 수 있습니다. 대화 시 한 템포 쉬어가는 여유가 필수입니다."},
            "토": {"organ": "위장, 비장, 소화기", "weak": "소화불량, 위염, 식욕 부진, 피부 트러블", "excess": "비만, 당뇨, 위궤양, 세포/종양 질환", "diet": "단맛 나는 음식(단호박, 꿀, 노란색 채소)이 위장을 편하게 하며, 밀가루와 야식을 피해야 합니다.", "marriage_focus": "토(土)는 생각과 번뇌를 뜻합니다. 기운이 막히면 부부 사이에 속마음을 털어놓지 않고 꽁하게 담아두어 속병이 생기니 대화를 자주 해야 합니다."},
            "금": {"organ": "폐, 대장, 호흡기", "weak": "천식, 비염, 잦은 감기, 장 트러블", "excess": "호흡기 건조, 변비, 관절/뼈 질환", "diet": "매운맛 나는 음식(생강, 마늘, 백색 채소)이 기관지를 보호하며, 건조한 환경을 피해야 합니다.", "marriage_focus": "금(金) 기운이 예민해지면 맺고 끊음이 차가워져 배우자에게 냉랭한 상처를 줍니다. 집안의 습도를 잘 맞추고 따뜻한 스킨십을 늘리십시오."},
            "수": {"organ": "신장, 방광, 생식기", "weak": "신장 기능 저하, 생식기 질환, 부종, 호르몬 불균형", "excess": "신장 결석, 냉증, 우울감, 산부인과/전립선 질환", "diet": "짠맛 나는 해조류(미역, 다시마, 검은콩)가 신장을 보양하며, 몸을 항상 따뜻하게 유지해야 합니다.", "marriage_focus": "수(水)는 생식과 잉태를 주관합니다. 이 기운이 고립되거나 과다하면 난임, 생리불순, 혹은 부부관계(속궁합)의 만족도 저하로 이어질 수 있으니 부인과/비뇨기과 관리가 매우 중요합니다."}
        }

        self.career_map = {
            "비견": {"style": "독립형 전문가", "jobs": "프리랜서, 1인 기업가, 운동선수, 지점장, 독자적 기술직", "wealth": "동업은 금물이며, 오직 내 땀방울과 기술로 번 돈만이 내 몫이 되는 자수성가형 재테크.", "marriage_role_M": "가정 내에서 주도권을 쥐려 하나, 때로는 아내를 동등한 친구처럼 대합니다. 고집이 세어 잦은 충돌이 우려되니 서로의 영역을 존중해야 합니다.", "marriage_role_F": "남편에게 통제받기를 극도로 싫어하며, 맞벌이나 사회활동을 통해 철저히 평등한 부부 관계를 지향하는 주체적인 아내입니다."},
            "겁재": {"style": "승부사 및 투자가", "jobs": "M&A 전문가, 펀드매니저, 프로게이머, 경쟁이 치열한 영업직", "wealth": "하이리스크 하이리턴. 공격적인 투자나 주식, 경매 등에 관심이 많아 재물의 기복이 큰 편입니다.", "marriage_role_M": "아내(재성)를 극하는 기운이 강해 무뚝뚝하거나 경제권을 두고 다툴 수 있습니다. 재산 관리를 아내에게 전적으로 맡기는 것이 가정을 지키는 길입니다.", "marriage_role_F": "남편을 두고 다른 여성과 경쟁하는 구도가 되기 쉬우며 자존심이 강합니다. 각자의 경제권을 분리하고 서로의 자존심을 건드리지 않아야 합니다."},
            "식신": {"style": "장인 및 연구가", "jobs": "연구원, 셰프, 개발자(IT), 작가, 제조업, 엔지니어", "wealth": "한 분야를 꾸준히 파고들어 얻는 정당하고 지속적인 수입으로, 마르지 않는 화수분 같은 재물운입니다.", "marriage_role_M": "아내와 자식에게 다정다감하게 베풀고 요리를 해주는 등 매우 가정적이고 따뜻한 남편입니다. 식도락을 즐기며 평화로운 가정을 꾸립니다.", "marriage_role_F": "자식에 대한 맹목적인 사랑과 교육열이 뛰어나며, 남편을 살뜰히 챙기고 집안에 훈훈한 생기를 불어넣는 완벽한 양육자입니다."},
            "상관": {"style": "크리에이터 및 언변가", "jobs": "마케터, 유튜버/방송인, 강사, 로이어(변호사), 디자이너", "wealth": "뛰어난 아이디어와 말재주를 무기로, 시류를 빠르게 읽고 단기간에 큰 수익을 창출해 내는 능력자입니다.", "marriage_role_M": "틀에 얽매이는 것을 싫어하고 개방적입니다. 센스와 유머로 가정을 즐겁게 하나, 잔소리가 심해질 수 있으니 말을 부드럽게 해야 합니다.", "marriage_role_F": "남편(관성)을 통제하고 가르치려 드는 기질이 있어 부부싸움이 잦을 수 있습니다. 그러나 위기 대처 능력이 뛰어나 가정의 든든한 해결사 역할을 합니다."},
            "편재": {"style": "사업가 및 무역가", "jobs": "글로벌 무역, 부동산 개발, 플랫폼 사업가, 유통/물류업", "wealth": "돈의 흐름을 꿰뚫어 보며 씀씀이가 크고 통 큰 투자를 즐깁니다. 사업이나 횡재수로 거대한 부를 쥘 수 있습니다.", "marriage_role_M": "집안에 머물기보다 밖에서 활발히 활동하며 통 큰 스케일로 가세를 일으킵니다. 다만 풍류를 즐길 우려가 있으니 가정에 충실해야 합니다.", "marriage_role_F": "시댁이나 가정의 대소사를 시원시원하게 처리하는 능력자입니다. 스케일이 크고 사회활동이 활발하여 남편을 경제적으로 돕는 여장부입니다."},
            "정재": {"style": "금융가 및 관리자", "jobs": "은행원, 회계사, 재무 관리자, 공기업, 안정적인 프랜차이즈", "wealth": "티끌 모아 태산. 모험을 피하고 저축과 안정적인 적금, 확실한 자산을 선호하는 꼼꼼한 관리형 재테크입니다.", "marriage_role_M": "책임감이 강하고 아내(재성)를 끔찍이 아끼며, 낭비 없이 가계를 건실하게 꾸리는 가장 모범적이고 든든한 남편입니다.", "marriage_role_F": "내조의 여왕입니다. 알뜰한 살림살이로 시댁과 가정을 평안하게 이끌며, 내 가족을 끝까지 보살피는 꼼꼼하고 지혜로운 현모양처입니다."},
            "편관": {"style": "특수직 및 카리스마 리더", "jobs": "군인, 경찰, 검찰, 외과의사, 스타트업 CEO, 리스크 관리자", "wealth": "돈보다는 조직의 명예와 가오(권력)를 중시하며, 큰 위기를 돌파한 후 보상으로 막대한 부가 따라오는 스타일입니다.", "marriage_role_M": "무뚝뚝하고 가부장적일 수 있으나, 외풍이 불 때 온몸으로 비바람을 막아내며 처자식을 지키는 강직한 카리스마의 수호자입니다.", "marriage_role_F": "평범 일상보다는 기복을 즐기며, 카리스마 넘치는 남편을 내조하거나 본인 스스로 억센 환경을 통제하며 가정을 지켜내는 강인한 아내입니다."},
            "정관": {"style": "행정가 및 조직인", "jobs": "고위 공무원, 대기업 임원, 행정직, 규정/감사 부서", "wealth": "안정적인 직장의 월급과 정년 보장을 통한 노후 연금 등 가장 합리적이고 변수 없는 안전 지향형 자산 축적입니다.", "marriage_role_M": "가정의 규범과 도리를 철저히 지키며, 아내를 존중하고 자녀에게 모범이 되는 가장 합리적이고 다정한 신사 같은 남편입니다.", "marriage_role_F": "남편을 하늘처럼 존중하고 따르며, 집안의 대소사를 규범에 맞게 흐트러짐 없이 이끌어가는 가장 이상적이고 단아한 아내입니다."},
            "편인": {"style": "전략가 및 기획자", "jobs": "기획자, 프로듀서, 종교/철학가, 정신과 의사, 예술 감독", "wealth": "남들이 보지 못하는 정보나 특수한 라이선스(자격증, 지적재산권)를 활용하여 지대(Rent) 수익을 창출해 냅니다.", "marriage_role_M": "눈치가 빠르고 직관력이 뛰어나 아내의 속마음을 잘 읽어냅니다. 다만 가끔은 혼자만의 고독한 취미나 은둔의 공간이 반드시 필요한 남편입니다.", "marriage_role_F": "남다른 센스와 예술적 감각으로 가정을 꾸리나, 감정 기복이 있고 시댁과의 거리를 두려 하는 경향이 있습니다. 독립적인 생활 패턴이 필요합니다."},
            "정인": {"style": "교육가 및 학자", "jobs": "교수, 교사, 문서/부동산 임대업, 학원 사업, 출판업", "wealth": "부동산 문서, 결재권, 혹은 상속받은 자산 등 땅이나 건물에 돈을 묻어두고 안정적인 임대 수익을 내는 것이 최상입니다.", "marriage_role_M": "아내에게 따뜻한 사랑을 기대하며 다소 의존적인 면이 있으나, 성품이 자애롭고 집안의 평화를 최우선으로 생각하는 선비 같은 남편입니다.", "marriage_role_F": "마치 어머니의 품처럼 넉넉하게 남편을 감싸주고 이해하며, 자녀 교육에 훌륭한 환경을 조성하고 가족에게 극진한 지혜로운 아내입니다."}
        }

    def analyze_health(self, elements_dist: dict) -> list:
        health_warnings = []
        if not isinstance(elements_dist, dict): elements_dist = {}
        for element, count in elements_dist.items():
            if element not in self.health_map: continue
            data = self.health_map[element]
            if count >= 3: health_warnings.append({"element": element, "status_code": "과다", "status": "과다 (기운이 너무 강해 병이 됨)", "organ": data["organ"], "symptom": data["excess"], "diet_advice": data["diet"], "marriage_focus": data["marriage_focus"], "advice": f"[{element}]의 기운이 사주에 너무 쏠려 있어 {data['organ']} 쪽에 열성(熱性) 질환이나 과부하가 올 수 있습니다. 꾸준한 검진이 필요합니다."})
            elif count == 0: health_warnings.append({"element": element, "status_code": "고립(無)", "status": "고립/태약 (기운이 없어 병이 됨)", "organ": data["organ"], "symptom": data["weak"], "diet_advice": data["diet"], "marriage_focus": data["marriage_focus"], "advice": f"사주 원국에 [{element}]의 기운이 메말라 있어 {data['organ']} 기능이 선천적으로 약할 수 있습니다. 해당 부위의 면역력 관리에 각별히 신경 쓰십시오."})
        if not health_warnings: health_warnings.append({"element": "종합", "status_code": "양호", "status": "오행 균형 양호", "organ": "전신", "symptom": "특별한 선천적 취약점 없음", "diet_advice": "편식 없이 골고루 섭취하는 것이 최고의 보약입니다.", "marriage_focus": "부부간 기운의 충돌이 적고 건강한 가정을 꾸릴 수 있는 훌륭한 밸런스입니다.", "advice": "오행의 개수가 비교적 골고루 분포되어 있어 선천적인 장기의 균형이 훌륭합니다. 규칙적인 생활만 유지하시면 큰 병 없이 건강을 누릴 수 있습니다."})
        return health_warnings

    def analyze_career(self, geokguk_data: dict, yongshin_data: dict, gender: str) -> dict:
        if not isinstance(geokguk_data, dict): geokguk_data = {}
        if not isinstance(yongshin_data, dict): yongshin_data = {}
        name_clean = geokguk_data.get("name_clean", geokguk_data.get("name", ""))
        core_tg = name_clean.replace("격", "").replace("월건록", "비견").replace("양인", "겁재").replace("월걸록", "겁재")
        if core_tg not in self.career_map: core_tg = "식신"
        career_info = self.career_map[core_tg]
        ys_str = str(yongshin_data.get("yongshin", ""))
        work_env = "나만의 페이스를 유지할 수 있는 독립적 환경이 중요합니다."
        if "식상" in ys_str or "재성" in ys_str: work_env = "가만히 앉아있는 업무보다는 성과에 따른 확실한 보상이 주어지고, 이동이나 활동성이 보장되는 환경에서 폭발적인 능력을 발휘합니다."
        elif "관성" in ys_str: work_env = "체계가 없고 불안정한 환경보다는, 간판이 확실하고 규율이 잡혀있는 큰 조직이나 공공기관에 소속될 때 심리적 안정과 승진이 빠릅니다."
        elif "인성" in ys_str or "비겁" in ys_str: work_env = "결과만을 재촉당하는 영업직보다는, 나의 전문 지식(자격증)을 바탕으로 결재권을 행사하거나 독립된 권한이 주어지는 환경이 유리합니다."
        role_key = "marriage_role_M" if gender.upper() == 'M' else "marriage_role_F"
        return {"core_trait": career_info["style"], "recommended_jobs": career_info["jobs"], "wealth_management": career_info["wealth"], "marriage_role": career_info.get(role_key, ""), "work_environment": work_env}

# ==========================================
# 🚨 1-2. 혼택촬요 궁합(FengShuiHontaekEngine) 딥 리포트 업그레이드 완전판
# ==========================================
NINE_STARS = {
    1: {"name": "일백수성(一白水星)", "element": "수(水)", "trigram": "감(坎)", "group": "동사택"},
    2: {"name": "이흑토성(二黑土星)", "element": "토(土)", "trigram": "곤(坤)", "group": "서사택"},
    3: {"name": "삼벽목성(三碧木星)", "element": "목(木)", "trigram": "진(震)", "group": "동사택"},
    4: {"name": "사록목성(四綠木星)", "element": "목(木)", "trigram": "손(巽)", "group": "동사택"},
    5: {"name": "오황토성(五黃土星)", "element": "토(土)", "trigram": "중궁(中)", "group": "중앙"},
    6: {"name": "육백금성(六白金星)", "element": "금(金)", "trigram": "건(乾)", "group": "서사택"},
    7: {"name": "칠적금성(七赤金星)", "element": "금(金)", "trigram": "태(兌)", "group": "서사택"},
    8: {"name": "팔백토성(八白土星)", "element": "토(土)", "trigram": "간(艮)", "group": "서사택"},
    9: {"name": "구자화성(九紫火星)", "element": "화(火)", "trigram": "이(離)", "group": "동사택"}
}

EIGHT_MANSIONS_DIRECTIONS = {
    1: {"생기": "동남", "천을": "동", "연년": "남", "복위": "북", "화해": "서", "육살": "북서", "오귀": "북동", "절명": "남서"},
    2: {"생기": "북동", "천을": "서", "연년": "북서", "복위": "남서", "화해": "동", "육살": "남", "오귀": "동남", "절명": "북"},
    3: {"생기": "남", "천을": "북", "연년": "동남", "복위": "동", "화해": "남서", "육살": "북동", "오귀": "북서", "절명": "서"},
    4: {"생기": "북", "천을": "남", "연년": "동", "복위": "동남", "화해": "북서", "육살": "서", "오귀": "남서", "절명": "북동"},
    6: {"생기": "서", "천을": "북동", "연년": "남서", "복위": "북서", "화해": "동남", "육살": "북", "오귀": "동", "절명": "남"},
    7: {"생기": "북서", "천을": "남서", "연년": "북동", "복위": "서", "화해": "북", "육살": "동남", "오귀": "남", "절명": "동"},
    8: {"생기": "남서", "천을": "북서", "연년": "서", "복위": "북동", "화해": "남", "육살": "동", "오귀": "북", "절명": "동남"},
    9: {"생기": "동", "천을": "동남", "연년": "북", "복위": "남", "화해": "북동", "육살": "남서", "오귀": "서", "절명": "북서"}
}

DIRECTION_ADVICE_DB = {
    "생기": "최상의 길방입니다. 이 방향으로 출입구를 내거나 머리를 두고 자면 재물과 명예가 크게 상승합니다.",
    "천을": "건강과 치유의 방위입니다. 침대를 이 방향으로 두면 질병이 낫고 훌륭한 귀인(조력자)을 만나게 됩니다.",
    "연년": "조화와 인연의 방위입니다. 부부 침실을 두기에 가장 좋으며, 가정이 화목해지고 안정적인 재물을 모읍니다.",
    "복위": "안정과 평온의 방위입니다. 학생의 책상이나 명상 공간으로 적합하며 집중력을 크게 높여줍니다.",
    "화해": "구설수나 피로가 쌓이는 흉방입니다. 창고나 화장실을 두면 흉한 기운을 억누를 수 있습니다.",
    "육살": "인간관계 마찰과 관재구설을 일으킵니다. 이 방향으로 머리를 두고 자는 것을 절대 피해야 합니다.",
    "오귀": "화재, 돌발 사고를 의미하는 독한 흉방입니다. 중요한 물건을 두거나 출입구를 내는 것을 피해야 합니다.",
    "절명": "최악의 흉방으로 기운이 단절됩니다. 가급적 공간을 비워두거나 무거운 가구로 억눌러 기운을 차단해야 합니다."
}

DAEYUNYEON_MATRIX = {
    1: {1: "복위", 2: "절명", 3: "천을", 4: "생기", 6: "육살", 7: "화해", 8: "오귀", 9: "연년"},
    2: {1: "절명", 2: "복위", 3: "화해", 4: "오귀", 6: "연년", 7: "천을", 8: "생기", 9: "육살"},
    3: {1: "천을", 2: "화해", 3: "복위", 4: "연년", 6: "오귀", 7: "절명", 8: "육살", 9: "생기"},
    4: {1: "생기", 2: "오귀", 3: "연년", 4: "복위", 6: "화해", 7: "육살", 8: "절명", 9: "천을"},
    6: {1: "육살", 2: "연년", 3: "오귀", 4: "화해", 6: "복위", 7: "생기", 8: "천을", 9: "절명"},
    7: {1: "화해", 2: "천을", 3: "절명", 4: "육살", 6: "생기", 7: "복위", 8: "연년", 9: "오귀"},
    8: {1: "오귀", 2: "생기", 3: "육살", 4: "절명", 6: "천을", 7: "연년", 8: "복위", 9: "화해"},
    9: {1: "연년", 2: "육살", 3: "생기", 4: "천을", 6: "절명", 7: "오귀", 8: "화해", 9: "복위"}
}

HONTAEK_GUNGHAP_DB = {
    "생기": {"type": "사길성(四吉星)", "desc": "【대길합】 자손이 번창하고 재물이 크게 일어나는 최고의 궁합입니다. 생명력이 넘치는 천생연분입니다."},
    "천을": {"type": "사길성(四吉星)", "desc": "【길합】 잔병치레가 없고 뜻밖의 귀인이 나타나 위기를 구원해 주는 평안하고 조화로운 궁합입니다."},
    "연년": {"type": "사길성(四吉星)", "desc": "【길합】 부부가 화목하고 수명이 길어 백년해로하는 훌륭한 길합입니다. 인연이 깊고 다정합니다."},
    "복위": {"type": "사길성(四吉星)", "desc": "【길합】 기운이 흩어지지 않고 안정되어 가정이 큰 굴곡 없이 평탄하게 유지되는 무난한 길합입니다."},
    "화해": {"type": "사흉성(四凶星)", "desc": "【흉합】 동서상혼(東西相混)으로 재물이 흩어지고 크고 작은 다툼과 상해를 입기 쉬운 흉합입니다."},
    "육살": {"type": "사흉성(四凶星)", "desc": "【흉합】 음란함, 시비, 관재구설이 발생하기 쉬운 흉합으로, 부부간의 강한 인내와 신뢰가 필요합니다."},
    "오귀": {"type": "사흉성(四凶星)", "desc": "【대흉합】 오귀천궁(五鬼穿宮). 예기치 않은 돌발 재난, 화재, 구설수가 따르는 매우 불안정한 결합입니다."},
    "절명": {"type": "사흉성(四凶星)", "desc": "【대흉합】 자손이 귀해지고 수명이 꺾일 우려가 있는 가장 치명적인 흉합입니다. 강력한 택일(개운법) 비보가 필수적입니다."}
}

GOJIN_GWASUK_MAP = {
    "수": {"branches": ["亥", "子", "丑"], "gojin": "寅", "gwasuk": "戌"},
    "목": {"branches": ["寅", "卯", "辰"], "gojin": "巳", "gwasuk": "丑"},
    "화": {"branches": ["巳", "午", "未"], "gojin": "申", "gwasuk": "辰"},
    "금": {"branches": ["申", "酉", "戌"], "gojin": "亥", "gwasuk": "未"}
}

GACHWI_GILWOL_DB = {
    "子": {"대리월": [6, 12], "소리월": [1, 7], "방녀부모": [2, 8], "방부": [3, 9], "방옹고": [4, 10], "방녀": [5, 11]},
    "丑": {"대리월": [5, 11], "소리월": [4, 10], "방녀부모": [3, 9], "방부": [2, 8], "방옹고": [1, 7], "방녀": [6, 12]},
    "寅": {"대리월": [2, 8], "소리월": [3, 9], "방녀부모": [4, 10], "방부": [5, 11], "방옹고": [6, 12], "방녀": [1, 7]},
    "卯": {"대리월": [1, 7], "소리월": [6, 12], "방녀부모": [5, 11], "방부": [4, 10], "방옹고": [3, 9], "방녀": [2, 8]},
    "辰": {"대리월": [4, 10], "소리월": [5, 11], "방녀부모": [6, 12], "방부": [1, 7], "방옹고": [2, 8], "방녀": [3, 9]},
    "巳": {"대리월": [3, 9], "소리월": [2, 8], "방녀부모": [1, 7], "방부": [6, 12], "방옹고": [5, 11], "방녀": [4, 10]},
    "午": {"대리월": [6, 12], "소리월": [1, 7], "방녀부모": [2, 8], "방부": [3, 9], "방옹고": [4, 10], "방녀": [5, 11]},
    "未": {"대리월": [5, 11], "소리월": [4, 10], "방녀부모": [3, 9], "방부": [2, 8], "방옹고": [1, 7], "방녀": [6, 12]},
    "申": {"대리월": [2, 8], "소리월": [3, 9], "방녀부모": [4, 10], "방부": [5, 11], "방옹고": [6, 12], "방녀": [1, 7]},
    "酉": {"대리월": [1, 7], "소리월": [6, 12], "방녀부모": [5, 11], "방부": [4, 10], "방옹고": [3, 9], "방녀": [2, 8]},
    "戌": {"대리월": [4, 10], "소리월": [5, 11], "방녀부모": [6, 12], "방부": [1, 7], "방옹고": [2, 8], "방녀": [3, 9]},
    "亥": {"대리월": [3, 9], "소리월": [2, 8], "방녀부모": [1, 7], "방부": [6, 12], "방옹고": [5, 11], "방녀": [4, 10]}
}

HONTAEK_SPECIAL_DB = {
    "천지합덕": {"hanja": "天地合德格", "desc": "하늘(천간)과 땅(지지)이 완벽히 화합하는 구조. 정신과 육체, 안과 밖이 빈틈없이 결합하는 궁합 최고의 대길상(大吉相)입니다."},
    "교귀격": {"hanja": "交貴格", "desc": "남녀가 서로의 귀인(천을귀인)을 교환하는 특별한 명리 구조. 흉함을 덮고 서로의 사회적 성취를 크게 끌어올려 줍니다."},
    "교록격": {"hanja": "交祿格", "desc": "남녀가 서로의 사주에서 튼튼한 복록(건록)을 상호 교환하는 대길격. 결혼 후 재물이 폭발적으로 일어나고 부귀쌍전합니다."}
}

class FengShuiHontaekEngine:
    def __init__(self):
        self.cheon_hap = [{"甲", "己"}, {"乙", "庚"}, {"丙", "辛"}, {"丁", "壬"}, {"戊", "癸"}]
        self.ji_hap = [{"子", "丑"}, {"寅", "亥"}, {"卯", "戌"}, {"辰", "酉"}, {"巳", "申"}, {"午", "未"}]
        self.gwiin_map = {"甲":["丑","未"], "戊":["丑","未"], "庚":["丑","未"], "乙":["子","申"], "己":["子","申"], "丙":["亥","酉"], "丁":["亥","酉"], "辛":["午","寅"], "壬":["卯","巳"], "癸":["卯","巳"]}
        self.geonrok_map = {"甲":"寅", "乙":"卯", "丙":"巳", "戊":"巳", "丁":"午", "己":"午", "庚":"申", "辛":"酉", "壬":"亥", "癸":"子"}

    def _safe_str(self, val) -> str: return str(val).strip() if val else ""
    def _safe_int(self, val, default=1984) -> int:
        try:
            clean_str = "".join(filter(str.isdigit, str(val)))
            return int(clean_str) if clean_str else default
        except (ValueError, TypeError): return default

    def calculate_honmyeong_gung(self, base_year: int, gender: str) -> dict:
        clean_year = self._safe_int(base_year)
        safe_gender = self._safe_str(gender).upper()
        if safe_gender not in ['M', 'F']: safe_gender = 'M'
        digit_sum = sum(int(digit) for digit in str(clean_year))
        while digit_sum > 9:
            digit_sum = sum(int(digit) for digit in str(digit_sum))
        if safe_gender == 'M':
            honmyeong_num = 11 - digit_sum
            if honmyeong_num > 9: honmyeong_num -= 9
            if honmyeong_num == 5: honmyeong_num = 2
        else: 
            honmyeong_num = digit_sum + 4
            if honmyeong_num > 9: honmyeong_num -= 9
            if honmyeong_num == 5: honmyeong_num = 8
        star_info = NINE_STARS.get(honmyeong_num, NINE_STARS[1])
        return {
            "number": honmyeong_num,
            "name": star_info["name"],
            "element": star_info["element"],
            "trigram": star_info["trigram"],
            "group": star_info["group"]
        }

    def get_auspicious_directions(self, honmyeong_num: int) -> dict:
        empty_result = {"good": {}, "bad": {}}
        h_num = self._safe_int(honmyeong_num, default=0)
        if h_num == 5 or h_num not in EIGHT_MANSIONS_DIRECTIONS:
            return empty_result
        dirs = EIGHT_MANSIONS_DIRECTIONS.get(h_num, {})
        return {
            "good": {
                "생기": {"dir": dirs.get("생기"), "advice": DIRECTION_ADVICE_DB.get("생기", "")},
                "천을": {"dir": dirs.get("천을"), "advice": DIRECTION_ADVICE_DB.get("천을", "")},
                "연년": {"dir": dirs.get("연년"), "advice": DIRECTION_ADVICE_DB.get("연년", "")},
                "복위": {"dir": dirs.get("복위"), "advice": DIRECTION_ADVICE_DB.get("복위", "")}
            },
            "bad": {
                "화해": {"dir": dirs.get("화해"), "advice": DIRECTION_ADVICE_DB.get("화해", "")},
                "육살": {"dir": dirs.get("육살"), "advice": DIRECTION_ADVICE_DB.get("육살", "")},
                "오귀": {"dir": dirs.get("오귀"), "advice": DIRECTION_ADVICE_DB.get("오귀", "")},
                "절명": {"dir": dirs.get("절명"), "advice": DIRECTION_ADVICE_DB.get("절명", "")}
            }
        }

    def _get_element_desc(self, el_pure: str) -> str:
        descs = {
            "목": "유연하고 뻗어나가는 목(木, 나무)의 에너지",
            "화": "뜨겁고 맹렬하게 타오르는 화(火, 불)의 에너지",
            "토": "만물을 포용하고 중재하는 토(土, 흙)의 에너지",
            "금": "강하고 단단한 금(金, 쇠)의 에너지",
            "수": "깊고 유연하게 스며드는 수(水, 물)의 에너지"
        }
        return descs.get(el_pure, "")

    def _analyze_element_relation(self, m_el: str, f_el: str) -> dict:
        el_map = {"목": 0, "화": 1, "토": 2, "금": 3, "수": 4}
        hanja_map = {"목": "木", "화": "火", "토": "土", "금": "金", "수": "水"}
        m_idx = el_map.get(m_el, 0)
        f_idx = el_map.get(f_el, 0)
        
        rel_type = ""
        title = ""
        desc = ""
        m_stance = ""
        f_stance = ""

        if m_idx == f_idx:
            rel_type = "비화"
            title = f"오행의 든든한 동질성 ({m_el}비화, {hanja_map[m_el]}比和)"
            desc = f"두 분은 같은 {m_el}의 에너지를 지녀 서로가 서로를 거울처럼 비추고 든든하게 지지해 주는 관계입니다."
            m_stance = "권위의식 없이 아내와 눈높이를 맞추며 평등하고 편안한 관계를 유지합니다."
            f_stance = "남편이라기보다 동등한 친구나 든든한 동료처럼 깊은 편안함을 느낍니다."
        elif f_idx == (m_idx + 1) % 5:
            rel_type = "남생여"
            title = f"오행의 이타적인 상생 작용 ({m_el}생{f_el}, {hanja_map[m_el]}生{hanja_map[f_el]})"
            desc = f"남성의 {m_el} 기운이 여성의 {f_el} 기운을 끊임없이 보살피고 키워주는 헌신적인 상생(相生) 관계입니다."
            m_stance = "아내를 위해 헌신하고 조건 없이 내어주는 것에 큰 기쁨과 보람을 느낍니다."
            f_stance = "남편의 전폭적인 지지와 희생 덕분에 정서적으로 완벽한 편안함과 안정감을 느낍니다."
        elif m_idx == (f_idx + 1) % 5:
            rel_type = "여생남"
            title = f"오행의 이타적인 상생 작용 ({f_el}생{m_el}, {hanja_map[f_el]}生{hanja_map[m_el]})"
            desc = f"여성의 {f_el} 기운이 남성의 {m_el} 기운을 끊임없이 보살피고 키워주는 내조의 상생(相生) 관계입니다."
            m_stance = "아내의 헌신적인 내조와 지지 덕분에 밖에서 사회적 능력을 마음껏 펼칠 수 있습니다."
            f_stance = "남편을 보살피고 뒷바라지하는 것에 보람을 느끼며, 가정의 든든한 뿌리 역할을 합니다."
        elif f_idx == (m_idx + 2) % 5:
            rel_type = "남극여"
            title = f"오행의 치명적인 상극 작용 ({m_el}극{f_el}, {hanja_map[m_el]}克{hanja_map[f_el]})"
            desc = f"두 분이 가진 에너지의 본질이 서로를 파괴하는 상극(相剋) 관계에 놓여 있습니다. 자연의 이치상 {m_el}의 기운이 {f_el}의 기운을 무자비하게 억압하는 '{m_el}극{f_el}'의 현상이 발생합니다."
            m_stance = "본인은 그럴 의도가 없더라도 결과적으로 여성의 에너지를 꺾고 일방적으로 통제하는 형태가 되어버립니다. 기운이 매끄럽게 순환하지 못해 남성 역시 피로감을 느낍니다."
            f_stance = "남성의 강한 기운과 성향에 심리적, 육체적으로 지속적인 억압을 받게 됩니다. 본인의 능력을 마음껏 펼치지 못하고 답답함을 느끼며 위축됩니다."
        elif m_idx == (f_idx + 2) % 5:
            rel_type = "여극남"
            title = f"오행의 치명적인 상극 작용 ({f_el}극{m_el}, {hanja_map[f_el]}克{hanja_map[m_el]})"
            desc = f"두 분이 가진 에너지의 본질이 서로를 파괴하는 상극(相剋) 관계에 놓여 있습니다. 자연의 이치상 {f_el}의 기운이 {m_el}의 기운을 무자비하게 억압하는 '{f_el}극{m_el}'의 현상이 발생합니다."
            m_stance = "여성의 강한 주관과 기운에 심리적으로 억압을 받으며, 집 안에서 안식을 찾기 어렵고 기가 눌려 무기력해지기 쉽습니다."
            f_stance = "본인은 그럴 의도가 없더라도 남편의 행동이 성에 차지 않아 끊임없이 통제하려 들며, 이로 인해 스스로도 피로와 예민함을 느낍니다."

        return {"title": title, "desc": desc, "m_stance": m_stance, "f_stance": f_stance, "is_clash": "극" in rel_type}

    def evaluate_hontaek_gunghap(self, m_year: int, f_year: int, m_name: str = "신랑", f_name: str = "신부") -> dict:
        result = {"status": "error", "star": "알 수 없음", "type": "-", "desc": "연산 오류"}
        m_gung = self.calculate_honmyeong_gung(m_year, 'M')
        f_gung = self.calculate_honmyeong_gung(f_year, 'F')
        m_num = m_gung.get("number")
        f_num = f_gung.get("number")
        if not m_num or not f_num: return result
        
        matched_star = DAEYUNYEON_MATRIX.get(m_num, {}).get(f_num)
        if matched_star:
            interpretation = HONTAEK_GUNGHAP_DB.get(matched_star, {})
            m_group = m_gung['group']
            f_group = f_gung['group']
            is_match = (m_group == f_group)
            
            m_el_pure = m_gung['element'].split('(')[0]
            f_el_pure = f_gung['element'].split('(')[0]

            if is_match:
                freq_title = f"1. 생체 주파수와 공간 에너지의 완벽한 조화 ({m_group} 결합)"
                freq_desc = f"두 분은 '{m_group}'이라는 동일한 주파수 대역을 수신합니다. 결혼이나 동거를 통해 한 공간에 살게 될 경우, 침대의 방향이나 현관문의 위치 등 공간의 에너지가 두 사람 모두에게 건강과 재물을 증폭시켜주는 강력 시너지 구조가 형성됩니다."
            else:
                freq_title = "1. 생체 주파수와 공간 에너지의 정반대 대립 (동사택 vs 서사택)"
                freq_desc = "동사택과 서사택은 마치 'AM 라디오와 FM 라디오'처럼 수신하는 주파수 대역이 완전히 다릅니다. 한 공간에 살게 되면 심각한 모순이 발생하여, 한쪽을 반드시 희생시키거나 기를 빨아먹는 구조가 되므로 장기적으로 원인 모를 컨디션 난조나 무기력증에 시달리게 됩니다."

            rel_data = self._analyze_element_relation(m_el_pure, f_el_pure)
            
            star_title = f"3. 팔택명경(八宅明鏡)상 '{matched_star}' 에너지의 형성"
            if is_match:
                star_desc = f"역학적으로 '{matched_star}'라는 훌륭한 에너지가 생성됩니다. 소통의 주파수가 맞아 대화의 핀트가 정확히 일치하며, 사소한 오해 없이 서로를 향한 깊은 신뢰와 화합을 주관하는 든든한 뼈대가 됩니다."
            else:
                star_desc = f"역학적으로 '{matched_star}'라는 흉한 에너지가 생성됩니다. '{matched_star}'란 재앙과 피해를 의미하며 소통의 단절을 주관합니다. 가치관과 삶의 템포가 달라 대화의 핀트가 자꾸 엇나가며, 서로 좋은 의도로 한 행동조차 상대방에게는 간섭이나 스트레스로 곡해되어 전달되는 빈도가 매우 높습니다."

            manifestations = []
            if is_match and not rel_data["is_clash"]:
                manifestations.append({"title": "\"함께 있을수록 에너지가 충전된다\"", "desc": "함께 시간을 보내고 같은 공간에서 잠을 잘 때, 서로의 기운이 톱니바퀴처럼 맞물려 방전된 체력이 빠르게 회복되는 느낌을 받게 됩니다."})
                manifestations.append({"title": "\"가까워질수록 서로의 능력을 키워준다\"", "desc": f"오행의 조화({m_el_pure}-{f_el_pure})로 인해, 대화를 나눌수록 막혀있던 아이디어가 떠오르고 사회적 성취를 크게 끌어올려 줍니다."})
                manifestations.append({"title": "결정적 순간의 가치관 일치", "desc": "주거지 이동이나 금전 문제 등 중요한 결정을 내릴 때, 서로 바라보는 길흉의 체계가 같아 갈등 없이 평탄하게 뜻을 모을 수 있습니다."})
                conclusion = "명리학과 풍수지리적 관점에서 볼 때, 두 분의 결합은 톱니바퀴가 완벽하게 맞물려 돌아가는 최상의 구조입니다. 서로가 서로의 결핍을 채워주고 공간의 에너지를 온전히 흡수할 수 있으니, 의구심을 가질 필요 없이 득(得)이 넘쳐나는 완벽한 천생연분임이 분명합니다."
            else:
                manifestations.append({"title": "\"함께 있을수록 이유 없이 피곤하다\"", "desc": "함께 시간을 보내고 같은 공간에서 잠을 자는데도 에너지가 충전되는 것이 아니라 서로 방전되는 느낌을 받게 됩니다."})
                if rel_data["is_clash"]:
                    manifestations.append({"title": "\"가까워질수록 상처를 준다\"", "desc": f"{rel_data['title'].split(' ')[-1]}의 형국이므로, 무심코 뱉은 말이나 행동이 날카로운 비수처럼 꽂혀 지울 수 없는 상처가 되기 쉽습니다."})
                else:
                    manifestations.append({"title": "\"채워지지 않는 공허함\"", "desc": "겉으로는 다투지 않더라도, 근본적인 에너지의 방향성이 달라 마음 한구석에 늘 채워지지 않는 외로움과 공허함이 자리 잡기 쉽습니다."})
                manifestations.append({"title": "결정적 순간의 가치관 충돌", "desc": "주거지 이동, 금전 문제 등 중요한 결정을 내릴 때, 서로 바라보는 방향(길흉의 체계)이 정반대이므로 끝없는 평행선을 달리게 됩니다."})
                conclusion = "명리학과 풍수지리적 관점에서 볼 때, 두 분의 결합은 톱니바퀴의 규격이 달라 맞물려 돌아갈수록 마모가 심해지는 구조입니다. 어느 한쪽이 나빠서가 아니라, 타고난 에너지의 설계도 자체가 서로를 밀어내고 극(剋)하는 방향으로 세팅되어 있기 때문입니다. 의구심을 가질 필요 없이, 역학적 원리상 서로에게 득보다 실이 많은 인연임이 분명하게 나타납니다."

            deep_report = {
                "groom_profile": {
                    "name": f"{m_name} 님 ({m_year}년생 남성)",
                    "gung": f"{m_gung['trigram']}궁",
                    "group": m_gung['group'],
                    "element_desc": self._get_element_desc(m_el_pure)
                },
                "bride_profile": {
                    "name": f"{f_name} 님 ({f_year}년생 여성)",
                    "gung": f"{f_gung['trigram']}궁",
                    "group": f_gung['group'],
                    "element_desc": self._get_element_desc(f_el_pure)
                },
                "is_good": (is_match and not rel_data["is_clash"]),
                "reasons": [
                    {"title": freq_title, "desc": freq_desc},
                    {"title": rel_data['title'], "desc": rel_data['desc'], "m_stance": rel_data['m_stance'], "f_stance": rel_data['f_stance']},
                    {"title": star_title, "desc": star_desc}
                ],
                "manifestations": manifestations,
                "conclusion": conclusion
            }

            result = {
                "status": "success",
                "star": matched_star,
                "type": interpretation.get("type", ""),
                "desc": interpretation.get("desc", ""),
                "deep_report": deep_report
            }
        return result

    def get_gachwi_gilwol(self, f_year_branch: str) -> dict:
        f_b = self._safe_str(f_year_branch)
        if not f_b or f_b not in GACHWI_GILWOL_DB: return {"status": "error", "message": "누락"}
        data = GACHWI_GILWOL_DB[f_b]
        return {"status": "success", "best_months": data["대리월"], "good_months": data["소리월"], "warning": "대리월(大利月)과 소리월(小利月) 내에서 택일하는 것이 혼택촬요의 제1원칙입니다.", "forbidden": {"신부부모흉": data["방녀부모"], "시부모흉": data["방옹고"], "신랑흉": data["방부"], "신부흉": data["방녀"]}}

    def check_taekil_gojin_gwasuk(self, m_branch: str, f_branch: str, target_day_branch: str) -> dict:
        m_b, f_b, t_b = self._safe_str(m_branch), self._safe_str(f_branch), self._safe_str(target_day_branch)
        result = {"is_banned": False, "reason": "사용 가능한 무난한 날짜입니다."}
        if not t_b: return result
        for group in GOJIN_GWASUK_MAP.values():
            if m_b in group["branches"] and t_b == group["gojin"]: return {"is_banned": True, "reason": f"【경고】 혼례일({t_b}일)이 신랑({m_b}띠)에게 고진살(孤辰殺, 홀아비살)입니다. 절대 배제하십시오."}
            if f_b in group["branches"] and t_b == group["gwasuk"]: return {"is_banned": True, "reason": f"【경고】 혼례일({t_b}일)이 신부({f_b}띠)에게 과숙살(寡宿殺, 상부살)입니다. 절대 배제하십시오."}
        return result

    def analyze_special_gunghap(self, m_day_stem: str, m_day_branch: str, f_day_stem: str, f_day_branch: str) -> list:
        m_ds, m_db = self._safe_str(m_day_stem), self._safe_str(m_day_branch)
        f_ds, f_db = self._safe_str(f_day_stem), self._safe_str(f_day_branch)
        results = []
        if not m_ds or not m_db or not f_ds or not f_db: return results
        is_cheon_hap = {m_ds, f_ds} in self.cheon_hap
        is_ji_hap = {m_db, f_db} in self.ji_hap
        if is_cheon_hap and is_ji_hap: results.append({"name": "천지합덕격", "desc": HONTAEK_SPECIAL_DB["천지합덕"]["desc"]})
        else:
            if is_cheon_hap: results.append({"name": "간합", "desc": "천간이 합을 이루어 부부간 정신적 교감과 뜻의 일치가 매우 깊습니다."})
            if is_ji_hap: results.append({"name": "지합", "desc": "지지가 합을 이루어 속궁합과 현실적인 생활 패턴이 완벽하게 융화됩니다."})
        if m_db in self.gwiin_map.get(f_ds, []) and f_db in self.gwiin_map.get(m_ds, []): results.append({"name": "교귀격", "desc": HONTAEK_SPECIAL_DB["교귀격"]["desc"]})
        if m_db == self.geonrok_map.get(f_ds) and f_db == self.geonrok_map.get(m_ds): results.append({"name": "교록격", "desc": HONTAEK_SPECIAL_DB["교록격"]["desc"]})
        return results

# ==========================================
# 🌟 이상형 자동 매칭 엔진 (기존 보존)
# ==========================================
class IdealPartnerEngine:
    def __init__(self, hontaek_engine: FengShuiHontaekEngine):
        self.hontaek = hontaek_engine
        self.samhap = {
            "申":["子","辰"], "子":["申","辰"], "辰":["申","子"],
            "亥":["卯","未"], "卯":["亥","未"], "未":["亥","卯"],
            "寅":["午","戌"], "午":["寅","戌"], "戌":["寅","午"],
            "巳":["酉","丑"], "酉":["巳","丑"], "丑":["巳","酉"]
        }
        self.wonjin = {"子":"未", "丑":"午", "寅":"酉", "卯":"申", "辰":"亥", "巳":"戌", "午":"丑", "未":"子", "申":"卯", "酉":"寅", "戌":"巳", "亥":"辰"}
        self.chung = {"子":"午", "丑":"未", "寅":"申", "卯":"酉", "辰":"戌", "巳":"亥", "午":"子", "未":"丑", "申":"寅", "酉":"卯", "戌":"辰", "亥":"巳"}
        self.tg_ideal_desc = {
            "비견": "당신은 누군가에게 일방적으로 억압받는 것을 견디지 못합니다. 친구처럼 동등하게 취미를 공유하고, 주도권 다툼 없이 서로의 영역과 독립성을 존중해 주는 편안한 동반자를 만나야 숨이 트입니다.",
            "겁재": "조용하고 평탄하기만 한 관계는 당신을 지루하게 만듭니다. 강한 주관과 승부욕을 갖추어 나를 끊임없이 자극하고 이끌어주며 긍정적인 경쟁 시너지를 내는 열정적인 파트너가 제격입니다.",
            "식신": "당신은 따뜻한 온기와 정서적 교감을 중시합니다. 다정다감한 성품으로 조건 없는 헌신과 사랑을 주며, 요리와 식도락을 함께 즐기며 일상의 행복을 누릴 수 있는 따뜻한 배우자가 완벽합니다.",
            "상관": "틀에 박힌 권위주의나 잔소리는 당신의 매력을 죽입니다. 재치와 유머 감각이 뛰어나며, 통통 튀는 아이디어로 지루할 틈 없이 당신의 삶에 활력을 불어넣어 주는 매력적인 연인에게 강하게 끌립니다.",
            "편재": "당신은 자유로운 영혼이자 큰 무대에서 활약해야 할 사람입니다. 좁은 우물에 당신을 구속하려는 사람보다는, 스케일이 크고 호탕하여 당신의 사회적 능력을 전폭적으로 지지해 주는 통 큰 파트너가 최상입니다.",
            "정재": "당신에게 가장 필요한 것은 삶의 흔들림 없는 닻입니다. 헛된 꿈을 좇기보다는 책임감이 매우 강하고 치밀하여 가계를 알뜰하게 꾸려가는, 평생 믿고 의지할 수 있는 성실한 배우자가 운명의 짝입니다.",
            "편관": "때로는 기댈 수 있는 거대한 바위 같은 존재가 필요합니다. 카리스마와 강한 리더십으로 당신을 험난한 외부의 위험으로부터 철저하게 보호하고 든든하게 리드해 주는 동반자를 만나야 안심합니다.",
            "정관": "당신은 상식과 도리가 통하는 평화로운 관계를 지향합니다. 감정 기복이 심한 사람보다는, 바르고 이성적이며 도덕적 규범을 잘 지켜 한평생 변함없는 신뢰를 유지할 수 있는 모범적인 배우자가 최고입니다.",
            "편인": "당신의 영혼은 꽤 깊고 예민합니다. 겉핥기식 대화보다는, 독특한 예술적 감각이나 영적 직관력을 지녀 굳이 말하지 않아도 내 깊은 마음속의 상처와 고독을 단숨에 꿰뚫어 보고 보듬어주는 소울메이트를 갈망합니다.",
            "정인": "당신은 상처받기 쉬운 여린 마음을 가졌습니다. 마치 어머니처럼 넓고 조건 없는 사랑으로, 당신의 부족한 허물과 실수마저도 넉넉하게 감싸 안아주며 언제든 돌아갈 수 있는 든든한 품이 되어주는 배우자가 필요합니다."
        }

    def _generate_real_life_manifestation(self, my_group: str, optimal_elements: str, day_tg: str) -> list:
        manifestations = []
        manifestations.append({"title": "함께 있을수록 에너지가 충전된다", "desc": f"서로가 같은 {my_group}의 생체 주파수를 공유하므로, 한 공간에 거주하거나 잠을 잘 때 기운이 엇갈리지 않습니다. 밖에서 방전된 체력이 배우자 옆에만 가면 이상하게 편안해지며 빠르게 회복됩니다."})
        manifestations.append({"title": "운의 막힘이 뚫리는 개운(開運) 효과", "desc": f"당신에게 절실히 필요한 [{optimal_elements}] 기운을 상대방이 듬뿍 채워줍니다. 결혼 전 풀리지 않던 진로나 금전 문제가, 신기하게도 이 파트너를 만난 직후부터 톱니바퀴 맞물리듯 술술 풀려나갑니다."})
        tg_focus = "주도권 없는 평등함" if day_tg in ["비견", "겁재"] else "조건 없는 따뜻한 보살핌" if day_tg in ["정인", "편인"] else "안정적인 현실 감각"
        manifestations.append({"title": "결정적 순간의 가치관 일치", "desc": f"배우자궁 성향({day_tg})이 완벽히 부합하므로, 주거지 이동이나 금전 문제 등 결정적인 순간에 서로 헛발질하지 않습니다. {tg_focus}을(를) 바탕으로 소모적인 감정싸움 없이 위기를 함께 극복해 냅니다."})
        return manifestations

    def find_optimal_partner(self, formatted_bazi: dict, user_year: int, gender: str, yongshin_data: dict) -> dict:
        day_stem = formatted_bazi.get("day", {}).get("stem", "-")
        day_branch = formatted_bazi.get("day", {}).get("branch", "-")
        year_branch = formatted_bazi.get("year", {}).get("branch", "-")
        day_tg = formatted_bazi.get("day", {}).get("branch_tg", "")
        if not day_tg or day_tg == "-" or day_tg == "일간": day_tg = "비견"

        my_gung = self.hontaek.calculate_honmyeong_gung(user_year, gender)
        my_group = my_gung.get("group", "알 수 없음")
        my_element = my_gung.get("element", "")
        group_desc = f"사람은 태어난 해에 따라 고유의 생체 주파수를 갖는데, 당신은 {my_element}의 기운을 띤 '{my_group}'에 속합니다. 반대 그룹을 만나면 AM/FM 라디오 주파수가 어긋나듯 일상 공간에서 서로의 기(氣)를 빨아먹고 화해(祸害)의 흉액이 발생합니다. 따라서 당신의 파트너는 반드시 당신과 동일한 주파수 대역인 '{my_group}'의 사람이어야만 생기(生氣)와 연년(延年)의 대길함을 누릴 수 있습니다."

        ideal_stem, ideal_branch = "", ""
        for pair in self.hontaek.cheon_hap:
            if day_stem in pair: ideal_stem = list(pair - {day_stem})[0]; break
        for pair in self.hontaek.ji_hap:
            if day_branch in pair: ideal_branch = list(pair - {day_branch})[0]; break
        ideal_ilju = f"{ideal_stem}{ideal_branch} 일주" if ideal_stem and ideal_branch else "기운 혼합형"
        ilju_desc = f"명리학에서 천간(天干)은 생각과 가치관을, 지지(地支)는 현실과 육체를 의미합니다. 당신의 일주({day_stem}{day_branch})와 하늘 땅이 모두 완벽하게 맞물리는 이 일주를 가진 사람은, 굳이 말하지 않아도 영혼이 통하고 현실적 속궁합까지 들어맞는 '천지합덕격(天地合德格)'의 100점짜리 인연입니다."

        best_zodiacs = []
        for z in self.hontaek.gwiin_map.get(day_stem, []):
            if z: best_zodiacs.append({"zodiac": z+"띠", "reason": "천을귀인(하늘의 수호성)"})
        rok = self.hontaek.geonrok_map.get(day_stem, "")
        if rok: best_zodiacs.append({"zodiac": rok+"띠", "reason": "교록격(마르지 않는 재물)"})
        if ideal_branch: best_zodiacs.append({"zodiac": ideal_branch+"띠", "reason": "지합(단단한 현실 결속)"})
        for z in self.samhap.get(year_branch, []):
            if z: best_zodiacs.append({"zodiac": z+"띠", "reason": "삼합(흔들림 없는 가치관)"})

        unique_best = []
        seen = set()
        for item in best_zodiacs:
            if item["zodiac"] not in seen:
                unique_best.append(item)
                seen.add(item["zodiac"])

        worst_zodiacs = []
        w_z = self.wonjin.get(year_branch, "")
        if w_z: worst_zodiacs.append({"zodiac": w_z+"띠", "reason": "원진살(끝없는 원망과 의심)"})
        c_z = self.chung.get(year_branch, "")
        if c_z: worst_zodiacs.append({"zodiac": c_z+"띠", "reason": "상충살(정면충돌과 파경)"})

        ideal_elements = "균형잡힌 오행"
        if isinstance(yongshin_data, dict):
            y_str = str(yongshin_data.get("yongshin", "")).replace("None", "").strip()
            h_str = str(yongshin_data.get("huishin", "")).replace("None", "").strip()
            elements_arr = []
            if y_str: elements_arr.append(f"{y_str}")
            if h_str: elements_arr.append(f"{h_str}")
            if elements_arr: ideal_elements = ", ".join(elements_arr)

        ideal_elements_desc = f"사주 원국 분석 결과, 현재 당신의 삶에 가장 절실하게 필요한 절대적 기운은 [{ideal_elements}]입니다. 이 기운이 메마른 사람을 만나면 도끼로 나무를 치는 듯한 상극(相剋) 현상으로 함께 있을수록 피가 마릅니다. 반면 이 기운을 듬뿍 가진 사람을 만나면, 당신의 억부와 조후가 완벽히 보완되며 막혔던 재물운과 건강이 폭발적으로 트이게 됩니다."
        ideal_personality = self.tg_ideal_desc.get(day_tg, "서로를 존중하고 헌신하는 따뜻한 배우자")
        manifestations = self._generate_real_life_manifestation(my_group, ideal_elements, day_tg)
        conclusion = f"종합하자면, 고객님의 운명의 짝은 막연히 성격이 좋은 사람이 아닙니다. 역학적 설계도상 반드시 생체 주파수({my_group})가 일치하고, 당신의 텅 빈 헛점([{ideal_elements}])을 메워주는 사주 구조를 가져야만 톱니바퀴의 마모 없이 백년해로가 가능합니다. 의구심을 가질 필요 없이, 우주의 원리상 이 조건에 부합하는 파트너야말로 득(得)이 흉(凶)을 덮고 당신을 살리는 진짜 인연입니다."

        if gender == 'M':
            role = "정재(正財)와 식신(食神)"
            role_desc = "남성에게 최고의 길신인 바르고 알뜰한 아내(정재)와, 다정다감하게 자손을 번창시키는 넉넉한 기운(식신)을 가진 여성이 당신의 완벽한 짝입니다."
        else:
            role = "정관(正官)과 정인(正印)"
            role_desc = "여성에게 최고의 길신인 명예롭고 책임감 강한 반듯한 남편(정관)과, 조건 없는 사랑으로 든든한 울타리가 되어주는 기운(정인)을 가진 남성이 당신의 완벽한 짝입니다."

        return {
            "dongseo_group": my_group,
            "dongseo_desc": group_desc,
            "ideal_ilju": ideal_ilju,
            "ideal_ilju_desc": ilju_desc,
            "best_zodiacs": unique_best,
            "worst_zodiacs": worst_zodiacs,
            "ideal_elements": ideal_elements,
            "ideal_elements_desc": ideal_elements_desc,
            "day_tg": day_tg,
            "ideal_personality": ideal_personality,
            "manifestations": manifestations, 
            "conclusion": conclusion,
            "ideal_role": role,
            "ideal_role_desc": role_desc
        }

# ==========================================
# 3. FastAPI 어플리케이션 및 라우터 설정
# ==========================================
app = FastAPI(title="명리 & 혼택촬요 마스터 API 서버", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

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
ideal_partner_engine = IdealPartnerEngine(hontaek_engine) 
dict_engine = DictionaryEngine()

class UserInfo(BaseModel):
    name: str = Field(...)
    gender: str = Field(..., pattern="^[MF]$")
    birth_date: str = Field(...)
    is_lunar: bool = Field(False)
    current_age: int = Field(...)
    longitude: float = Field(127.0)

class SajuRequest(BaseModel):
    user: UserInfo

class GunghapRequest(BaseModel):
    groom: UserInfo
    bride: UserInfo
    target_date: Optional[str] = Field(None)

def _get_year_from_date(date_str: str) -> int:
    try: return datetime.strptime(date_str, "%Y-%m-%d %H:%M").year
    except: return 1984

def _get_solar_datetime(date_str: str, is_lunar: bool) -> datetime:
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    if is_lunar:
        calendar = KoreanLunarCalendar()
        calendar.setLunarDate(dt.year, dt.month, dt.day, isIntercalation=False)
        return datetime.strptime(f"{calendar.SolarIsoFormat()} {dt.strftime('%H:%M')}", "%Y-%m-%d %H:%M")
    return dt

def _build_formatted_bazi(bazi_chars: dict, day_stem: str) -> dict:
    pillars = ["year", "month", "day", "hour"]
    formatted = {}
    for pillar in pillars:
        pillar_chars = bazi_chars.get(f"{pillar}_pillar", "--")
        stem, branch = (pillar_chars[0], pillar_chars[1]) if len(pillar_chars) == 2 else ("-", "-")
        formatted[pillar] = {"stem": stem, "branch": branch, "stem_tg": mechanics_engine.get_ten_god(day_stem, stem) if stem != "-" else "-", "branch_tg": mechanics_engine.get_ten_god(day_stem, branch) if branch != "-" else "-", "wunseong": mechanics_engine.get_12wunseong(day_stem, branch) if branch != "-" else "-"}
    return formatted

@app.post("/api/v1/saju")
async def get_personal_saju(req: SajuRequest):
    try:
        dt = _get_solar_datetime(req.user.birth_date, req.user.is_lunar)
        astro_res = astro_engine.calculate_bazi(dt, req.user.gender, longitude=req.user.longitude)
        bazi_chars = astro_res.get("bazi", {})
        
        day_stem = bazi_chars.get("day_pillar", "--")[0]
        formatted_bazi = _build_formatted_bazi(bazi_chars, day_stem)
        stems_list = [formatted_bazi[p]["stem"] for p in formatted_bazi]
        branches_list = [formatted_bazi[p]["branch"] for p in formatted_bazi]
        
        element_dist = mechanics_engine.get_five_elements_distribution(stems_list, branches_list)
        hidden_stems = {p: mechanics_engine.get_hidden_stems(formatted_bazi[p]["branch"]) for p in formatted_bazi}
        branches_dict = {p: formatted_bazi[p]["branch"] for p in formatted_bazi}
        stems_dict = {p: formatted_bazi[p]["stem"] for p in formatted_bazi}

        tonggeun_data = mechanics_engine.check_tonggeun(day_stem, branches_dict)
        strength_data = yongshin_engine.determine_strength(formatted_bazi)
        
        local_element_map = {
            "甲": "목", "乙": "목", "寅": "목", "卯": "목",
            "丙": "화", "丁": "화", "巳": "화", "午": "화",
            "戊": "토", "己": "토", "辰": "토", "戌": "토", "丑": "토", "未": "토",
            "庚": "금", "辛": "금", "申": "금", "酉": "금",
            "壬": "수", "癸": "수", "亥": "수", "子": "수"
        }
        producing_map = {"목": "수", "화": "목", "토": "화", "금": "토", "수": "금"}
        
        if isinstance(strength_data, dict):
            day_element = local_element_map.get(day_stem)
            ally_pct = 0
            
            if day_element:
                ally_elements = [day_element, producing_map.get(day_element)]
                weights = {
                    "year": {"stem": 5, "branch": 10},
                    "month": {"stem": 10, "branch": 30},
                    "day": {"stem": 10, "branch": 15},
                    "hour": {"stem": 10, "branch": 10}
                }
                
                ally_score = 0
                for pillar in ["year", "month", "day", "hour"]:
                    s_char = formatted_bazi[pillar]["stem"]
                    b_char = formatted_bazi[pillar]["branch"]
                    
                    if local_element_map.get(s_char) in ally_elements:
                        ally_score += weights[pillar]["stem"]
                    if local_element_map.get(b_char) in ally_elements:
                        ally_score += weights[pillar]["branch"]
                        
                ally_pct = ally_score
            
            status_text = strength_data.get("status", strength_data.get("strength", ""))
            
            if "극신강" in status_text or "태강" in status_text:
                ally_pct = max(ally_pct, 75)
                strength_desc = "아군의 기운이 압도적인 [극신강(極身强)] 사주입니다. 단순 오행의 개수를 넘어 계절(월지)과 뿌리의 힘을 완벽히 장악했습니다. 고집을 줄이고 기운을 밖으로 발산하는 환경이 필요합니다."
            elif "신강" in status_text:
                ally_pct = max(ally_pct, 55)
                strength_desc = "아군의 기운이 든든한 [신강(身强)] 사주입니다. 주체성과 독립심이 뛰어나며, 타인에게 의존하기보다 자기 주도적으로 삶을 개척하기 좋은 튼튼한 구조입니다."
            elif "극신약" in status_text or "태약" in status_text:
                ally_pct = min(ally_pct, 25)
                strength_desc = "적군의 기운에 심하게 억눌린 [극신약(極身弱)] 사주입니다. 글자 수가 겉보기에 많아도 계절(월지)의 주도권을 뺏겨 힘이 매우 약합니다. 흐름에 유연하게 순응하거나 든든한 조력자에게 기대는 지혜가 필요합니다."
            elif "신약" in status_text:
                ally_pct = min(ally_pct, 45)
                strength_desc = "적군의 기운이 다소 강한 [신약(身弱)] 사주입니다. 내 힘이 빠져나가고 있으니, 타인과의 협력, 든든한 조직, 또는 인성(배움/자격증)을 통해 힘을 보충해야 유리합니다."
            else:
                ally_pct = max(40, min(ally_pct, 60))
                strength_desc = "아군과 적군의 세력이 균형을 이루는 [중화(中和)] 사주입니다. 운의 흐름에 따라 유연하게 대처할 수 있는 안정적인 구조입니다."

            enemy_pct = 100 - ally_pct
            strength_data["ally_pct"] = ally_pct
            strength_data["enemy_pct"] = enemy_pct
            strength_data["desc"] = strength_desc

        yongshin_data = yongshin_engine.determine_yongshin(formatted_bazi, strength_data)
        geokguk_data = yongshin_engine.determine_geokguk(formatted_bazi, hidden_stems)
        special_stars = dynamics_engine.scan_special_stars(stems_dict, branches_dict, req.user.gender)
        disasters = dynamics_engine.scan_disasters(branches_list, req.user.gender)
        month_stem = formatted_bazi["month"]["stem"]
        month_branch = formatted_bazi["month"]["branch"]
        daewun_data = mechanics_engine.get_daewun_sequence(req.user.gender, formatted_bazi["year"]["stem"], month_stem, month_branch)
        secret_data = secret_engine.get_secrets(formatted_bazi, daewun_data, req.user.current_age)
        health_data = practical_engine.analyze_health(element_dist)
        career_data = practical_engine.analyze_career(geokguk_data, yongshin_data, req.user.gender)

        # ---------------------------------------------------------
        # 🚨 [최종 복원 튜닝 구역] 대운 및 세운 프론트엔드 맞춤 매핑
        # ---------------------------------------------------------
        now = datetime.now()
        now_bazi = astro_engine.calculate_bazi(now, req.user.gender, longitude=127.0).get("bazi", {})
        
        # 1. 10년 대운(daewun_data) 정밀 파싱 (빈 한자 추출 해결)
        daewun_timeline = []
        if isinstance(daewun_data, dict) and "timeline" in daewun_data:
            daewun_timeline = daewun_data["timeline"]
        elif isinstance(daewun_data, list):
            daewun_timeline = daewun_data

        daewun_flow_payload = None
        if daewun_timeline and len(daewun_timeline) > 0:
            pillars_arr = []
            ages_arr = []
            current_daewun = daewun_timeline[0]
            
            for dw in daewun_timeline:
                if isinstance(dw, dict):
                    # stem, branch 추출 및 ganji 조립
                    s = dw.get("stem", "-")
                    b = dw.get("branch", "-")
                    ganji = s + b if s != "-" and b != "-" else dw.get("ganji", "--")
                    pillars_arr.append(ganji)
                    
                    try:
                        start_age = int(dw.get("age", dw.get("start_age", 0)))
                    except:
                        start_age = 0
                    ages_arr.append(start_age)
                    
                    # 현재 나이가 속한 대운 찾기
                    if start_age <= req.user.current_age < start_age + 10:
                        current_daewun = dw
            
            # 현재 대운 분석 텍스트 생성
            dw_s = current_daewun.get("stem", "-")
            dw_b = current_daewun.get("branch", "-")
            dw_ganji = dw_s + dw_b if dw_s != "-" and dw_b != "-" else current_daewun.get("ganji", "--")
            dw_age = int(current_daewun.get("age", current_daewun.get("start_age", 0)))
            
            frontend_payload = {}
            if len(dw_ganji) >= 2 and dw_ganji != "--":
                dw_branch = dw_ganji[1]
                dw_tg = mechanics_engine.get_ten_god(day_stem, dw_branch) if day_stem != "-" else "-"
                daewun_result = unse_engine.analyze_daewun(formatted_bazi, dw_branch, dw_tg, yongshin_data)
                
                frontend_payload = {
                    "title": f"현재 대운: {dw_age}세 ~ {dw_age+9}세 ({dw_ganji})",
                    "subtitle": daewun_result.get("overall_status"),
                    "progress_message": daewun_result.get("overall_desc")
                }
            else:
                frontend_payload = {
                    "title": "현재 대운 분석 불가",
                    "subtitle": "데이터 누락",
                    "progress_message": "엔진에서 대운 간지(干支) 데이터를 정상적으로 반환하지 않았습니다."
                }

            daewun_flow_payload = {
                "daewun_flow": {
                    "pillars": pillars_arr,
                    "ages": ages_arr
                },
                "current_status": {
                    "active_daewun": { "started_at_age": dw_age },
                    "frontend_ui_payload": frontend_payload
                }
            }

        # 2. 실전 운세 스캐너 조립 (UnseScanner.jsx 용 객체화 + 12운성 테마 주입)
        year_pillar = now_bazi.get("year_pillar", "--")
        year_branch = year_pillar[1] if len(year_pillar) >= 2 else "-"
        year_tg = mechanics_engine.get_ten_god(day_stem, year_branch) if year_branch != "-" else "-"
        sewun_result = unse_engine.analyze_sewun(formatted_bazi, year_branch, year_tg, yongshin_data)
        sewun_result['title'] = f"{now.year}년 ({year_pillar}) 올해의 운세"
        
        month_pillar = now_bazi.get("month_pillar", "--")
        month_branch = month_pillar[1] if len(month_pillar) >= 2 else "-"
        month_tg = mechanics_engine.get_ten_god(day_stem, month_branch) if month_branch != "-" else "-"
        wolgeon_result = unse_engine.analyze_wolgeon(formatted_bazi, month_branch, month_tg, yongshin_data)
        wolgeon_result['title'] = f"{now.month}월 ({month_pillar}) 이달의 운세"
        
        day_curr_pillar = now_bazi.get("day_pillar", "--")
        day_curr_branch = day_curr_pillar[1] if len(day_curr_pillar) >= 2 else "-"
        day_curr_tg = mechanics_engine.get_ten_god(day_stem, day_curr_branch) if day_curr_branch != "-" else "-"
        iljin_result = unse_engine.analyze_iljin(formatted_bazi, day_curr_branch, day_curr_tg, yongshin_data)
        iljin_result['title'] = f"오늘 ({day_curr_pillar}일) 하루 일진"
        
        wunseong_name = mechanics_engine.get_12wunseong(day_stem, year_branch) if year_branch != "-" else "-"
        wunseong_desc = ""
        try:
            wunseong_desc = WUNSEONG_DESC.get(wunseong_name, f"올해는 [{wunseong_name}]의 에너지가 작용하는 시기입니다.")
        except NameError:
             wunseong_desc = f"올해는 [{wunseong_name}]의 에너지가 작용하는 시기입니다."
        
        # 향후 10년 세운 흐름 자동 생성 로직
        sewun_flow_arr = []
        base_year = now.year
        for i in range(10):
            t_year = base_year + i
            offset = t_year - 1984 # 1984(갑자) 기준 단순 계산
            s_char = "甲乙丙丁戊己庚辛壬癸"[offset % 10]
            b_char = "子丑寅卯辰巳午未申酉戌亥"[offset % 12]
            s_tg = mechanics_engine.get_ten_god(day_stem, s_char) if day_stem != "-" else "-"
            b_tg = mechanics_engine.get_ten_god(day_stem, b_char) if day_stem != "-" else "-"
            
            sewun_flow_arr.append({
                "year": t_year,
                "ganji": s_char + b_char,
                "stem": s_char,
                "branch": b_char,
                "stem_tg": s_tg,
                "branch_tg": b_tg
            })

        unse_timeline = {
            "sewun": sewun_result, 
            "wolgeon": wolgeon_result, 
            "iljin": iljin_result,
            "current_sewun": {
                "year": now.year, 
                "ganji": year_pillar, 
                "wunseong": {
                    "name": wunseong_name, 
                    "desc": wunseong_desc
                }
            },
            "sewun_flow": sewun_flow_arr
        }
        # ---------------------------------------------------------

        original_dt = datetime.strptime(req.user.birth_date, "%Y-%m-%d %H:%M")
        lunar_m, lunar_d = original_dt.month, original_dt.day
        if not req.user.is_lunar:
            cal = KoreanLunarCalendar()
            cal.setSolarDate(original_dt.year, original_dt.month, original_dt.day)
            lunar_m, lunar_d = cal.lunarMonth, cal.lunarDay

        y_branch = formatted_bazi["year"]["branch"]
        h_branch = formatted_bazi["hour"]["branch"]
        dangsaju_data = dangsaju_engine.calculate_12_stars(y_branch, lunar_m, lunar_d, h_branch)

        user_year = _get_year_from_date(req.user.birth_date)
        optimal_partner = ideal_partner_engine.find_optimal_partner(formatted_bazi, user_year, req.user.gender, yongshin_data)

        return {
            "status": "success",
            "metadata": {
                "name": req.user.name,
                "gender": "건명(남성)" if req.user.gender == 'M' else "곤명(여성)",
                "corrected_time": astro_res.get("corrected_time")
            },
            "bazi_matrix": formatted_bazi,
            "daewun_analysis": daewun_flow_payload if daewun_flow_payload else {"daewun_flow": {"pillars": [], "ages": []}},  
            "unse_analysis": unse_timeline,      
            "daewun_data": daewun_data,
            "unse_timeline": unse_timeline,
            "dangsaju_data": dangsaju_data,
            "elements_distribution": element_dist,
            "optimal_partner": optimal_partner,
            "core_analysis": {
                "strength": strength_data,
                "tonggeun": tonggeun_data, 
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
    try:
        m_dt = _get_solar_datetime(req.groom.birth_date, req.groom.is_lunar)
        f_dt = _get_solar_datetime(req.bride.birth_date, req.bride.is_lunar)
        
        m_bazi_res = astro_engine.calculate_bazi(m_dt, req.groom.gender, longitude=req.groom.longitude).get("bazi", {})
        f_bazi_res = astro_engine.calculate_bazi(f_dt, req.bride.gender, longitude=req.bride.longitude).get("bazi", {})

        m_day_stem, m_day_branch = m_bazi_res.get("day_pillar", "--")[0], m_bazi_res.get("day_pillar", "--")[1]
        f_day_stem, f_day_branch = f_bazi_res.get("day_pillar", "--")[0], f_bazi_res.get("day_pillar", "--")[1]
        m_stems, m_branches = [m_bazi_res.get(p, "--")[0] for p in ["year_pillar", "month_pillar", "day_pillar", "hour_pillar"]], [m_bazi_res.get(p, "--")[1] for p in ["year_pillar", "month_pillar", "day_pillar", "hour_pillar"]]
        f_stems, f_branches = [f_bazi_res.get(p, "--")[0] for p in ["year_pillar", "month_pillar", "day_pillar", "hour_pillar"]], [f_bazi_res.get(p, "--")[1] for p in ["year_pillar", "month_pillar", "day_pillar", "hour_pillar"]]
        
        m_elements = mechanics_engine.get_five_elements_distribution(m_stems, m_branches)
        f_elements = mechanics_engine.get_five_elements_distribution(f_stems, f_branches)

        element_report = []
        for el in ["목", "화", "토", "금", "수"]:
            m_cnt, f_cnt = m_elements.get(el, 0), f_elements.get(el, 0)
            if m_cnt >= 3 and f_cnt == 0: element_report.append(f"【오행 불균형】 신랑에게 넘치는 [{el}] 기운을 신부가 품어주지 못해 아쉽습니다. 신랑의 독단적인 고집을 경계해야 합니다.")
            elif m_cnt == 0 and f_cnt >= 3: element_report.append(f"【완벽한 상호보완】 신랑에게 결핍된 [{el}] 기운을 신부가 풍부하게 채워줍니다! 훌륭한 톱니바퀴 조후 궁합입니다.")
            elif f_cnt >= 3 and m_cnt == 0: element_report.append(f"【오행 불균형】 신부에게 넘치는 [{el}] 기운을 신랑이 수용하지 못해 다소 아쉽습니다. 신부의 감정 기복을 잘 보듬어 주어야 합니다.")
            elif f_cnt == 0 and m_cnt >= 3: element_report.append(f"【완벽한 상호보완】 신부에게 메마른 [{el}] 기운을 신랑이 강력하게 보완해 주어, 신부의 육체적 건강과 정신적 안정이 크게 올라갑니다.")
        element_conclusion = "\n\n".join(element_report) if element_report else "두 분 모두 특정 오행으로 크게 치우치지 않은 평탄하고 안정적인 구조를 지녀, 극단적인 충돌 없이 무난하게 화합할 수 있는 결합입니다."

        day_pillar_report = []
        
        branch_clash = {"子":"午", "丑":"未", "寅":"申", "卯":"酉", "辰":"戌", "巳":"亥", "午":"子", "未":"丑", "申":"寅", "酉":"卯", "戌":"辰", "亥":"巳"}
        
        if {m_day_stem, f_day_stem} in hontaek_engine.cheon_hap: day_pillar_report.append("【천간합(干合)】 정신적 교감이 완벽합니다. 말하지 않아도 서로의 이상과 가치관을 깊이 이해하는 천생연분입니다.")
        if {m_day_branch, f_day_branch} in hontaek_engine.ji_hap: day_pillar_report.append("【지합(支合)】 땅의 뿌리가 굳게 얽히는 길상입니다. 현실적·육체적 속궁합이 훌륭하며, 가정을 지키는 끈끈한 결속력이 압도적입니다.")
        wonjin_pairs = [{"子", "未"}, {"丑", "午"}, {"寅", "酉"}, {"卯", "申"}, {"辰", "亥"}, {"巳", "戌"}]
        if {m_day_branch, f_day_branch} in wonjin_pairs: day_pillar_report.append("【일지 원진살(怨嗔殺)】 안방(부부궁)에 까닭 없는 원망과 히스테리가 서려 있습니다. 겉으로는 화목해 보여도 속으로는 서로를 향한 집착과 오해가 쌓이기 쉬우니(천심육해), 각자의 취미를 철저히 존중하고 거리를 두는 개운법이 필요합니다.")
        
        if branch_clash.get(m_day_branch) == f_day_branch or branch_clash.get(f_day_branch) == m_day_branch: day_pillar_report.append("【일지 충(沖)】 부부의 뿌리가 정면으로 부딪혀 깨지는 흉합입니다. 성격 대립과 가치관 충돌이 잦으니, 주말부부나 맞벌이 등 서로의 일상을 철저히 분리해야 파국을 막을 수 있습니다.")
        if not day_pillar_report: day_pillar_report.append("부부궁(안방)에 서로를 깨뜨리거나 원망하는 치명적 흉살(충/원진)이 감지되지 않아, 평탄하고 무던하게 백년해로할 수 있는 인연입니다.")

        m_year, f_year = _get_year_from_date(req.groom.birth_date), _get_year_from_date(req.bride.birth_date)
        
        dongseo_gunghap = hontaek_engine.evaluate_hontaek_gunghap(m_year, f_year, req.groom.name, req.bride.name)
        
        special_gunghap = hontaek_engine.analyze_special_gunghap(m_day_stem, m_day_branch, f_day_stem, f_day_branch)
        m_honmyeong = hontaek_engine.calculate_honmyeong_gung(m_year, "M")
        fengshui_dirs = hontaek_engine.get_auspicious_directions(m_honmyeong.get("number", 1))

        taekil_result = None
        if req.target_date:
            t_dt = datetime.strptime(req.target_date, "%Y-%m-%d %H:%M")
            t_bazi = astro_engine.calculate_bazi(t_dt, "M", longitude=req.groom.longitude).get("bazi", {})
            t_stem, t_branch = t_bazi.get("day_pillar", "--")[0], t_bazi.get("day_pillar", "--")[1]
            f_year_branch, m_year_branch = f_bazi_res.get("year_pillar", "--")[1], m_bazi_res.get("year_pillar", "--")[1]
            
            calendar = KoreanLunarCalendar()
            calendar.setSolarDate(t_dt.year, t_dt.month, t_dt.day)
            t_lunar_month = calendar.lunarMonth

            steps = []
            final_status = "PASS"
            
            gachwi = hontaek_engine.get_gachwi_gilwol(f_year_branch)
            if t_lunar_month in gachwi.get("best_months", []): steps.append({"step": "1관문: 용월법 (달의 선택)", "status": "대리월 (大吉)", "reason": f"음력 {t_lunar_month}월은 신부의 띠({f_year_branch})를 기준으로 자손이 번창하고 양가 부모에게 흉함이 전혀 없는 최고의 길월(吉月)입니다."})
            elif t_lunar_month in gachwi.get("good_months", []): steps.append({"step": "1관문: 용월법 (달의 선택)", "status": "소리월 (吉)", "reason": f"음력 {t_lunar_month}월은 신부({f_year_branch}띠) 기준 무난하고 평탄하게 쓰일 수 있는 차선책의 길월입니다."})
            else:
                final_status = "FAIL"
                steps.append({"step": "1관문: 용월법 (달의 선택)", "status": "흉월 (大凶)", "reason": f"음력 {t_lunar_month}월은 신부({f_year_branch}띠) 기준 방부/방녀부모 등에 해당하는 흉월(凶月)입니다. 신랑이나 친정 부모에게 화가 미칠 수 있으니 택월을 다시 하십시오."})

            gojin_res = hontaek_engine.check_taekil_gojin_gwasuk(m_year_branch, f_year_branch, t_branch)
            if gojin_res["is_banned"]:
                final_status = "FAIL"
                steps.append({"step": "2관문: 고진/과숙 (고독살)", "status": "대흉 (大凶)", "reason": gojin_res["reason"]})
            else: steps.append({"step": "2관문: 고진/과숙 (고독살)", "status": "안전 (PASS)", "reason": f"희망일({t_branch}일)은 두 분 모두에게 상부살이나 홀아비/과부살이 끼지 않는 맑은 날입니다."})

            if branch_clash.get(m_day_branch) == t_branch:
                final_status = "FAIL"
                steps.append({"step": "3관문: 사주 원국 沖 충돌", "status": "대흉 (大凶)", "reason": f"희망일({t_branch}일)이 신랑의 일지(부부궁: {m_day_branch})를 정면으로 깨부수는 치명적인 흉일입니다. 혼례 중 사고나 훗날 파혼의 위험이 따릅니다."})
            elif branch_clash.get(f_day_branch) == t_branch:
                final_status = "FAIL"
                steps.append({"step": "3관문: 사주 원국 沖 충돌", "status": "대흉 (大凶)", "reason": f"희망일({t_branch}일)이 신부의 일지(부부궁: {f_day_branch})를 정면으로 깨부수는 치명적인 흉일입니다. 반드시 다른 날 고르십시오."})
            else: steps.append({"step": "3관문: 사주 원국 沖 충돌", "status": "안전 (PASS)", "reason": "두 분의 사주 기둥과 희망일이 파괴적으로 부딪히지 않고 무던하게 흘러갑니다."})

            m_tg = mechanics_engine.get_ten_god(m_day_stem, t_stem)
            f_tg = mechanics_engine.get_ten_god(f_day_stem, t_stem)
            
            good_stars = []
            if m_tg in ["정재", "식신", "정관", "정인"]: good_stars.append(f"신랑에게 {m_tg}(안정된 아내, 재물, 명예, 보호막)")
            if f_tg in ["정관", "식신", "정재", "정인"]: good_stars.append(f"신부에게 {f_tg}(반듯한 남편, 다산, 평안)")
            
            bad_stars = []
            if m_tg in ["겁재", "편관", "상관"]: bad_stars.append(f"신랑에게 {m_tg}(재물 분탈, 억압, 불화)")
            if f_tg in ["상관", "편관", "겁재"]: bad_stars.append(f"신부에게 {f_tg}(남편 극함, 가부장적 억압, 다툼)")

            if good_stars:
                steps.append({"step": "4관문: 일진(日辰) 길흉신 강림", "status": "대길 (大吉)", "reason": f"우주의 축복이 쏟아지는 날입니다! 이 날은 {', '.join(good_stars)}의 길신(吉神) 에너지가 혼례식장에 가득 채워져, 흉살마저 덮어버리는 훌륭한 추길(趨吉)의 작용을 합니다."})
            elif bad_stars:
                steps.append({"step": "4관문: 일진(日辰) 길흉신 강림", "status": "주의 (WARNING)", "reason": f"결혼을 진행하기엔 다소 거친 기운이 감돕니다. 이 날은 {', '.join(bad_stars)}의 흉포한 에너지가 섞여 있으니, 혼례 진행 중 다툼이 생기지 않도록 각별히 언행을 조심해야 합니다."})
            else:
                steps.append({"step": "4관문: 일진(日辰) 길흉신 강림", "status": "무난 (PASS)", "reason": "이 날은 특별히 부부를 크게 돕는 길신도, 크게 해치는 흉신도 없는 무난하고 고요한 평일입니다."})

            taekil_result = {
                "target_date": req.target_date,
                "final_status": final_status,
                "conclusion": "모든 흉살을 피해가고 우주의 길신이 강림하는 하늘이 내린 완벽한 길일입니다. 이 날 식을 올리십시오." if final_status == "PASS" else "절명, 상부살, 충(沖) 등 치명적인 흉액이 도사리고 있는 날입니다. 이유를 확인하시고 즉각 다른 길일을 모색하십시오.",
                "steps": steps
            }

        return {
            "status": "success",
            "deep_analysis": {
                "elements_synergy": element_conclusion, 
                "day_pillar_synergy": day_pillar_report
            },
            "hontaek_summary": {
                "dongseo_gunghap": dongseo_gunghap,
                "special_gunghap": special_gunghap
            },
            "fengshui_advice": {
                "base_gung": m_honmyeong, 
                "directions": fengshui_dirs
            },
            "taekil_validation": taekil_result if taekil_result else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"궁합/혼택 연산 중 오류 발생: {str(e)}")

@app.get("/api/v1/dictionary")
async def search_dictionary(query: str, category: Optional[str] = None):
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