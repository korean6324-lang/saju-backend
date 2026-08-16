# ==========================================
# 0. 60갑자 납음오행 (納音五行) DB
# ==========================================
NAPEUM_DB = {
    "甲子": "해중금(金)", "乙丑": "해중금(金)", "丙寅": "노중화(火)", "丁卯": "노중화(火)",
    "戊辰": "대림토(土)", "己巳": "대림토(土)", "庚午": "노방토(土)", "辛未": "노방토(土)",
    "壬申": "검봉금(金)", "癸酉": "검봉금(金)", "甲戌": "산두화(火)", "乙亥": "산두화(火)",
    "丙子": "간하수(水)", "丁丑": "간하수(水)", "戊寅": "성두토(土)", "己卯": "성두토(土)",
    "庚辰": "백납금(金)", "辛巳": "백납금(金)", "壬午": "양류목(木)", "癸未": "양류목(木)",
    "甲申": "천중수(水)", "乙酉": "천중수(水)", "丙戌": "옥상토(土)", "丁亥": "옥상토(土)",
    "戊子": "벽력화(火)", "己丑": "벽력화(火)", "庚寅": "송백목(木)", "辛卯": "송백목(木)",
    "壬辰": "장류수(水)", "癸巳": "장류수(水)", "甲午": "사중금(金)", "乙未": "사중금(金)",
    "丙申": "산하화(火)", "丁酉": "산하화(火)", "戊戌": "평지목(木)", "己亥": "평지목(木)",
    "庚子": "벽상토(土)", "辛丑": "벽상토(土)", "壬寅": "금박금(金)", "癸卯": "금박금(金)",
    "甲辰": "복등화(火)", "乙巳": "복등화(火)", "丙午": "천하수(水)", "丁未": "천하수(水)",
    "戊申": "대역토(土)", "己酉": "대역토(土)", "庚戌": "차천금(金)", "辛亥": "차천금(金)",
    "壬子": "상자목(木)", "癸丑": "상자목(木)", "甲寅": "대계수(水)", "乙卯": "대계수(水)",
    "丙辰": "사중토(土)", "丁巳": "사중토(土)", "戊午": "천상화(火)", "己未": "천상화(火)",
    "庚申": "석류목(木)", "辛酉": "석류목(木)", "壬戌": "대해수(水)", "癸亥": "대해수(水)"
}

