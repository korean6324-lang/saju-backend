# logic_classical.py

class ClassicalEngine:
    def __init__(self):
        # 정규화된 한국어 전용 당사주 DB (이름, 한자, 설명 완벽 분리)
        self.dang_saju = {
            "子": {"name": "천귀성", "hanja": "天貴星", "desc": "부귀영화와 총명함을 관장하는 기운. 타고난 두뇌가 비상하여 학업과 관직에서 두각을 나타내며 인덕이 따릅니다. 단, 자만심이 강해 타인을 얕잡아보기 쉬우니 겸손이 필수입니다."},
            "丑": {"name": "천액성", "hanja": "天厄星", "desc": "고난과 인내, 대기만성의 기운. 척박한 시련도 묵묵히 버텨내는 불굴의 의지가 있어 중말년에 거대한 성취를 이룹니다. 초중년의 풍파와 마음고생을 피할 수 없습니다."},
            "寅": {"name": "천권성", "hanja": "天權星", "desc": "권력과 통솔력을 상징하는 우두머리의 기운. 만인을 거느리는 카리스마가 탁월하여 조직을 장악합니다. 독단적인 성정 탓에 타인과의 마찰과 구설수가 잦습니다."},
            "卯": {"name": "천파성", "hanja": "天破星", "desc": "파재(破財)와 특수 기술을 관장하는 기운. 정교한 손재주와 예술, 전문 기술로 자수성가합니다. 다만 모은 재물이 흩어지거나 믿었던 인연과 이별을 겪는 굴곡이 있습니다."},
            "辰": {"name": "천간성", "hanja": "天奸星", "desc": "뛰어난 지략과 임기응변의 기운. 두뇌 회전이 빠르고 처세술이 능수능란하여 최악의 위기에서도 기지를 발휘합니다. 잦은 변덕과 잔꾀로 신뢰를 잃지 않도록 주의해야 합니다."},
            "巳": {"name": "천문성", "hanja": "天文星", "desc": "학문과 예술, 예리한 직관의 기운. 학자나 예술가로서 천재성을 발휘하며 고결한 품격을 지닙니다. 성정이 지나치게 예민하여 상처를 잘 받고 신경쇠약에 걸리기 쉽습니다."},
            "午": {"name": "천복성", "hanja": "天福星", "desc": "복록과 여유, 인덕을 상징하는 기운. 일생토록 의식주가 마르지 않고 귀인의 도움이 따르며 순탄합니다. 태생적 풍족함에 취해 나태해지고 투지가 부족해질 수 있습니다."},
            "未": {"name": "천역성", "hanja": "天驛星", "desc": "이동과 개척, 역마(驛馬)의 기운. 고향을 떠나 넓은 세상(해외, 유통, 영업)으로 나아가야 대운이 크게 열립니다. 평생 한곳에 정착하지 못해 삶의 피로도가 매우 높습니다."},
            "申": {"name": "천고성", "hanja": "天孤星", "desc": "고독과 자립, 깊은 철학의 기운. 누구에게도 의존하지 않는 자립심이 극강하여 연구, 종교, 철학 분야에서 일가를 이룹니다. 군중 속에서도 뼈저린 고독감을 자주 느끼게 됩니다."},
            "酉": {"name": "천인성", "hanja": "天刃星", "desc": "날카로운 결단력과 수술수(칼)의 기운. 맺고 끊음이 확실하여 의료, 사법, 금융, 군경 등 예리한 직업에서 대성합니다. 몸에 칼을 대거나 예리한 언행으로 적을 만들기 쉽습니다."},
            "戌": {"name": "천예성", "hanja": "天藝星", "desc": "정교한 재주와 장인정신의 기운. 남들이 흉내 내지 못할 독창성과 끈기로 한 분야를 깊게 파고들어 존경받습니다. 외골수 기질로 인해 타인과 원만하게 타협하기 어렵습니다."},
            "亥": {"name": "천수성", "hanja": "天壽星", "desc": "무병장수와 태평한 수용력의 기운. 성품이 온화하고 매사를 둥글게 수용하여 무병장수하며 말년에 큰 평안을 얻습니다. 거절을 못 해 끌려다니거나 결정적 기회를 놓칠 수 있습니다."}
        }

    def _get_dynamic_johu_desc(self, yongshin_str: str) -> str:
        base_text = f"이 명식에 가장 시급하고 귀중한 수호 에너지는 [{yongshin_str}]입니다. "
        if "목" in yongshin_str or "木" in yongshin_str:
            return base_text + "사주의 메마른 땅에 튼튼한 뿌리를 내리고 생명력을 불어넣는 귀중한 에너지입니다. 이 기운이 들어올 때 성장이 촉진되고 거대한 숲을 이루듯 번창하게 됩니다."
        elif "화" in yongshin_str or "火" in yongshin_str:
            return base_text + "사주의 얼어붙은 한기를 녹이고 어둠을 밝혀주는 한줄기 빛과 같은 에너지입니다. 이 기운이 들어올 때 얼어붙어 막혔던 일들이 풀리고 찬란한 결실을 맺게 됩니다."
        elif "토" in yongshin_str or "土" in yongshin_str:
            return base_text + "사주의 흔들리는 기운을 든든하게 지탱하고 범람하는 물결을 막아주는 튼튼한 제방 같은 에너지입니다. 이 기운이 들어올 때 삶의 기반이 굳건해지고 거대한 산처럼 안정됩니다."
        elif "금" in yongshin_str or "金" in yongshin_str:
            return base_text + "사주의 엉킨 기운을 예리하게 끊어내고 불필요한 가지를 쳐내는 결단력의 에너지입니다. 이 기운이 들어올 때 혼란이 정리되고 보석처럼 빛나는 가치를 세상에 인정받게 됩니다."
        elif "수" in yongshin_str or "水" in yongshin_str:
            return base_text + "사주의 끓어오르는 열기를 식혀주고 마른 대지를 윤택하게 적셔주는 생명수 같은 에너지입니다. 이 기운이 들어올 때 지독한 갈증이 해소되고 만물이 유연하게 흘러가게 됩니다."
        else:
            return base_text + "사주의 불균형을 해소하고 막힌 기운을 뚫어주는 절대적인 구원처가 되며, 이 기운이 들어올 때 비로소 삶의 조화가 완성됩니다."

    def _get_nature(self, d_stem: str, m_branch: str) -> str:
        s_map = {"寅":"초봄", "卯":"완연한 봄", "辰":"늦봄", "巳":"초여름", "午":"한여름", "未":"늦여름", "申":"초가을", "酉":"완연한 가을", "戌":"늦가을", "亥":"초겨울", "子":"한겨울", "丑":"꽁꽁 언 겨울"}
        e_map = {"甲":"우뚝 솟은 거목(巨木)", "乙":"강인한 생명력의 화초", "丙":"세상을 비추는 태양(太陽)", "丁":"어둠을 밝히는 용광로", "戊":"만물을 품는 거대한 산(大山)", "己":"비옥한 전답", "庚":"예리한 무쇠와 바위", "辛":"정교하게 세공된 보석", "壬":"거대한 바다", "癸":"대지를 적시는 생명수"}
        season = s_map.get(m_branch, "")
        element = e_map.get(d_stem, "")
        if not element: return "-"
        return f"당신은 {season}에 태어난 {element}의 기상을 품고 있습니다. 모진 비바람이 불어도 내면에는 절대 꺾이지 않는 무서운 자립심과 끈질긴 생존력을 타고난 명식입니다."

    # 🚨 [정통 고법 복원] 당사주 순차 연산 알고리즘
    def calculate_orthodox_dang_saju(self, year_branch: str, lunar_month: int, lunar_day: int, hour_branch: str) -> dict:
        branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        if year_branch not in branches:
            return {p: {"name_clean": "-", "hanja_clean": "", "desc": "-"} for p in ["year", "month", "day", "hour"]}

        # 1. 연성(초년): 띠(연지) 그대로
        y_idx = branches.index(year_branch)
        # 2. 월성(청년): 연성 기준에서 음력 월수만큼 전진
        m_idx = (y_idx + lunar_month - 1) % 12
        # 3. 일성(중년): 월성 기준에서 음력 일수만큼 전진
        d_idx = (m_idx + lunar_day - 1) % 12
        
        # 4. 시성(말년): 일성 기준에서 시지 인덱스만큼 전진
        h_star_idx = None
        if hour_branch in branches:
            h_idx = branches.index(hour_branch)
            h_star_idx = (d_idx + h_idx) % 12

        stars = {
            "year": branches[y_idx],
            "month": branches[m_idx],
            "day": branches[d_idx],
            "hour": branches[h_star_idx] if h_star_idx is not None else "-"
        }

        result = {}
        for p, branch_key in stars.items():
            if branch_key == "-":
                result[p] = {"name_clean": "시간 모름", "hanja_clean": "時柱未詳", "desc": "태어난 시간을 알 수 없어 말년의 당사주를 판별하지 않습니다."}
            else:
                db_data = self.dang_saju[branch_key]
                result[p] = {"name_clean": db_data["name"], "hanja_clean": db_data["hanja"], "desc": db_data["desc"]}
        return result

    # 🚨 [정통 고법 복원] 납음오행 초년-말년 생극제화 스캐너
    def _get_napeum_interaction(self, y_napeum: str, h_napeum: str) -> list:
        if not y_napeum or not h_napeum or y_napeum == "-" or h_napeum == "-" or "모름" in h_napeum:
            return [{"title": "판별 불가", "hanja": "未詳", "text": "태어난 시간을 알 수 없어 초년과 말년의 납음오행 상호작용을 판별할 수 없습니다."}]

        y_elem = y_napeum[-1]
        h_elem = h_napeum[-1]
        
        valid_elems = ["목", "화", "토", "금", "수"]
        if y_elem not in valid_elems or h_elem not in valid_elems:
            return [{"title": "판별 불가", "hanja": "未詳", "text": "납음오행 정보가 부족하여 상호작용을 판별할 수 없습니다."}]

        generates = {"목":"화", "화":"토", "토":"금", "금":"수", "수":"목"}
        overcomes = {"목":"토", "토":"수", "수":"화", "화":"금", "금":"목"}

        if y_elem == h_elem:
            return [{"title": "비화(比和) - 초지일관", "hanja": "初志一貫", "text": f"초년({y_elem})과 말년({h_elem})의 파동이 동일합니다. 평생토록 기운이 흔들리지 않으며, 한 분야를 고집스럽게 파고들어 일가를 이룹니다. 기복 없이 굳건한 생을 누립니다."}]
        elif generates[y_elem] == h_elem:
            return [{"title": "상생(相生) - 연생시", "hanja": "根生果", "text": f"초년의 뿌리({y_elem})가 말년의 성과({h_elem})를 생(生)하는 대길의 형국입니다. 조상의 은덕과 젊은 시절의 땀방울이 노후에 이르러 거대한 부와 번창으로 찬란하게 만개합니다."}]
        elif generates[h_elem] == y_elem:
            return [{"title": "상생(相生) - 시생연", "hanja": "果生根", "text": f"말년의 기운({h_elem})이 초년의 뿌리({y_elem})를 다시 윤택하게 돕는 형국입니다. 스스로 일군 말년의 영광과 자손의 성공이 오히려 가문을 크게 빛내고 명예를 드높입니다."}]
        elif overcomes[y_elem] == h_elem:
            return [{"title": "상극(相剋) - 연극시", "hanja": "先勝後憂", "text": f"초년의 강한 기운({y_elem})이 말년의 흉({h_elem})을 통제하고 다스리는 형국입니다. 중말년에 찾아오는 위기나 방황을 젊은 시절 다져놓은 탄탄한 자산과 인맥으로 완벽하게 제압해 냅니다."}]
        elif overcomes[h_elem] == y_elem:
            return [{"title": "상극(相剋) - 시극연", "hanja": "下剋上", "text": f"말년의 기운({h_elem})이 초년의 뿌리({y_elem})를 정면으로 치는 흉상입니다. 중말년에 이르러 주거지, 직업, 가치관이 180도 뒤바뀌는 대격변을 겪게 되며 낡은 껍질을 부수고 나오는 뼈아픈 혁신이 필요합니다."}]
        return []

    # 🚨 [통합 렌더링]
    def generate_classical_reading(self, formatted_bazi: dict, yongshin_data: dict, gender: str, lunar_month: int, lunar_day: int) -> list:
        readings = []
        gender_title = "乾命 (건명 : 남성)" if gender == "M" else "坤命 (곤명 : 여성)"

        # 1. 기질 및 조후 (신법/고법 공통)
        yongshin_str = yongshin_data.get("yongshin", {}).get("yongshin", str(yongshin_data.get("yongshin", "-"))) if isinstance(yongshin_data, dict) else str(yongshin_data)
        readings.append({
            "section": f"1. {gender_title} 사주 원국 기질 분석",
            "items": [
                {"title": "기질 (氣質)", "hanja": "", "text": self._get_nature(formatted_bazi["day"]["stem"], formatted_bazi["month"]["branch"])},
                {"title": "조후 (調候)", "hanja": "", "text": self._get_dynamic_johu_desc(yongshin_str)}
            ]
        })

        # 2. 당사주 (정통 순차 연산 적용)
        ds = self.calculate_orthodox_dang_saju(formatted_bazi["year"]["branch"], lunar_month, lunar_day, formatted_bazi["hour"]["branch"])
        readings.append({
            "section": "2. 당사주(唐四柱) 인생 사계절 흐름",
            "items": [
                {"title": "초년 (전생과 조상궁)", "hanja": ds["year"]["hanja_clean"], "text": f"[{ds['year']['name_clean']}] {ds['year']['desc']}"},
                {"title": "청년 (부모와 직업궁)", "hanja": ds["month"]["hanja_clean"], "text": f"[{ds['month']['name_clean']}] {ds['month']['desc']}"},
                {"title": "중년 (본인과 부부궁)", "hanja": ds["day"]["hanja_clean"], "text": f"[{ds['day']['name_clean']}] {ds['day']['desc']}"},
                {"title": "말년 (자식과 노후궁)", "hanja": ds["hour"]["hanja_clean"], "text": f"[{ds['hour']['name_clean']}] {ds['hour']['desc']}"}
            ]
        })

        # 3. 납음오행 상호작용 (신규 이식)
        y_napeum = formatted_bazi["year"].get("napeum", "-").split("(")[0]
        h_napeum = formatted_bazi["hour"].get("napeum", "-").split("(")[0]
        readings.append({
            "section": "3. 납음오행(納音五行) 초말년 생극제화",
            "items": self._get_napeum_interaction(y_napeum, h_napeum)
        })

        # 4. 그릇 (봉황)
        strength = yongshin_data.get("strength", {}).get("status", "") if isinstance(yongshin_data, dict) else ""
        if "신강" in strength or "극강" in strength:
            hero_items = [{"title": "압도적 주체성", "hanja": "事雖速心 非理不行", "text": "매사에 마음이 급하더라도 도리에 어긋나는 짓은 결코 하지 않는 위대한 신념을 가졌습니다. 운수가 뻗는 대운을 만나면 천금을 쥐고 천하를 호령할 명입니다."}]
        else:
            hero_items = [{"title": "인내와 수용력", "hanja": "外財入內", "text": "자신을 낮추고 지독하게 인내하며 때를 기다리는 저력이 있습니다. 시기가 도래하면 밖의 거대한 재물들이 봇물 터지듯 들어오는 고결한 영웅의 삶입니다."}]
        
        readings.append({"section": "4. 鳳凰 (봉황 : 인생관과 영웅의 그릇)", "items": hero_items})

        return readings