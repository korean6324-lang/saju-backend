# logic_classical.py

class ClassicalEngine:
    def __init__(self):
        # 12성(당사주) 보조 데이터 (UI 보조 패널용으로 보존)
        self.dang_saju = {
            "子": {"name": "천귀성(天貴星)", "desc": "귀한 기운을 타고났으나 자만하면 꺾인다."},
            "丑": {"name": "천액성(天厄星)", "desc": "초년의 고난과 인내를 거쳐 말년에 우뚝 서는 대기만성."},
            "寅": {"name": "천권성(天權星)", "desc": "남 밑에 있기 싫어하는 권력과 우두머리의 기운."},
            "卯": {"name": "천파성(天破星)", "desc": "인연이나 재물이 흩어지기 쉬우나 기술로 발복한다."},
            "辰": {"name": "천간성(天奸星)", "desc": "변화무쌍하고 지략이 뛰어나 임기응변으로 위기 극복."},
            "巳": {"name": "천문성(天文星)", "desc": "직관과 학문이 뛰어나며 활인업에 인연이 깊다."},
            "午": {"name": "천복성(天福星)", "desc": "의식주가 풍족하고 복록이 따르나 나태해질 수 있다."},
            "未": {"name": "천역성(天驛星)", "desc": "고향을 떠나 분주히 움직이고 땀 흘려야 크게 성공한다."},
            "申": {"name": "천고성(天孤星)", "desc": "일찍 독립하여 홀로 서야 하는 외롭지만 강인한 기운."},
            "酉": {"name": "천인성(天刃星)", "desc": "맺고 끊음이 확실하며, 몸에 흉터나 수술수가 있다."},
            "戌": {"name": "천예성(天藝星)", "desc": "손재주와 고집이 대단하며 자기만의 확고한 세계 구축."},
            "亥": {"name": "천수성(天壽星)", "desc": "느긋하고 수용력이 강하며 말년이 평안하고 장수한다."}
        }

    def get_four_pillars_stars(self, branches_dict: dict) -> dict:
        result = {}
        for pillar, branch in branches_dict.items():
            result[pillar] = self.dang_saju.get(branch, {"name": "알 수 없음", "desc": "-"})
        return result

    def generate_classical_reading(self, formatted_bazi: dict, disasters_data: dict, yongshin_data: dict) -> list:
        """
        [Phase 14] 대가의 간명지 생성 엔진
        태화 이상섭 선생님의 심층 간명 구조를 벤치마킹하여, 고객의 사주에 맞춘 동적 실전 통변을 생성합니다.
        """
        readings = []

        # [에러 픽스] 용신 데이터 안전한 파싱
        yongshin_str = "중화(中和)의 기운"
        if isinstance(yongshin_data, dict):
            y_data = yongshin_data.get("yongshin")
            if isinstance(y_data, dict):
                yongshin_str = y_data.get("yongshin", "조화로운 기운")
            elif isinstance(y_data, str):
                yongshin_str = y_data

        # 1. 사주 원국 (四柱 原局) 분석
        day_stem = formatted_bazi["day"]["stem"]
        month_branch = formatted_bazi["month"]["branch"]
        nature_text = self._get_nature(day_stem, month_branch)
        
        readings.append({
            "section": "1. 사주 원국 (四柱 原局) 분석",
            "items": [
                {"title": "기질 (氣質)", "hanja": "", "text": nature_text},
                {"title": "조후 (調候)", "hanja": "", "text": f"이 명식에 가장 시급하고 귀중한 에너지는 [{yongshin_str}]입니다. 사주의 얼어붙은 흉을 녹이거나 끓는 열기를 식혀주는 절대적인 구원처가 되며, 이 기운이 들어올 때 거대한 숲을 이룹니다."}
            ]
        })

        # 2. 총운 (總運): 인생의 일대기
        y_tg = formatted_bazi["year"]["branch_tg"]
        m_tg = formatted_bazi["month"]["branch_tg"]
        readings.append({
            "section": "2. 총운 (總運) : 뼈를 깎는 시련과 찬란한 발복",
            "items": self._get_chongwun(y_tg, m_tg)
        })

        # 3. 금슬궁 (琴瑟宮): 부부운
        d_tg = formatted_bazi["day"]["branch_tg"]
        readings.append({
            "section": "3. 琴瑟宮 (금슬궁 : 부부운)",
            "items": self._get_couple_wun(d_tg)
        })

        # 4. 자식궁 및 말년 (子宮)
        h_tg = formatted_bazi["hour"]["branch_tg"]
        readings.append({
            "section": "4. 子宮 (자궁 : 자식운 및 말년)",
            "items": self._get_children_wun(h_tg)
        })

        # 5. 봉황 (鳳凰): 영웅의 철학과 그릇
        strength = yongshin_data.get("strength", {}).get("status", "신약")
        readings.append({
            "section": "5. 鳳凰 (봉황 : 인생관과 영웅의 그릇)",
            "items": self._get_phoenix(strength)
        })

        return readings

    def _get_nature(self, d_stem: str, m_branch: str) -> str:
        seasons = {"寅":"초봄", "卯":"완연한 봄", "辰":"늦봄", "巳":"초여름", "午":"한여름", "未":"늦여름", 
                   "申":"초가을", "酉":"완연한 가을", "戌":"늦가을", "亥":"초겨울", "子":"한겨울", "丑":"꽁꽁 언 겨울"}
        elements = {"甲":"우뚝 솟은 거목(巨木)", "乙":"강인한 생명력의 화초(덩굴)", "丙":"세상을 비추는 태양(太陽)", "丁":"어둠을 밝히는 용광로",
                    "戊":"만물을 품는 거대한 산(大山)", "己":"만물을 기르는 비옥한 전답", "庚":"단단하고 예리한 무쇠와 바위", "辛":"정교하게 세공된 보석(명예)",
                    "壬":"속을 알 수 없는 거대한 바다", "癸":"대지를 적시는 생명수(지혜)"}
        
        season = seasons.get(m_branch, "")
        element = elements.get(d_stem, "")
        return f"당신은 {season}에 태어난 {element}의 기상을 품고 있습니다. 모진 비바람이 불어도 내면에는 절대 꺾이지 않는 무서운 자립심과 끈질긴 생존력을 타고난 명식입니다."

    def _get_chongwun(self, y_tg: str, m_tg: str) -> list:
        items = []
        # 년주 (초년)
        if "비견" in y_tg or "겁재" in y_tg:
            items.extend([
                {"title": "", "hanja": "自手成家 (자수성가)", "text": "어린 시절의 외로움을 견디며 오직 자기 손으로 뼈 빠지게 일하여 빈손으로 가문을 일으키는 위대한 개척자의 운명이다."},
                {"title": "", "hanja": "勤力自生 (근력자생)", "text": "단 한 번도 편히 앉아 쉰 적 없이 뼈 빠지게 일하여 스스로 살아남는 억척스러움이 있다."}
            ])
        elif "재" in y_tg:
            items.extend([
                {"title": "", "hanja": "早得財利 (조득재리)", "text": "초년에 재성이 들어있어 남들보다 일찍 현실 감각과 경제관념에 눈을 뜬다. 소년기부터 돈의 흐름을 본능적으로 쫓는다."},
                {"title": "", "hanja": "衣食自足 (의식자족)", "text": "타고난 감각으로 입고 먹는 재물이 풍부하여 스스로 넉넉함을 이룬다."}
            ])
        elif "관" in y_tg:
            items.extend([
                {"title": "", "hanja": "身貴榮門 (신귀영문)", "text": "일찍부터 벼슬길(조직)에 뜻을 품고 반듯한 규율을 익히니 몸이 귀해지고 가문에 영화가 깃든다."},
                {"title": "", "hanja": "平時值杀 (평시치살)", "text": "단, 관살이 무거워지면 어린 시절부터 남모를 억압과 고난을 겪어 남들보다 일찍 철이 든다."}
            ])
        else: # 식상, 인성
            items.extend([
                {"title": "", "hanja": "年上藝星 (년상예성)", "text": "태어난 해에 하늘이 내린 재주(천예성)를 품었으니, 총명함과 남다른 손재주로 일찍이 두각을 나타낸다."},
                {"title": "", "hanja": "祖上恩德 (조상은덕)", "text": "조상의 지극한 은덕을 받아 모진 풍파 속에서도 반드시 구원처가 나타나 위기를 넘긴다."}
            ])

        # 월주 (청년/중년)
        if "식" in m_tg or "상" in m_tg:
            items.extend([
                {"title": "", "hanja": "一生藝術 (일생예술)", "text": "일생토록 예술적이고 뛰어난 기술을 지녀, 쇠를 만져 꽃을 피워내는 듯한 특별한 재주로 세상을 누빈다."}
            ])
        elif "재" in m_tg:
            items.extend([
                {"title": "", "hanja": "行商爲業 (행상위업)", "text": "반듯한 벼슬길이 아니라면 상업과 사업에 투신하게 되며, 수많은 재물을 다루며 거상(巨商)의 길을 걷는다."}
            ])
        elif "관" in m_tg:
            items.extend([
                {"title": "", "hanja": "出入貴家 (출입귀가)", "text": "귀하고 높은 집안과 거대한 조직을 거침없이 출입하며 자연스레 법도를 익히고 큰 명예를 쥔다."}
            ])
        else:
            items.extend([
                {"title": "", "hanja": "東西奔走 (동서분주)", "text": "동서남북 사방으로 바쁘게 뛰어다니며 모진 풍파와 타인의 시기를 이겨내고 마침내 굳건한 입지를 다진다."}
            ])
        return items

    def _get_couple_wun(self, d_tg: str) -> list:
        if "비견" in d_tg or "겁재" in d_tg:
            return [
                {"title": "", "hanja": "雙金相敵 (쌍금상적)", "text": "배우자궁에 나와 똑같은 기운이 앉았으니, 칼과 칼이 부딪히듯 서로 굽히지 않고 자존심 싸움을 벌이기 쉽다."},
                {"title": "", "hanja": "未免叩盆 (미면고분)", "text": "서로를 소유물이 아닌 대등한 동업자나 전우처럼 대우하며 뼈를 깎는 배려를 해야만 흉액을 면하고 백년해로한다."}
            ]
        elif "재" in d_tg:
            return [
                {"title": "", "hanja": "琴瑟和調 (금슬화조)", "text": "거문고와 비파 소리가 섞이듯 부부 화합이 완벽하여, 평생토록 함께 의지하며 즐거움을 누린다."},
                {"title": "", "hanja": "賢妻得財 (현처득재)", "text": "아내와 재물의 기운이 넘치도록 왕성하니 부부가 합심하여 집안을 평안하게 이끌고 탄탄한 부를 이룬다."}
            ]
        elif "관" in d_tg:
            return [
                {"title": "", "hanja": "夫婦相愛 (부부상애)", "text": "나를 통제하고 이끄는 기운이 배우자궁에 있으니 다소 억압됨이 있으나, 결국 서로 깊이 아끼고 사랑하게 된다."},
                {"title": "", "hanja": "家道和暢 (가도화창)", "text": "서로가 서로의 울타리가 되어주니 가정의 기운이 평안하게 뻗어 나가며, 흔들림 없이 가문을 지켜낸다."}
            ]
        else: # 인성, 식상
            return [
                {"title": "", "hanja": "母性夫婦 (모성부부)", "text": "배우자를 자식처럼 보살피거나, 반대로 어머니처럼 나의 모든 것을 품어주는 애틋한 인연이다."},
                {"title": "", "hanja": "百年同樂 (백년동락)", "text": "청장년의 험난하고 모진 일들이 다 지나가고, 흰 머리가 되어서 따뜻한 봄바람을 맞으며 백년해로한다."}
            ]

    def _get_children_wun(self, h_tg: str) -> list:
        if "재" in h_tg or "식" in h_tg or "상" in h_tg:
            return [
                {"title": "", "hanja": "時上福星 (시상복성)", "text": "태어난 시(말년)에 복을 내리는 별이 있으니, 중말년의 운이 천하 거부(금곡)가 부럽지 않다."},
                {"title": "", "hanja": "良田沃土 (양전옥토)", "text": "험사가 모두 지나가고 넓은 땅과 재물로 의식이 풍족해지니, 자손들이 평탄하게 번성하고 안락함을 누린다."}
            ]
        elif "비" in h_tg or "겁" in h_tg:
            return [
                {"title": "", "hanja": "晩年獨立 (만년독립)", "text": "말년 자식궁에 내 재물을 다투는 기운이 있으니, 자식에게 섣불리 재산을 넘기거나 기대려 해선 안 된다."},
                {"title": "", "hanja": "手散千金 (수산천금)", "text": "내 지갑은 내가 굳게 쥐어야 하며, 천금을 함부로 흩어버리면 후회막급일 것이니 끝까지 자립해야 평안하다."}
            ]
        else:
            return [
                {"title": "", "hanja": "險事已過 (험사이과)", "text": "초중년의 뼈아픈 시련과 험난한 일들이 이미 다 지나가고, 백발이 되어서야 태평한 봄바람을 맞는다."},
                {"title": "", "hanja": "老來誰共 (노래수공)", "text": "때로는 외기러기처럼 외로움이 닥치나, 맑은 정신으로 덕을 베풀고 선업을 쌓으면 노후의 근심이 풀릴 것이다."}
            ]

    def _get_phoenix(self, strength: str) -> list:
        if "신강" in strength or "극강" in strength:
            return [
                {"title": "", "hanja": "事雖速心 非理不行 (사수속심 비리불행)", "text": "매사에 마음이 아무리 급하고 서두르더라도, 도리와 이치에 어긋나는 일은 결코 행동에 옮기지 않는 위대한 신념을 가졌다."},
                {"title": "", "hanja": "立三立七 手弄千金 (입삼입칠 수롱천금)", "text": "운수가 뻗어 나가는 대운을 만나면, 천금 같은 거대한 재물을 내 손으로 거머쥐고 천하를 호령하게 될 것이다."}
            ]
        else:
            return [
                {"title": "", "hanja": "外財入內 (외재입내)", "text": "견디고 인내하며 때를 기다리면, 밖의 거대한 재물들이 봇물 터지듯 집 안으로 쏟아져 들어오게 된다."},
                {"title": "", "hanja": "聖世已遠 誰與覽德 (성세이원 수여람덕)", "text": "성인의 시대는 멀어졌으니, 이 혼탁한 세상에서 고독하게 땀 흘린 그대의 고결한 덕을 뉘와 나눌 것인가. 참으로 귀하고 단단한 영웅의 삶이다."}
            ]