# ==========================================
# 1. 한문-한글 융합 메타데이터 (Hanja-Tooltip DB)
# ==========================================
HANJA_DB = {
    # [천간 10글자]
    "甲": {"term": "갑", "hanja": "甲", "meaning": "양목(陽木), 큰 나무, 곧게 뻗어나가는 기질"},
    "乙": {"term": "을", "hanja": "乙", "meaning": "음목(陰木), 화초/넝쿨, 유연함과 생존력"},
    "丙": {"term": "병", "hanja": "丙", "meaning": "양화(陽火), 태양, 만물을 비추는 발산지기"},
    "丁": {"term": "정", "hanja": "丁", "meaning": "음화(陰火), 등촉/모닥불, 집중된 열기와 인공의 불"},
    "戊": {"term": "무", "hanja": "戊", "meaning": "양토(陽土), 큰 산/광야, 포용력과 중재자"},
    "己": {"term": "기", "hanja": "己", "meaning": "음토(陰土), 전답/정원, 만물을 길러내는 실속형 토양"},
    "庚": {"term": "경", "hanja": "庚", "meaning": "양금(陽金), 제련되지 않은 무쇠/바위, 결단력과 숙살지기"},
    "辛": {"term": "신", "hanja": "辛", "meaning": "음금(陰金), 보석/칼날, 예리함과 완성된 가치"},
    "壬": {"term": "임", "hanja": "壬", "meaning": "양수(陽水), 바다/큰 강, 깊은 지혜와 포용력"},
    "癸": {"term": "계", "hanja": "癸", "meaning": "음수(陰水), 이슬/시냇물, 섬세함과 생명수"},
    
    # [지지 12글자 완벽 추가]
    "子": {"term": "자", "hanja": "子", "meaning": "양수(陽水), 쥐, 지혜와 생명력의 잉태, 한겨울"},
    "丑": {"term": "축", "hanja": "丑", "meaning": "음토(陰土), 소, 인내와 끈기, 얼어붙은 땅"},
    "寅": {"term": "인", "hanja": "寅", "meaning": "양목(陽木), 호랑이, 권력과 시작의 에너지, 초봄"},
    "卯": {"term": "묘", "hanja": "卯", "meaning": "음목(陰木), 토끼, 도화살과 봄의 생기, 만물 생장"},
    "辰": {"term": "진", "hanja": "辰", "meaning": "양토(陽土), 용, 이상주의와 변화무쌍, 수(水)의 고지"},
    "巳": {"term": "사", "hanja": "巳", "meaning": "음화(陰火), 뱀, 지적 호기심과 활동력, 초여름"},
    "午": {"term": "오", "hanja": "午", "meaning": "양화(陽火), 말, 열정과 도화살, 한여름의 불꽃"},
    "未": {"term": "미", "hanja": "未", "meaning": "음토(陰土), 양, 희생과 수용, 목(木)의 고지"},
    "申": {"term": "신", "hanja": "申", "meaning": "양금(陽金), 원숭이, 다재다능과 역마살, 초가을"},
    "酉": {"term": "유", "hanja": "酉", "meaning": "음금(陰金), 닭, 결단력과 도화살, 완성된 열매"},
    "戌": {"term": "술", "hanja": "戌", "meaning": "양토(陽土), 개, 충직함과 천라지망, 화(火)의 고지"},
    "亥": {"term": "해", "hanja": "亥", "meaning": "음수(陰水), 돼지, 포용력과 역마살, 초겨울"},

    # [명리 심화 전문 용어 (툴팁용 안정화 데이터 추가)]
    "통근": {"term": "통근(뿌리내림)", "hanja": "通根", "meaning": "하늘의 기운이 땅에 튼튼하게 뿌리를 내렸다는 뜻. 주변에 흔들리지 않는 자기만의 확고한 기반과 독립성을 의미합니다."},
    "개두": {"term": "개두", "hanja": "蓋頭", "meaning": "천간(하늘)이 지지(땅)를 억누르는 형국. 운이 들어와도 머리가 덮여 있어 실속이 다소 떨어집니다."},
    "절각": {"term": "절각", "hanja": "截脚", "meaning": "지지(땅)가 천간(하늘)을 쳐서 다리가 잘린 형국. 겉보기와 달리 진행이 막히거나 지연될 수 있습니다."},
    "충": {"term": "충", "hanja": "沖", "meaning": "글자끼리 정면으로 부딪히는 기운. 깨짐과 분리를 뜻하지만, 긍정적으로는 '폭발적인 변화와 새로운 시작'을 의미하기도 합니다."},
    "원진": {"term": "원진", "hanja": "怨嗔", "meaning": "서로 미워하고 원망하며 밀어내는 갈등의 살(殺). 인간관계에서 오해와 집착이 생기기 쉽습니다."},
    "귀문": {"term": "귀문", "hanja": "鬼門", "meaning": "귀신이 드나드는 문. 비상한 영감, 천재성, 직관력, 예술성을 의미하며, 부정적으로는 신경쇠약이나 과도한 집착을 뜻합니다."},
    "천라지망": {"term": "천라지망", "hanja": "天羅地網", "meaning": "하늘과 땅에 쳐진 그물. 활동이 묶이는 답답함이 있으나, 사람을 살리고 돕는 직업(의료, 교육, 법률, 상담 등)으로 대성할 수 있는 특별한 기운입니다."},
    "공협": {"term": "공협", "hanja": "拱挾", "meaning": "두 글자 사이에 빠진 글자를 허공에서 자석처럼 끌어와 '보이지 않는 숨겨진 무기'로 사용하는 현상입니다."},
    "도충": {"term": "도충", "hanja": "倒沖", "meaning": "강한 같은 기운이 뭉쳐서 반대편 기운을 폭발적으로 불러오는 현상. 원국에 없는 기운을 기적처럼 쓰게 됩니다."},

    "형": {"term": "형", "hanja": "刑", "meaning": "형벌을 가한다는 뜻으로, 조정, 타협, 수술수나 관재구설을 의미합니다."},
    "자형": {"term": "자형", "hanja": "自刑", "meaning": "스스로 형벌을 가한다는 뜻으로, 자기비하, 내적 갈등을 의미합니다."},
    "파": {"term": "파", "hanja": "破", "meaning": "깨어지고 파괴된다는 뜻으로, 약속 파기나 분열을 의미합니다."},
    "해": {"term": "해", "hanja": "害", "meaning": "서로 방해하고 해친다는 뜻으로, 이간질이나 불화를 의미합니다."},
    "육합": {"term": "육합", "hanja": "六合", "meaning": "음양의 합으로 비밀스러운 결속, 친밀한 관계를 의미합니다."},

    # [12운성]
    "장생": {"term": "장생", "hanja": "長生", "meaning": "만물이 생겨나는 시기. 후원과 발전, 순수한 시작과 생명력을 의미합니다."},
    "목욕": {"term": "목욕", "hanja": "沐浴", "meaning": "태어나서 씻는 시기. 도화살의 기운, 멋내기, 호기심과 시행착오를 의미합니다."},
    "관대": {"term": "관대", "hanja": "冠帶", "meaning": "띠를 두르는 시기(청년). 투지와 고집, 자수성가, 뻗어나가는 강한 힘을 의미합니다."},
    "건록": {"term": "건록", "hanja": "建祿", "meaning": "벼슬길에 오르는 시기. 독립, 건실함, 완벽주의, 자수성가와 안정을 의미합니다."},
    "제왕": {"term": "제왕", "hanja": "帝旺", "meaning": "인생의 최정점. 강력한 카리스마, 리더십, 극성스러움과 독립심을 의미합니다."},
    "쇠": {"term": "쇠", "hanja": "衰", "meaning": "기운이 쇠퇴하기 시작함. 노련함, 타협, 관조적인 자세와 수용력을 의미합니다."},
    "병": {"term": "병", "hanja": "病", "meaning": "병이 드는 시기. 동정심, 감수성, 예민함, 직관력과 예술성을 의미합니다."},
    "사": {"term": "사", "hanja": "死", "meaning": "죽음에 이르는 시기. 정신적인 세계, 철학/종교적 관심, 육체적 정지와 내면적 깊이를 의미합니다."},
    "묘": {"term": "묘", "hanja": "墓", "meaning": "무덤(창고)에 들어가는 시기. 저장, 구두쇠 기질, 내면의 비밀, 치밀한 안정 추구를 의미합니다."},
    "절": {"term": "절", "hanja": "絶", "meaning": "끊어지고 완전히 소멸함. 극적인 변화, 단절 후의 새로운 전환과 결단력을 의미합니다."},
    "태": {"term": "태", "hanja": "胎", "meaning": "다시 잉태되는 시기. 새로운 가능성, 의존성, 조심스러움과 기획력을 의미합니다."},
    "양": {"term": "양", "hanja": "養", "meaning": "뱃속에서 길러지는 시기. 평화, 육성, 준비, 양육과 보호받는 기운을 의미합니다."},

    # [십신 및 공망 툴팁 데이터]
    "일간": {"term": "일간(나)", "hanja": "日干", "meaning": "사주의 기준이 되는 '나 자신'입니다."},
    "비견": {"term": "비견", "hanja": "比肩", "meaning": "나와 오행/음양이 같은 기운. 독립심, 주체성, 형제자매, 경쟁자를 상징합니다."},
    "겁재": {"term": "겁재", "hanja": "劫財", "meaning": "나와 오행은 같으나 음양이 다른 기운. 강한 투쟁심, 재물 탈취, 라이벌을 상징합니다."},
    "식신": {"term": "식신", "hanja": "食神", "meaning": "내가 생(生)하며 음양이 같은 기운. 의식주, 창의력, 수명, 전문적 재능을 상징합니다."},
    "상관": {"term": "상관", "hanja": "傷官", "meaning": "내가 생(生)하며 음양이 다른 기운. 혁신, 달변, 관습 타파, 날카로운 재능을 상징합니다."},
    "편재": {"term": "편재", "hanja": "偏財", "meaning": "내가 극(剋)하며 음양이 같은 기운. 큰 재물, 투기성, 공간 지각력, 사업 수완을 상징합니다."},
    "정재": {"term": "정재", "hanja": "正財", "meaning": "내가 극(剋)하며 음양이 다른 기운. 안정적인 재물, 월급, 꼼꼼함, 성실함을 상징합니다."},
    "편관": {"term": "편관", "hanja": "偏官", "meaning": "나를 극(剋)하며 음양이 같은 기운. 강한 권력, 카리스마, 스트레스, 명예욕을 상징합니다."},
    "정관": {"term": "정관", "hanja": "正官", "meaning": "나를 극(剋)하며 음양이 다른 기운. 합리적 규율, 직장, 책임감, 안정된 명예를 상징합니다."},
    "편인": {"term": "편인", "hanja": "偏印", "meaning": "나를 생(生)하며 음양이 같은 기운. 직관, 영감, 전문 자격, 눈치, 외골수 기질을 상징합니다."},
    "정인": {"term": "정인", "hanja": "正印", "meaning": "나를 생(生)하며 음양이 다른 기운. 학문, 모성애, 도덕성, 문서와 결재 운을 상징합니다."},
    "공망": {"term": "공망", "hanja": "空亡", "meaning": "밑빠진 독처럼 채워지지 않는 기운. 해당 글자의 덕이 비어버려 갈구하게 되거나, 정신적인 가치로 승화시켜야 함을 뜻합니다."},

    # [추가 보강: 전문가 심층 신살 및 대운/세운 툴팁]
    "천을귀인": {"term": "천을귀인", "hanja": "天乙貴人", "meaning": "모든 흉액을 길함으로 바꾸는 최고 존엄의 길성. 위기에서 돕는 귀인을 만납니다."},
    "문창귀인": {"term": "문창귀인", "hanja": "文昌貴人", "meaning": "총명하고 학문적 성취가 뛰어남을 의미하는 길성. 글재주와 창의력이 뛰어납니다."},
    "도화살": {"term": "도화살", "hanja": "桃花殺", "meaning": "사람을 끌어당기는 강한 매력과 인기. 현대에는 연예인, 방송, 마케팅 분야의 강력한 무기입니다."},
    "역마살": {"term": "역마살", "hanja": "驛馬殺", "meaning": "이동과 활동성이 강한 기운. 해외 진출, 무역, 유통, 출장 등 동적인 환경에서 발복합니다."},
    "화개살": {"term": "화개살", "hanja": "華蓋殺", "meaning": "화려함을 덮는다는 뜻. 예술, 학문, 철학, 종교에 깊은 재능과 정신적 성숙함을 상징합니다."},
    "백호대살": {"term": "백호대살", "hanja": "白虎大殺", "meaning": "폭발적인 프로페셔널 에너지와 압도적 카리스마로 쓰이며, 전문직이나 특수 분야에서 대성합니다."},
    "괴강살": {"term": "괴강살", "hanja": "魁罡殺", "meaning": "우두머리의 별. 굽히기 싫어하는 강한 주체성과 극단적 결단력을 상징하며 리더에 어울립니다."},
    "양인살": {"term": "양인살", "hanja": "羊刃殺", "meaning": "칼을 쥔 강건한 기운. 권력과 끈기, 타협 없는 불굴의 의지를 의미하며, 전문직(의료/법조)에서 대성합니다."},
    "대운": {"term": "대운", "hanja": "大運", "meaning": "10년마다 바뀌는 인생의 큰 환경과 도로망. 대운이 좋으면 흉액이 반감됩니다."},
    "세운": {"term": "세운", "hanja": "歲運", "meaning": "매년 들어오는 1년짜리 기운. 그 해에 일어날 구체적인 사건과 체감을 의미합니다."},
    "순행": {"term": "순행", "hanja": "順行", "meaning": "시간의 흐름대로 기운이 순조롭게 흘러가는 방향입니다."},
    "역행": {"term": "역행", "hanja": "逆行", "meaning": "시간의 흐름과 반대로 기운이 거슬러 올라가는 방향입니다."}
}

