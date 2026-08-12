# logic_practical.py

class PracticalEngine:
    def __init__(self):
        # 1. 오행별 건강/질병 매핑 DB
        self.health_map = {
            "목": {"organ": "간, 담낭, 신경계", "weak": "만성 피로, 신경쇠약, 우울증, 시력 저하", "excess": "간 수치 상승, 근육 뭉침, 분노 조절 어려움"},
            "화": {"organ": "심장, 소장, 혈관", "weak": "수족냉증, 저혈압, 무기력, 심장 두근거림", "excess": "고혈압, 심혈관 질환, 다혈질, 불면증"},
            "토": {"organ": "위장, 비장, 소화기", "weak": "소화불량, 위염, 식욕 부진, 피부 트러블", "excess": "비만, 당뇨, 위궤양, 세포/종양 질환"},
            "금": {"organ": "폐, 대장, 호흡기", "weak": "천식, 비염, 잦은 감기, 장 트러블", "excess": "호흡기 건조, 변비, 관절/뼈 질환"},
            "수": {"organ": "신장, 방광, 생식기", "weak": "신장 기능 저하, 생식기 질환, 부종, 호르몬 불균형", "excess": "신장 결석, 냉증, 우울감, 산부인과/전립선 질환"}
        }

        # 2. 십신(격국) 기반 현대 직업 매핑 DB
        self.career_map = {
            "비견": {"style": "독립형 전문가", "jobs": "프리랜서, 1인 기업가, 운동선수, 지점장, 독자적 기술직"},
            "겁재": {"style": "승부사 및 투자가", "jobs": "M&A 전문가, 펀드매니저, 프로게이머, 경쟁이 치열한 영업직"},
            "식신": {"style": "장인 및 연구가", "jobs": "연구원, 셰프, 개발자(IT), 작가, 제조업, 엔지니어"},
            "상관": {"style": "크리에이터 및 언변가", "jobs": "마케터, 유튜버/방송인, 강사, 로이어(변호사), 디자이너"},
            "편재": {"style": "사업가 및 무역가", "jobs": "글로벌 무역, 부동산 개발, 플랫폼 사업가, 유통/물류업"},
            "정재": {"style": "금융가 및 관리자", "jobs": "은행원, 회계사, 재무 관리자, 공기업, 안정적인 프랜차이즈"},
            "편관": {"style": "특수직 및 카리스마 리더", "jobs": "군인, 경찰, 검찰, 외과의사, 스타트업 CEO, 리스크 관리자"},
            "정관": {"style": "행정가 및 조직인", "jobs": "고위 공무원, 대기업 임원, 행정직, 규정/감사 부서"},
            "편인": {"style": "전략가 및 기획자", "jobs": "기획자, 프로듀서, 종교/철학가, 정신과 의사, 예술 감독"},
            "정인": {"style": "교육가 및 학자", "jobs": "교수, 교사, 문서/부동산 임대업, 학원 사업, 출판업"}
        }

    def analyze_health(self, elements_dist: dict) -> list:
        """
        [헬스케어 질병 스캐너]
        오행의 분포(개수)를 분석하여 과다(3개 이상)하거나 
        고립/태약(0개)한 오행을 찾아 취약한 장기를 진단합니다.
        """
        health_warnings = []
        
        for element, count in elements_dist.items():
            if count >= 3:
                data = self.health_map[element]
                health_warnings.append({
                    "element": element,
                    "status_code": "과다", # 🚨 프론트엔드가 텍스트 대신 이 코드로 조건 판별
                    "status": "과다 (기운이 너무 강해 병이 됨)",
                    "organ": data["organ"],
                    "symptom": data["excess"],
                    "advice": f"[{element}]의 기운이 사주에 너무 쏠려 있어 {data['organ']} 쪽에 열성(熱性) 질환이나 과부하가 올 수 있습니다. 꾸준한 검진이 필요합니다."
                })
            elif count == 0:
                data = self.health_map[element]
                health_warnings.append({
                    "element": element,
                    "status_code": "고립(無)", # 🚨 프론트엔드가 텍스트 대신 이 코드로 조건 판별
                    "status": "고립/태약 (기운이 없어 병이 됨)",
                    "organ": data["organ"],
                    "symptom": data["weak"],
                    "advice": f"사주 원국에 [{element}]의 기운이 메말라 있어 {data['organ']} 기능이 선천적으로 약할 수 있습니다. 해당 부위의 면역력 관리에 각별히 신경 쓰십시오."
                })
                
        # 만약 심각한 불균형이 없다면 무난한 텍스트 추가
        if not health_warnings:
            health_warnings.append({
                "element": "종합",
                "status_code": "양호", # 🚨 안전 플래그
                "status": "오행 균형 양호",
                "organ": "전신",
                "symptom": "특별한 선천적 취약점 없음",
                "advice": "오행의 개수가 비교적 골고루 분포되어 있어 선천적인 장기의 균형이 훌륭합니다. 규칙적인 생활만 유지하시면 큰 병 없이 건강을 누릴 수 있습니다."
            })
            
        return health_warnings

    def analyze_career(self, geokguk_data: dict, yongshin_data: dict) -> dict:
        """
        [현대적 직업/적성 큐레이션]
        """
        # 🚨 [수정 완료] 하드코딩된 [:2] 슬라이싱 방지, name_clean을 기반으로 안전하게 십신명 치환
        name_clean = geokguk_data.get("name_clean", geokguk_data.get("name", ""))
        core_tg = name_clean.replace("격", "").replace("월건록", "비견").replace("양인", "겁재").replace("월걸록", "겁재")
        
        # 만약 치환 후에도 십신 10개 중에 없다면 기본값 식신으로 보호
        if core_tg not in self.career_map:
            core_tg = "식신"
            
        career_info = self.career_map[core_tg]
        
        # 용신(수호신)에 따른 근무 환경 조언
        ys_str = yongshin_data.get("yongshin", "")
        work_env = "나만의 페이스를 유지할 수 있는 환경이 중요합니다."
        if "식상" in ys_str or "재성" in ys_str:
            work_env = "가만히 앉아있는 업무보다는 성과에 따른 확실한 보상이 주어지고, 이동이나 활동성이 보장되는 환경에서 폭발적인 능력을 발휘합니다."
        elif "관성" in ys_str:
            work_env = "체계가 없고 불안정한 스타트업보다는, 간판이 확실하고 규율이 잡혀있는 큰 조직이나 공공기관에 소속될 때 심리적 안정과 승진이 빠릅니다."
        elif "인성" in ys_str or "비겁" in ys_str:
            work_env = "결과만을 재촉당하는 영업직보다는, 나의 지식(자격증)을 바탕으로 결재권을 행사하거나 나만의 독립된 권한이 주어지는 환경이 유리합니다."

        return {
            "core_trait": career_info["style"],
            "recommended_jobs": career_info["jobs"],
            "work_environment": work_env
        }