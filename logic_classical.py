# logic_classical.py

class ClassicalEngine:
    def __init__(self):
        # 🚨 [CTO 지시] 당사주 DB(self.dang_saju) 전면 제거 완료
        pass

    def _get_nature(self, d_stem: str, m_branch: str) -> str:
        s_map = {"寅":"초봄", "卯":"완연한 봄", "辰":"늦봄", "巳":"초여름", "午":"한여름", "未":"늦여름", "申":"초가을", "酉":"완연한 가을", "戌":"늦가을", "亥":"초겨울", "子":"한겨울", "丑":"꽁꽁 언 겨울"}
        e_map = {"甲":"우뚝 솟은 거목(巨木)", "乙":"강인한 생명력의 화초", "丙":"세상을 비추는 태양(太陽)", "丁":"어둠을 밝히는 용광로", "戊":"만물을 품는 거대한 산(大山)", "己":"비옥한 전답", "庚":"예리한 무쇠와 바위", "辛":"정교하게 세공된 보석", "壬":"거대한 바다", "癸":"대지를 적시는 생명수"}
        season = s_map.get(m_branch, "")
        element = e_map.get(d_stem, "")
        if not element: return "-"
        return f"당신은 {season}에 태어난 {element}의 기상을 품고 있습니다. 모진 비바람이 불어도 내면에는 절대 꺾이지 않는 무서운 자립심과 끈질긴 생존력을 타고난 명식입니다."

    # 🚨 [CTO 지시] calculate_orthodox_dang_saju() 및 _get_dynamic_johu_desc() 전면 제거 완료

    # 납음오행 상호작용 생극제화 스캐너 (보존)
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

    # 🚨 [통합 렌더링] 당사주/조후 제거 및 3대 핵심 텍스트만 리턴하도록 초경량화
    def generate_classical_reading(self, formatted_bazi: dict, yongshin_data: dict, strength_data: dict, gender: str, lunar_month: int, lunar_day: int) -> list:
        readings = []
        gender_title = "乾命 (건명 : 남성)" if gender == "M" else "坤命 (곤명 : 여성)"

        # 1. 기질 분석 (조후 텍스트 제거)
        readings.append({
            "section": f"1. {gender_title} 사주 원국 기질 분석",
            "items": [
                {"title": "기질 (氣質)", "hanja": "", "text": self._get_nature(formatted_bazi["day"]["stem"], formatted_bazi["month"]["branch"])}
            ]
        })

        # 2. 납음오행 상호작용
        y_napeum = formatted_bazi["year"].get("napeum", "-").split("(")[0]
        h_napeum = formatted_bazi["hour"].get("napeum", "-").split("(")[0]
        readings.append({
            "section": "2. 납음오행(納音五行) 초말년 생극제화",
            "items": self._get_napeum_interaction(y_napeum, h_napeum)
        })

        # 3. 그릇 (봉황)
        strength = strength_data.get("status", "")
        if "신강" in strength or "극강" in strength:
            hero_items = [{"title": "압도적 주체성", "hanja": "事雖速心 非理不行", "text": "매사에 마음이 급하더라도 도리에 어긋나는 짓은 결코 하지 않는 위대한 신념을 가졌습니다. 운수가 뻗는 대운을 만나면 천금을 쥐고 천하를 호령할 명입니다."}]
        else:
            hero_items = [{"title": "인내와 수용력", "hanja": "外財入內", "text": "자신을 낮추고 지독하게 인내하며 때를 기다리는 저력이 있습니다. 시기가 도래하면 밖의 거대한 재물들이 봇물 터지듯 들어오는 고결한 영웅의 삶입니다."}]
        
        readings.append({"section": "3. 鳳凰 (봉황 : 인생관과 영웅의 그릇)", "items": hero_items})

        return readings