# ==========================================
# 2. 지장간 (Hidden Stems in Earthly Branches)
# ==========================================
HIDDEN_STEMS = {
    "子": {"initial": ("壬", 10), "middle": (None, 0), "main": ("癸", 20)},
    "丑": {"initial": ("癸", 9),  "middle": ("辛", 3), "main": ("己", 18)},
    "寅": {"initial": ("戊", 7),  "middle": ("丙", 7), "main": ("甲", 16)},
    "卯": {"initial": ("甲", 10), "middle": (None, 0), "main": ("乙", 20)},
    "辰": {"initial": ("乙", 9),  "middle": ("癸", 3), "main": ("戊", 18)},
    "巳": {"initial": ("戊", 7),  "middle": ("庚", 7), "main": ("丙", 16)},
    "午": {"initial": ("丙", 10), "middle": ("己", 9), "main": ("丁", 11)},
    "未": {"initial": ("丁", 9),  "middle": ("乙", 3), "main": ("己", 18)},
    "申": {"initial": ("戊", 7),  "middle": ("壬", 7), "main": ("庚", 16)},
    "酉": {"initial": ("庚", 10), "middle": (None, 0), "main": ("辛", 20)},
    "戌": {"initial": ("辛", 9),  "middle": ("丁", 3), "main": ("戊", 18)},
    "亥": {"initial": ("戊", 7),  "middle": ("甲", 7), "main": ("壬", 16)}
}

