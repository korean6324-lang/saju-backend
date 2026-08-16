# logic_practical.py

class PracticalEngine:
    def __init__(self):
        # ==========================================
        # 1. 🚨 [DB 확장] 오행별 건강/질병 및 부부 건강/식이요법 매핑 DB
        # ==========================================
        self.health_map = {
            "목": {
                "organ": "간, 담낭, 신경계", 
                "weak": "만성 피로, 신경쇠약, 우울증, 시력 저하", 
                "excess": "간 수치 상승, 근육 뭉침, 분노 조절 어려움",
                "diet": "신맛 나는 음식(모과, 유자, 녹색 채소)이 약이 되며, 과음을 피해야 합니다.",
                "marriage_focus": "목(木) 기운이 불안정하면 신경질과 짜증이 잦아져 부부싸움의 원인이 됩니다. 부부가 함께 등산이나 산책을 하며 스트레스를 푸는 것이 좋습니다."
            },
            "화": {
                "organ": "심장, 소장, 혈관", 
                "weak": "수족냉증, 저혈압, 무기력, 심장 두근거림", 
                "excess": "고혈압, 심혈관 질환, 다혈질, 불면증",
                "diet": "쓴맛 나는 음식(수수, 홍삼, 붉은색 과일)이 좋으며, 카페인과 맵고 짠 음식을 줄여야 합니다.",
                "marriage_focus": "화(火) 기운이 넘치면 감정의 기복이 심해 부부간에 돌이킬 수 없는 폭언을 할 수 있습니다. 대화 시 한 템포 쉬어가는 여유가 필수입니다."
            },
            "토": {
                "organ": "위장, 비장, 소화기", 
                "weak": "소화불량, 위염, 식욕 부진, 피부 트러블", 
                "excess": "비만, 당뇨, 위궤양, 세포/종양 질환",
                "diet": "단맛 나는 음식(단호박, 꿀, 노란색 채소)이 위장을 편하게 하며, 밀가루와 야식을 피해야 합니다.",
                "marriage_focus": "토(土)는 생각과 번뇌를 뜻합니다. 기운이 막히면 부부 사이에 속마음을 털어놓지 않고 꽁하게 담아두어 속병이 생기니 대화를 자주 해야 합니다."
            },
            "금": {
                "organ": "폐, 대장, 호흡기", 
                "weak": "천식, 비염, 잦은 감기, 장 트러블", 
                "excess": "호흡기 건조, 변비, 관절/뼈 질환",
                "diet": "매운맛 나는 음식(생강, 마늘, 백색 채소)이 기관지를 보호하며, 건조한 환경을 피해야 합니다.",
                "marriage_focus": "금(金) 기운이 예민해지면 맺고 끊음이 차가워져 배우자에게 냉랭한 상처를 줍니다. 집안의 습도를 잘 맞추고 따뜻한 스킨십을 늘리십시오."
            },
            "수": {
                "organ": "신장, 방광, 생식기", 
                "weak": "신장 기능 저하, 생식기 질환, 부종, 호르몬 불균형", 
                "excess": "신장 결석, 냉증, 우울감, 산부인과/전립선 질환",
                "diet": "짠맛 나는 해조류(미역, 다시마, 검은콩)가 신장을 보양하며, 몸을 항상 따뜻하게 유지해야 합니다.",
                "marriage_focus": "수(水)는 생식과 잉태를 주관합니다. 이 기운이 고립되거나 과다하면 난임, 생리불순, 혹은 부부관계(속궁합)의 만족도 저하로 이어질 수 있으니 부인과/비뇨기과 관리가 매우 중요합니다."
            }
        }

        # ==========================================
        # 2. 🚨 [DB 확장] 십신(격국) 기반 직업, 재테크 및 부부 역할 매핑 DB
        # ==========================================
        self.career_map = {
            "비견": {
                "style": "독립형 전문가", "jobs": "프리랜서, 1인 기업가, 운동선수, 지점장, 독자적 기술직",
                "wealth": "동업은 금물이며, 오직 내 땀방울과 기술로 번 돈만이 내 몫이 되는 자수성가형 재테크.",
                "marriage_role": "가정 내에서 통제받기를 싫어하며, 부부가 상하 관계가 아닌 철저히 동등한 '친구 같은 맞벌이 동반자' 역할을 선호합니다."
            },
            "겁재": {
                "style": "승부사 및 투자가", "jobs": "M&A 전문가, 펀드매니저, 프로게이머, 경쟁이 치열한 영업직",
                "wealth": "하이리스크 하이리턴. 공격적인 투자나 주식, 경매 등에 관심이 많아 재물의 기복이 큰 편입니다.",
                "marriage_role": "경제권 다툼(군비쟁재)이 일어날 수 있으니, 부부의 재산을 철저히 분리하거나 자산 관리를 배우자에게 전적으로 맡기는 것이 안전합니다."
            },
            "식신": {
                "style": "장인 및 연구가", "jobs": "연구원, 셰프, 개발자(IT), 작가, 제조업, 엔지니어",
                "wealth": "한 분야를 꾸준히 파고들어 얻는 정당하고 지속적인 수입으로, 마르지 않는 화수분 같은 재물운입니다.",
                "marriage_role": "배우자와 자식에게 다정다감하게 베풀고 요리를 해주는 등 매우 가정적이고 따뜻한 양육자 역할을 훌륭히 해냅니다."
            },
            "상관": {
                "style": "크리에이터 및 언변가", "jobs": "마케터, 유튜버/방송인, 강사, 로이어(변호사), 디자이너",
                "wealth": "뛰어난 아이디어와 말재주를 무기로, 시류를 빠르게 읽고 단기간에 큰 수익을 창출해 내는 능력자입니다.",
                "marriage_role": "잔소리가 다소 있으나 융통성이 좋고 센스가 넘쳐 가정의 문제를 빠르고 스마트하게 해결하는 만능 해결사입니다."
            },
            "편재": {
                "style": "사업가 및 무역가", "jobs": "글로벌 무역, 부동산 개발, 플랫폼 사업가, 유통/물류업",
                "wealth": "돈의 흐름을 꿰뚫어 보며 씀씀이가 크고 통 큰 투자를 즐깁니다. 사업이나 횡재수로 거대한 부를 쥘 수 있습니다.",
                "marriage_role": "가정 안에만 머물기보다는 밖에서 활발히 활동하며 가세를 크게 일으키는 활동적이고 능력 있는 배우자입니다."
            },
            "정재": {
                "style": "금융가 및 관리자", "jobs": "은행원, 회계사, 재무 관리자, 공기업, 안정적인 프랜차이즈",
                "wealth": "티끌 모아 태산. 모험을 피하고 저축과 안정적인 적금, 확실한 자산을 선호하는 꼼꼼한 관리형 재테크입니다.",
                "marriage_role": "낭비 없이 가계를 건실하게 꾸리며, 내 가족을 끝까지 책임지는 가장 모범적이고 든든한 배우자입니다."
            },
            "편관": {
                "style": "특수직 및 카리스마 리더", "jobs": "군인, 경찰, 검찰, 외과의사, 스타트업 CEO, 리스크 관리자",
                "wealth": "돈보다는 조직의 명예와 가오(권력)를 중시하며, 큰 위기를 돌파한 후 보상으로 막대한 부가 따라오는 스타일입니다.",
                "marriage_role": "가정을 강한 카리스마로 이끌며, 배우자가 힘들 때 거센 비바람을 맨몸으로 막아주는 무뚝뚝하지만 든든한 수호자입니다."
            },
            "정관": {
                "style": "행정가 및 조직인", "jobs": "고위 공무원, 대기업 임원, 행정직, 규정/감사 부서",
                "wealth": "안정적인 직장의 월급과 정년 보장을 통한 노후 연금 등 가장 합리적이고 변수 없는 안전 지향형 자산 축적입니다.",
                "marriage_role": "책임감이 강하고 가정의 규범과 도리를 철저히 지키며, 사회적으로 인정받는 반듯하고 다정한 남편/아내입니다."
            },
            "편인": {
                "style": "전략가 및 기획자", "jobs": "기획자, 프로듀서, 종교/철학가, 정신과 의사, 예술 감독",
                "wealth": "남들이 보지 못하는 정보나 특수한 라이선스(자격증, 지적재산권)를 활용하여 지대(Rent) 수익을 창출해 냅니다.",
                "marriage_role": "눈치가 빠르고 직관력이 뛰어나 배우자의 속마음을 잘 읽어내나, 가끔은 혼자만의 고독한 취미나 공간이 반드시 필요합니다."
            },
            "정인": {
                "style": "교육가 및 학자", "jobs": "교수, 교사, 문서/부동산 임대업, 학원 사업, 출판업",
                "wealth": "부동산 문서, 결재권, 혹은 상속받은 자산 등 땅이나 건물에 돈을 묻어두고 안정적인 임대 수익을 내는 것이 최상입니다.",
                "marriage_role": "마치 어머니의 품처럼 넉넉하게 배우자를 감싸주고 이해하며, 자녀 교육에 매우 훌륭한 환경을 조성하는 지혜로운 동반자입니다."
            }
        }

    def analyze_health(self, elements_dist: dict) -> list:
        """
        [헬스케어 질병 및 부부 건강 스캐너]
        오행의 분포(개수)를 분석하여 과다/고립된 오행을 찾아 취약 장기와 개운법을 진단합니다.
        """
        health_warnings = []
        
        # 🚨 [보안 추가] 타입 검증 및 초기화. 프론트 오류 시 서버 다운 방지
        if not isinstance(elements_dist, dict):
            elements_dist = {}
            
        for element, count in elements_dist.items():
            # 🚨 [보안 추가] 유효하지 않은 키값(KeyError) 방어
            if element not in self.health_map:
                continue
                
            data = self.health_map[element]
            
            if count >= 3:
                health_warnings.append({
                    "element": element,
                    "status_code": "과다", # 🚨 프론트엔드가 텍스트 대신 이 코드로 조건 판별
                    "status": "과다 (기운이 너무 강해 병이 됨)",
                    "organ": data["organ"],
                    "symptom": data["excess"],
                    "diet_advice": data["diet"],
                    "marriage_focus": data["marriage_focus"],
                    "advice": f"[{element}]의 기운이 사주에 너무 쏠려 있어 {data['organ']} 쪽에 열성(熱性) 질환이나 과부하가 올 수 있습니다. 꾸준한 검진이 필요합니다."
                })
            elif count == 0:
                health_warnings.append({
                    "element": element,
                    "status_code": "고립(無)", # 🚨 프론트엔드가 텍스트 대신 이 코드로 조건 판별
                    "status": "고립/태약 (기운이 없어 병이 됨)",
                    "organ": data["organ"],
                    "symptom": data["weak"],
                    "diet_advice": data["diet"],
                    "marriage_focus": data["marriage_focus"],
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
                "diet_advice": "편식 없이 골고루 섭취하는 것이 최고의 보약입니다.",
                "marriage_focus": "부부간 기운의 충돌이 적고 건강한 가정을 꾸릴 수 있는 훌륭한 밸런스입니다.",
                "advice": "오행의 개수가 비교적 골고루 분포되어 있어 선천적인 장기의 균형이 훌륭합니다. 규칙적인 생활만 유지하시면 큰 병 없이 건강을 누릴 수 있습니다."
            })
            
        return health_warnings

    def analyze_career(self, geokguk_data: dict, yongshin_data: dict) -> dict:
        """
        [현대적 직업/재테크/부부역할 큐레이션]
        """
        # 🚨 [보안 추가] 타입 검증으로 AttributeError 원천 차단
        if not isinstance(geokguk_data, dict): geokguk_data = {}
        if not isinstance(yongshin_data, dict): yongshin_data = {}

        name_clean = geokguk_data.get("name_clean", geokguk_data.get("name", ""))
        core_tg = name_clean.replace("격", "").replace("월건록", "비견").replace("양인", "겁재").replace("월걸록", "겁재")
        
        # 만약 치환 후에도 십신 10개 중에 없다면 기본값 '식신'으로 보호
        if core_tg not in self.career_map:
            core_tg = "식신"
            
        career_info = self.career_map[core_tg]
        
        # 용신(수호신)에 따른 근무 환경 조언
        ys_str = str(yongshin_data.get("yongshin", ""))
        work_env = "나만의 페이스를 유지할 수 있는 독립적 환경이 중요합니다."
        if "식상" in ys_str or "재성" in ys_str:
            work_env = "가만히 앉아있는 업무보다는 성과에 따른 확실한 보상이 주어지고, 이동이나 활동성이 보장되는 환경에서 폭발적인 능력을 발휘합니다."
        elif "관성" in ys_str:
            work_env = "체계가 없고 불안정한 환경보다는, 간판이 확실하고 규율이 잡혀있는 큰 조직이나 공공기관에 소속될 때 심리적 안정과 승진이 빠릅니다."
        elif "인성" in ys_str or "비겁" in ys_str:
            work_env = "결과만을 재촉당하는 영업직보다는, 나의 전문 지식(자격증)을 바탕으로 결재권을 행사하거나 독립된 권한이 주어지는 환경이 유리합니다."

        return {
            "core_trait": career_info["style"],
            "recommended_jobs": career_info["jobs"],
            "wealth_management": career_info["wealth"],        # 🚨 [추가] 재테크 성향
            "marriage_role": career_info["marriage_role"],     # 🚨 [추가] 가정 내 경제적/정신적 역할
            "work_environment": work_env
        }