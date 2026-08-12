# logic_gunghap.py

class GunghapEngine:
    def __init__(self):
        self.stars = {
            1: "일백수성(一白水星)", 2: "이흑토성(二黑土星)", 3: "삼벽목성(三碧木星)",
            4: "사록목성(四綠木星)", 5: "오황토성(五黃土星)", 6: "육백금성(六白金星)",
            7: "칠적금성(七赤金星)", 8: "팔백토성(八白土星)", 9: "구자화성(九紫火星)"
        }
        self.star_elements = {1: "수", 2: "토", 3: "목", 4: "목", 5: "토", 6: "금", 7: "금", 8: "토", 9: "화"}
        self.relations = {
            "충(沖)": [{"子", "午"}, {"丑", "未"}, {"寅", "申"}, {"卯", "酉"}, {"辰", "戌"}, {"巳", "亥"}],
            "원진(怨嗔)": [{"子", "未"}, {"丑", "午"}, {"寅", "酉"}, {"卯", "申"}, {"辰", "亥"}, {"巳", "戌"}],
            "귀문(鬼門)": [{"子", "酉"}, {"丑", "午"}, {"寅", "未"}, {"卯", "申"}, {"辰", "亥"}, {"巳", "戌"}],
            "파(破)": [{"子", "酉"}, {"卯", "午"}, {"寅", "亥"}, {"辰", "丑"}, {"申", "巳"}, {"戌", "未"}],
            "해(害)": [{"子", "未"}, {"丑", "午"}, {"寅", "巳"}, {"卯", "辰"}, {"申", "亥"}, {"酉", "戌"}],
            "육합(六合)": [{"子", "丑"}, {"寅", "亥"}, {"卯", "戌"}, {"辰", "酉"}, {"巳", "申"}, {"午", "未"}],
            "삼합(三合)": [{"亥", "卯", "未"}, {"寅", "午", "戌"}, {"巳", "酉", "丑"}, {"申", "子", "辰"}],
            "방합(方合)": [{"寅", "卯", "辰"}, {"巳", "午", "未"}, {"申", "酉", "戌"}, {"亥", "子", "丑"}]
        }

        # 🚨 [수정 완료] 다국어 철거 및 한국어 단일화
        self.samwon_db = [
            "상원갑", "만물이 태동하고 새롭게 시작되는 양(陽)의 기운이 팽배한 시대", "上元甲",
            "중원갑", "문명과 제도가 무르익고 기운이 중화되는 만개의 시대", "中元甲",
            "하원갑", "물질명리가 극에 달하고 정신적 성숙이 요구되는 음(陰)의 시대", "下元甲",
            "알 수 없음", "측정 범위를 벗어났습니다.", ""
        ]

        # 🚨 [수정 완료] 다국어 철거 및 한자 분리 준비
        self.eight_mansions_db = {
            "생기(生氣)": {"score": 100, "text": "하늘이 맺어준 완벽한 짝입니다. 부부가 합심하면 무에서 유를 창조할 만큼 재물과 자손이 폭발적으로 늘어납니다.", "classical": "貪生五子 (탐랑성의 기운을 받아 자손과 재물이 번창한다)", "timing": "돼지(亥), 토끼(卯), 양(未)의 해에 결실이 터집니다."},
            "천의(天醫)": {"score": 90, "text": "상처를 치유하는 귀인입니다. 부부의 멘탈이 안정되고 잔병치레가 사라지며 부동산 같은 굳건한 자산을 축적하게 됩니다.", "classical": "巨三郞 (거문성의 기운으로 건강하고 흔들림 없는 안정을 누린다)", "timing": "원숭이(申), 쥐(子), 용(辰)의 해에 막힌 운이 회복됩니다."},
            "연년(延年)": {"score": 85, "text": "연이 매우 질깁니다. 살면서 다투는 일이 있어도 절대 헤어지지 않으며, 나이가 들수록 큰 안정과 명예를 누립니다.", "classical": "武曲金星四子强 (음양의 화합이 강력하여 가문을 튼튼하게 지킨다)", "timing": "뱀(巳), 닭(酉), 소(丑)의 해에 큰 성취를 이룹니다."},
            "복위(伏位)": {"score": 75, "text": "거울을 보듯 편안한 동반자입니다. 굴곡 없는 평온함이 장점이나, 기운이 정체되어 극적인 발전은 기대하기 어렵고 권태로울 수 있습니다.", "classical": "輔弼知是半兒郞 (딸을 낳듯 큰 소란 없이 가문을 조용히 잇는다)", "timing": "돼지(亥), 토끼(卯), 양(未)의 해에 잔잔한 이득을 봅니다."},
            "화해(禍害)": {"score": 40, "text": "사소한 다툼이 관재구설과 소송으로 번집니다. 한발 물러서지 않으면 매사가 꼬이고 외부적 구설수나 사기에 휘말리기 쉽습니다.", "classical": "祿存土宿人遭殃 (잦은 다툼과 예측 불가능한 재앙, 구설에 휘말린다)", "timing": "호랑이(寅), 말(午), 개(戌)의 해에 구설이 터집니다."},
            "육살(六殺)": {"score": 30, "text": "감정 기복이 요동치며 재물이 새어나갑니다. 이성 문제, 유흥, 사치 등으로 인한 파재(破財)와 멘탈 파괴를 뼈저리게 경계해야 합니다.", "classical": "文曲水星僅一子 (구설과 풍파 속에 정서적 안정이 파괴된다)", "timing": "원숭이(申), 쥐(子), 용(辰)의 해에 숨겨진 치부가 드러납니다."},
            "오귀(五鬼)": {"score": 20, "text": "다섯 귀신이 씌인 듯 까닭 없는 불화와 탐욕이 들끓습니다. 이유 없는 의심이 잦고, 무리한 투자가 가정 경제를 완벽하게 파괴할 수 있습니다.", "classical": "廉貞獨火鬼兩箇 (통제 불가능한 불귀신처럼 다투며 탐욕이 화를 부른다)", "timing": "호랑이(寅), 말(午), 개(戌)의 해에 갈등과 파탄이 폭발합니다."},
            "절명(絶命)": {"score": 10, "text": "기운을 끊어내는 대흉살입니다. 서로 뼈를 깎아먹고 종국에는 재물이 박살 나거나(파산) 홀로 고독해지는 최악의 파국 조합입니다.", "classical": "破軍破財孤孀 (재물이 완전히 깨지고 홀로 남아 고독해지는 최악의 형국)", "timing": "뱀(巳), 닭(酉), 소(丑)의 해에 회복 불가한 재앙이 몰아칩니다."}
        }

        self.gender_dyn_db = {
            "bihwa": "【음양 조화】 [비화] 오행이 동일하여 전우처럼 끈끈합니다. 하지만 자존심이 충돌하면 어느 한쪽도 굽히지 않아 냉전이 극단적으로 길어집니다. 각자의 경제권을 철저히 분리해야 파국을 막습니다.",
            "m_f": "【음양 조화】 [남생여] 남편이 아내에게 무한한 에너지를 공급하고 희생합니다. 아내는 남편의 헌신을 딛고 발복하나, 남편의 멘탈과 기운이 지속적으로 빨려 나가니 아내의 명확한 보답이 없으면 파국이 옵니다.",
            "f_m": "【음양 조화】 [여생남] 아내가 남편을 완벽하게 내조하여 남편의 잠재력을 무한대로 폭발시킵니다. 가문이 크게 일어서나, 남편이 아내의 뼈 깎는 희생을 당연하게 여기면 아내의 건강이 처참하게 망가집니다.",
            "m_k_f": "【음양 조화】 [남극녀] 남편이 아내를 강하게 통제하는 전형적인 가부장적 형국입니다. 아내가 순응하면 집안이 흔들림 없이 돌아가나, 억압이 선을 넘으면 아내의 가슴에 맺힌 화병(원망)이 치명적인 질병으로 발현됩니다.",
            "f_k_m": "【음양 조화】 [여극남] 아내가 남편의 기를 완전히 꺾어누르고 가장 노릇을 하는 하극상(下剋上)의 흉상입니다. 남편이 자존심을 완벽히 버리지 못하면 폭력, 외도, 경제적 붕괴 등 끔찍한 파국으로 치달을 수 있는 극위험군 결합입니다."
        }

        self.inner_compat_db = {
            "bihwa": {"relation": "비화(比和)", "status": "권태롭고 편안한 동행", "desc": "【분석】 불타오르는 열정보다는 묵직한 신뢰와 동질감으로 가정을 이끕니다. 피로도는 낮으나 긴장감이 현저히 떨어져 심각한 섹스리스(권태기)에 빠질 위험이 매우 높으니 의식적인 이벤트가 절대적으로 필요합니다."},
            "6hap": {"relation": "육합(六合)", "status": "천상의 속궁합 (대길)", "desc": "【분석】 겉보기엔 무심해도 침소에 들면 자석처럼 미친 듯이 이끌립니다. 외도나 파산 등 거대한 흉파가 닥쳐도 결코 서로의 손을 놓지 못하는 무서운 육체적/정서적 결속력을 발휘합니다."},
            "3hap": {"relation": "삼합(三合)", "status": "의리와 안정의 결합", "desc": "【분석】 서로의 부족한 점을 든든하게 채워줍니다. 뜻이 잘 맞고 속궁합이 무던하여 큰 다툼 없이 안정적으로 재물을 불리고 가정을 번창시킵니다."},
            "banghap": {"relation": "방합(方合)", "status": "형제 같은 강한 결속", "desc": "【분석】 같은 방위의 기운으로 뭉쳐, 부부라기보다는 한 배를 탄 전우처럼 외부의 적에 맞서 가정을 억척스럽게 지켜내는 무서운 결속력입니다."},
            "choong": {"relation": "충(沖)", "status": "치명적 대립과 파괴 (극흉)", "desc": "【분석】 침실(부부궁)이 정면으로 들이받고 박살 나는 최악의 흉상입니다. 애정이 식는 순간 상대를 짓밟으려는 파괴적 증오심으로 돌변합니다. 철저한 각방이나 주말부부로 물리적 거리를 강제 확보하지 않으면 참담한 이별 서류를 쓰게 됩니다."},
            "wonjin": {"relation": "원진(怨嗔)", "status": "가학적 애증의 덫 (극흉)", "desc": "【분석】 밤에는 이성을 잃을 정도로 미치도록 끌리다가도, 낮에는 서로를 저주하며 물어뜯는 소모전이 무한 반복됩니다. 죽일 듯이 미워하면서도 헤어지려 하면 질척하게 얽혀서 절대 깔끔하게 떨어지지 못하는 피 말리는 애증의 사슬입니다."},
            "guimun": {"relation": "귀문(鬼門)", "status": "광적 집착과 신경쇠약 (흉)", "desc": "【분석】 성적, 정서적 의존도가 광적으로 치솟으며 상대의 일거수일투족을 통제하려 듭니다. 영혼이 통하는 짜릿함 이면에는 심각한 의처증, 의부증, 편집증으로 발현될 수 있는 초고위험군 폭탄이 숨겨져 있습니다."},
            "hyung": {"relation": "형(刑)", "status": "강압적 통제와 억압 (흉)", "desc": "【분석】 서로의 방식을 강제로 뜯어고치려 듭니다. 침실과 일상에서 끝없는 주도권 싸움이 벌어지며, 한쪽이 자존심을 완벽하게 꺾고 지배에 복종해야만 아슬아슬하게 유지되는 활화산 같은 결합입니다."},
            "pa_hae": {"relation": "파해(破害)", "status": "잠복된 균열과 이간질 (흉)", "desc": "【분석】 겉은 화목해 보이나 가장 밑바닥 신뢰에 치명적인 균열이 잠복해 있습니다. 위기의 순간 각자의 이기심이 발동하여 배신하거나, 외도 및 제3자의 이간질로 침실의 평화가 와장창 깨지기 쉽습니다."},
            "none": {"relation": "무해무덕(無害無德)", "status": "이성적이고 건조한 관계", "desc": "【분석】 강렬한 끌림도 치명적인 충돌도 없습니다. 육체적 황홀함보다는 철저히 자녀 양육, 경제적 목적을 위해 뭉친 비즈니스 파트너에 가깝습니다. 평온하게 유지되나 정서적 교류가 부족해 뼈저린 고독감이 평생 수반될 수 있습니다."}
        }

    # 🚨 문자열에서 이름과 한자를 분리하는 유틸리티
    def _split_name_hanja(self, raw_str: str) -> tuple:
        if "(" in raw_str and ")" in raw_str:
            parts = raw_str.split("(")
            return parts[0].strip(), parts[1].replace(")", "").strip()
        return raw_str, ""

    def _get_root_number(self, year: int) -> int:
        r = sum(int(digit) for digit in str(year))
        while r > 9:
            r = sum(int(digit) for digit in str(r))
        return r

    def get_samwon_gapja(self, year: int) -> dict:
        offset = year - 1864
        if offset < 0: return {"name": self.samwon_db[9], "hanja": self.samwon_db[11], "desc": self.samwon_db[10]}
            
        cycle = (offset % 180) // 60
        idx = cycle * 3
        return {"name": self.samwon_db[idx], "hanja": self.samwon_db[idx+2], "desc": self.samwon_db[idx+1]}

    def get_bonmyeongseong(self, year: int, gender: str) -> dict:
        root_num = self._get_root_number(year)
        if gender == 'M': star_num = (11 - root_num) % 9
        else: star_num = (4 + root_num) % 9
        if star_num == 0: star_num = 9
        
        star_full = self.stars[star_num]
        name_clean, hanja_clean = self._split_name_hanja(star_full)
        
        return {
            "number": star_num, 
            "name": name_clean,
            "hanja": hanja_clean
        }

    def get_gugung_compatibility(self, male_star: int, my_gender: str, female_star: int, p_gender: str) -> dict:
        m_trigram = 2 if male_star == 5 else male_star
        f_trigram = 8 if female_star == 5 else female_star
        pair = frozenset([m_trigram, f_trigram])
        
        if len(pair) == 1: match_result = "복위(伏位)"
        else:
            match_matrix = {
                frozenset([1, 4]): "생기(生氣)", frozenset([2, 8]): "생기(生氣)", frozenset([3, 9]): "생기(生氣)", frozenset([6, 7]): "생기(生氣)",
                frozenset([1, 3]): "천의(天醫)", frozenset([2, 6]): "천의(天醫)", frozenset([4, 9]): "천의(天醫)", frozenset([7, 8]): "천의(天醫)",
                frozenset([1, 9]): "연년(延年)", frozenset([2, 7]): "연년(延年)", frozenset([3, 4]): "연년(延年)", frozenset([6, 8]): "연년(延年)",
                frozenset([1, 7]): "화해(禍害)", frozenset([2, 3]): "화해(禍害)", frozenset([4, 6]): "화해(禍害)", frozenset([8, 9]): "화해(禍害)",
                frozenset([1, 6]): "육살(六殺)", frozenset([2, 9]): "육살(六殺)", frozenset([3, 8]): "육살(六殺)", frozenset([4, 7]): "육살(六殺)",
                frozenset([1, 8]): "오귀(五鬼)", frozenset([2, 4]): "오귀(五鬼)", frozenset([3, 6]): "오귀(五鬼)", frozenset([7, 9]): "오귀(五鬼)",
                frozenset([1, 2]): "절명(絶命)", frozenset([3, 7]): "절명(絶命)", frozenset([4, 8]): "절명(絶命)", frozenset([6, 9]): "절명(絶命)"
            }
            match_result = match_matrix.get(pair, "알 수 없음")

        b_data = self.eight_mansions_db.get(match_result, {"score": 0, "text": "-", "classical": "-", "timing": "-"})

        m_elem = self.star_elements[male_star]
        f_elem = self.star_elements[female_star]
        generates = {"목": "화", "화": "토", "토": "금", "금": "수", "수": "목"}
        overcomes = {"목": "토", "토": "수", "수": "화", "화": "금", "금": "목"}
        
        gender_dynamics = ""
        
        if m_elem == f_elem: gender_dynamics = self.gender_dyn_db["bihwa"]
        elif generates[m_elem] == f_elem: gender_dynamics = self.gender_dyn_db["m_f"]
        elif generates[f_elem] == m_elem: gender_dynamics = self.gender_dyn_db["f_m"]
        elif overcomes[m_elem] == f_elem: gender_dynamics = self.gender_dyn_db["m_k_f"]
        elif overcomes[f_elem] == m_elem: gender_dynamics = self.gender_dyn_db["f_k_m"]

        final_desc = f"【구궁 팔괘】 {b_data['text']}\n{gender_dynamics}"
        
        # 🚨 [수정 완료] 프론트엔드가 자를 필요 없도록 name과 hanja를 정규화
        name_clean, hanja_clean = self._split_name_hanja(match_result)

        return {
            "status": name_clean, 
            "hanja": hanja_clean,
            "score": b_data["score"], 
            "desc": final_desc, 
            "classical": b_data["classical"], 
            "timing": b_data["timing"]
        }

    def get_inner_compatibility(self, m_day_branch: str, f_day_branch: str) -> dict:
        if m_day_branch == f_day_branch: result_data = self.inner_compat_db["bihwa"]
        else:
            pair = {m_day_branch, f_day_branch}
            result_data = None
            if pair in self.relations["육합(六合)"]: result_data = self.inner_compat_db["6hap"]
            
            if not result_data:
                for samhap in self.relations["삼합(三合)"]:
                    if pair.issubset(samhap): result_data = self.inner_compat_db["3hap"]; break
                    
            if not result_data:
                for banghap in self.relations["방합(方合)"]:
                    if pair.issubset(banghap): result_data = self.inner_compat_db["banghap"]; break
                    
            if not result_data:
                if pair in self.relations["충(沖)"]: result_data = self.inner_compat_db["choong"]
                elif pair in self.relations["원진(怨嗔)"]: result_data = self.inner_compat_db["wonjin"]
                elif pair in self.relations["귀문(鬼門)"]: result_data = self.inner_compat_db["guimun"]
                elif pair in self.relations["파(破)"] or pair in self.relations["해(害)"]: result_data = self.inner_compat_db["pa_hae"]
                else: result_data = self.inner_compat_db["none"]

        # 🚨 [수정 완료] 속궁합 결과의 relation(예: "원진(怨嗔)")도 한자 분리 정규화
        name_clean, hanja_clean = self._split_name_hanja(result_data["relation"])
        
        return {
            "relation": name_clean,
            "hanja": hanja_clean,
            "status": result_data["status"],
            "desc": result_data["desc"]
        }