# 오행 맵핑 (통근 분석용)
ELEMENT_MAP = {
    "甲": "목", "乙": "목", "寅": "목", "卯": "목",
    "丙": "화", "丁": "화", "巳": "화", "午": "화",
    "戊": "토", "己": "토", "辰": "토", "戌": "토", "丑": "토", "未": "토",
    "庚": "금", "辛": "금", "申": "금", "酉": "금",
    "壬": "수", "癸": "수", "亥": "수", "子": "수"
}

# 십신/공망 산출용 코어 데이터
YIN_YANG = {
    "甲": "+", "丙": "+", "戊": "+", "庚": "+", "壬": "+",
    "乙": "-", "丁": "-", "己": "-", "辛": "-", "癸": "-",
    "寅": "+", "辰": "+", "巳": "+", "申": "+", "戌": "+", "亥": "+",
    "卯": "-", "丑": "-", "午": "-", "未": "-", "酉": "-", "子": "-"
}

TEN_GODS_MAP = {
    0: {"same": "비견", "diff": "겁재"},
    1: {"same": "식신", "diff": "상관"},
    2: {"same": "편재", "diff": "정재"},
    3: {"same": "편관", "diff": "정관"},
    4: {"same": "편인", "diff": "정인"}
}

STEMS_SEQ = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 12운성 순행(양간)/역행(음간) 인덱스 오프셋 맵핑
WUNSEONG_STAGES = ["장생", "목욕", "관대", "건록", "제왕", "쇠", "병", "사", "묘", "절", "태", "양"]
WUNSEONG_BASE = {
    "甲": {"亥": 0}, "丙": {"寅": 0}, "戊": {"寅": 0}, "庚": {"巳": 0}, "壬": {"申": 0}, # 양간 (순행)
    "乙": {"午": 0}, "丁": {"酉": 0}, "己": {"酉": 0}, "辛": {"子": 0}, "癸": {"卯": 0}  # 음간 (역행)
}
EARTHLY_BRANCHES_SEQ = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]


class MechanicsEngine:
    def __init__(self):
        pass

    # [핵심 추가] 천문 절기 무시하고 둔월법(遁月法)으로 고법 월주 도출
    def get_traditional_month_pillar(self, year_stem: str, lunar_month: int) -> tuple:
        """고법 명리의 둔월법을 이용해 음력 달 기준의 강제 월간/월지를 반환합니다."""
        if year_stem not in STEMS_SEQ or not (1 <= lunar_month <= 12):
            return None, None
        
        # 1. 월지 (음력 1월 = 寅, 11월 = 子)
        m_branch = EARTHLY_BRANCHES_SEQ[(lunar_month + 1) % 12]
        
        # 2. 월간 (둔월법 공식: 연간 인덱스 % 5 * 2 + 2)
        y_stem_idx = STEMS_SEQ.index(year_stem)
        start_stem_idx = ((y_stem_idx % 5) * 2 + 2) % 10
        m_stem_idx = (start_stem_idx + lunar_month - 1) % 10
        m_stem = STEMS_SEQ[m_stem_idx]
        
        return m_stem, m_branch

    # [핵심 추가] 납음오행 반환
    def get_napeum(self, stem: str, branch: str) -> str:
        """60갑자에 해당하는 납음오행(소리 오행)을 반환합니다."""
        ganzi = stem + branch
        return NAPEUM_DB.get(ganzi, "알수없음")

    def get_metadata(self, term: str) -> dict:
        """한자/의미 메타데이터 반환"""
        return HANJA_DB.get(term, {"term": term, "hanja": term, "meaning": "데이터 준비 중"})

    def get_hidden_stems(self, branch: str) -> dict:
        """지장간 객체 반환"""
        return HIDDEN_STEMS.get(branch, {})

    def get_12wunseong(self, stem: str, branch: str) -> str:
        """천간과 지지의 관계를 통한 12운성 도출"""
        if stem not in WUNSEONG_BASE or branch not in EARTHLY_BRANCHES_SEQ:
            return "알 수 없음"
            
        base_branch = list(WUNSEONG_BASE[stem].keys())[0]
        base_idx = EARTHLY_BRANCHES_SEQ.index(base_branch)
        target_idx = EARTHLY_BRANCHES_SEQ.index(branch)
        
        # 양간은 순행(+), 음간은 역행(-)
        is_yang = stem in ["甲", "丙", "戊", "庚", "壬"]
        if is_yang:
            diff = (target_idx - base_idx) % 12
        else:
            diff = (base_idx - target_idx) % 12
            
        return WUNSEONG_STAGES[diff]

    def check_tonggeun(self, target_stem: str, branches_dict: dict) -> dict:
        """통근(通根) 스캐너"""
        result = {
            "target": target_stem,
            "is_rooted": False,
            "total_power": 0,
            "roots": []
        }
        
        # 🚨 [보완 적용] 프론트엔드 비정상 입력(None, List 등) 차단
        if not isinstance(branches_dict, dict) or not target_stem:
            return result

        target_element = ELEMENT_MAP.get(target_stem)
        if not target_element:
            return result

        for pillar_name, branch in branches_dict.items():
            hidden = self.get_hidden_stems(branch)
            
            for root_type in ["initial", "middle", "main"]:
                h_stem, power = hidden.get(root_type, (None, 0))
                
                if h_stem and ELEMENT_MAP.get(h_stem) == target_element:
                    weight = 1.2 if h_stem == target_stem else 1.0
                    # 🚨 [보완 적용] 부동소수점 오차 방지를 위한 반올림 처리
                    calculated_power = round(power * weight)
                    
                    result["is_rooted"] = True
                    result["total_power"] += calculated_power
                    result["roots"].append({
                        "pillar": pillar_name,
                        "branch": branch,
                        "type": "여기" if root_type == "initial" else "중기" if root_type == "middle" else "정기",
                        "hidden_stem": h_stem,
                        "power": calculated_power
                    })
                    
        return result

    def get_five_elements_distribution(self, stems_list: list, branches_list: list) -> dict:
        """사주 8글자의 오행 개수를 스캔하여 반환합니다."""
        # 🚨 [보완 적용] None 타입이 들어올 경우 빈 리스트로 초기화하여 런타임 에러 방지
        stems_list = stems_list or []
        branches_list = branches_list or []
        
        distribution = {"목": 0, "화": 0, "토": 0, "금": 0, "수": 0}
        
        for char in stems_list + branches_list:
            element = ELEMENT_MAP.get(char)
            if element in distribution:
                distribution[element] += 1
                
        return distribution

    def get_ten_god(self, day_stem: str, target_char: str) -> str:
        """일간을 기준으로 특정 글자의 십신(육친)을 연산합니다."""
        if day_stem == target_char:
            return "일간"
            
        elements_idx = {"목": 0, "화": 1, "토": 2, "금": 3, "수": 4}
        day_el = ELEMENT_MAP.get(day_stem)
        target_el = ELEMENT_MAP.get(target_char)
        
        # 🚨 [보완 적용] 매칭 실패 시 빈 문자열 대신 일관된 "알 수 없음" 반환
        if not day_el or not target_el: 
            return "알 수 없음"
        
        day_yy = YIN_YANG.get(day_stem)
        target_yy = YIN_YANG.get(target_char)
        
        diff = (elements_idx[target_el] - elements_idx[day_el]) % 5
        yy_match = "same" if day_yy == target_yy else "diff"
        
        return TEN_GODS_MAP[diff][yy_match]

    def get_gongmang(self, day_stem: str, day_branch: str) -> list:
        """일주(일간과 일지)를 기준으로 공망(空亡) 지지 2개를 도출합니다."""
        if day_stem not in STEMS_SEQ or day_branch not in EARTHLY_BRANCHES_SEQ:
            return []
            
        s_idx = STEMS_SEQ.index(day_stem)
        b_idx = EARTHLY_BRANCHES_SEQ.index(day_branch)
        
        group_idx = (b_idx - s_idx) % 12
        gm1_idx = (group_idx - 2) % 12
        gm2_idx = (group_idx - 1) % 12
        
        return [EARTHLY_BRANCHES_SEQ[gm1_idx], EARTHLY_BRANCHES_SEQ[gm2_idx]]

    # ==========================================
    # [Phase 9 추가] 대운(10년 주기) & 세운(1년 주기) 연산 알고리즘
    # ==========================================
    def get_daewun_sequence(self, gender: str, year_stem: str, month_stem: str, month_branch: str, daewun_num: int = 1, count: int = 8) -> dict:
        """
        양남음녀(陽男陰女) 순행, 음남양녀(陰男陽女) 역행 법칙에 따라 대운의 흐름과 기둥을 도출합니다.
        """
        if year_stem not in YIN_YANG or month_stem not in STEMS_SEQ or month_branch not in EARTHLY_BRANCHES_SEQ:
            return {"direction": "알 수 없음", "timeline": []}

        # 🚨 [보완 적용] 성별 입력값 정규화 (대소문자/공백 무시) 및 Fallback 처리
        safe_gender = str(gender).strip().upper()
        if safe_gender not in ['M', 'F']:
            safe_gender = 'M'  # 예외 상황 시 기본값 지정
            
        # 🚨 [보완 적용] 대운수(daewun_num)를 명리학의 한계치인 1~10 사이로 강제
        safe_daewun_num = max(1, min(10, int(daewun_num)))

        is_yang_year = YIN_YANG[year_stem] == "+"
        is_forward = (safe_gender == 'M' and is_yang_year) or (safe_gender == 'F' and not is_yang_year)
        direction_str = "순행" if is_forward else "역행"
        
        s_idx = STEMS_SEQ.index(month_stem)
        b_idx = EARTHLY_BRANCHES_SEQ.index(month_branch)
        
        timeline = []
        for i in range(1, count + 1):
            if is_forward:
                curr_s = STEMS_SEQ[(s_idx + i) % 10]
                curr_b = EARTHLY_BRANCHES_SEQ[(b_idx + i) % 12]
            else:
                curr_s = STEMS_SEQ[(s_idx - i) % 10]
                curr_b = EARTHLY_BRANCHES_SEQ[(b_idx - i) % 12]
            
            age = safe_daewun_num + (i - 1) * 10
            timeline.append({"age": age, "stem": curr_s, "branch": curr_b})
            
        return {"direction": direction_str, "timeline": timeline}

    def get_sewun_sequence(self, start_year: int, count: int = 10) -> list:
        """
        갑자년(1984년 등 연도가 4로 끝나는 해)을 기준으로 현재 시점부터의 1년짜리 세운(歲運) 60갑자 도출
        """
        sewun_list = []
        for y in range(start_year, start_year + count):
            stem_idx = (y - 4) % 10
            branch_idx = (y - 4) % 12
            sewun_list.append({
                "year": y,
                "stem": STEMS_SEQ[stem_idx],
                "branch": EARTHLY_BRANCHES_SEQ[branch_idx]
            })
        return sewun_list