# logic_dynamics.py

EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 오행 맵핑 (개두/절각 분석용)
ELEMENTS = {
    "목": ["甲", "乙", "寅", "卯"],
    "화": ["丙", "丁", "巳", "午"],
    "토": ["戊", "己", "辰", "戌", "丑", "未"],
    "금": ["庚", "辛", "申", "酉"],
    "수": ["壬", "癸", "亥", "子"]
}

# 오행 상극 관계 (key가 value를 극함)
CLASH_MAP = {"목": "토", "토": "수", "수": "화", "화": "금", "금": "목"}

# 🚨 [수정 완료] 하드코딩(괄호) 제거 및 딕셔너리 키 정규화
RELATIONS = {
    "충": [{"子", "午"}, {"丑", "未"}, {"寅", "申"}, {"卯", "酉"}, {"辰", "戌"}, {"巳", "亥"}],
    "원진": [{"子", "未"}, {"丑", "午"}, {"寅", "酉"}, {"卯", "申"}, {"辰", "亥"}, {"巳", "戌"}],
    "귀문": [{"子", "酉"}, {"丑", "午"}, {"寅", "未"}, {"卯", "申"}, {"辰", "亥"}, {"巳", "戌"}],
    "천라지망": [{"戌", "亥"}, {"辰", "巳"}],
    "형": [{"寅", "巳"}, {"巳", "申"}, {"寅", "申"}, {"丑", "戌"}, {"戌", "未"}, {"丑", "未"}, {"子", "卯"}],
    "자형": [{"辰"}, {"午"}, {"酉"}, {"亥"}], 
    "파": [{"子", "酉"}, {"丑", "辰"}, {"寅", "亥"}, {"卯", "午"}, {"巳", "申"}, {"戌", "未"}],
    "해": [{"子", "未"}, {"丑", "午"}, {"寅", "巳"}, {"卯", "辰"}, {"申", "亥"}, {"酉", "戌"}],
    "육합": [{"子", "丑"}, {"寅", "亥"}, {"卯", "戌"}, {"辰", "酉"}, {"巳", "申"}, {"午", "未"}]
}

# 🚨 [수정 완료] 한자 및 텍스트 구조화 (JSON 파싱 최적화)
SPECIAL_STARS_DB = {
    "천을귀인": {"hanja": "天乙貴人", "desc": "【특징】 사주 내 최고의 길성(吉星).\n【분석】 인생의 치명적인 위기나 재액이 닥칠 때, 보이지 않는 귀인의 강한 조력이 개입하여 흉(凶)을 길(吉)로 탈바꿈시킵니다. 인덕이 깊고 난관을 돌파하는 가장 강력한 영적 보호막입니다."},
    "문창귀인": {"hanja": "文昌貴人", "desc": "【특징】 비상한 두뇌와 학문적 재능을 관장하는 길성.\n【분석】 타고난 추리력과 암기력, 뛰어난 기획력과 글재주를 부여합니다. 학자, 교육, 연구, 작가 등의 직무에서 압도적인 지적 성취를 거두며, 위기를 지혜로 모면하는 기운입니다."},
    "도화살": {"hanja": "桃花殺", "desc": "【특징】 대중의 강렬한 시선과 인기를 블랙홀처럼 끌어당기는 기운.\n【분석】 방송, 연예, 마케팅, 유통, 정치 등 타인의 주목을 받아야 성공하는 현대 사회 최고의 무기입니다. 다만 기운을 바르게 쓰지 못하면 이성 구설수나 사치, 주색잡기로 인한 파재(破財)를 겪습니다."},
    "역마살": {"hanja": "驛馬殺", "desc": "【특징】 강제적이고 역동적인 이동과 개척의 에너지.\n【분석】 한곳에 갇혀있으면 병이 나며, 무역, 외교, 항공, 영업, 운수업 등 활동 반경을 전 세계로 넓힐 때 폭발적으로 발복합니다. 주거지나 직업의 잦은 변동으로 심신의 피로도가 높습니다."},
    "화개살": {"hanja": "華蓋殺", "desc": "【특징】 세속의 화려함을 덮고 정신적 고결함을 추구하는 고독의 별.\n【분석】 예술, 철학, 종교, 명리, 심리학 분야에서 타인이 범접 불가한 천재성과 통찰력을 보입니다. 세속적 욕망을 초월하려는 내면의 고독감과 정신적 번뇌가 평생 수반됩니다."},
    "백호대살": {"hanja": "白虎大殺", "desc": "【특징】 맹호의 물어뜯는 살기. 압도적인 프로페셔널 에너지.\n【분석】 기운이 흉폭하고 급진적이나, 이 살기를 직업(군인, 경찰, 사법, 의료, 정육, 특수기술)으로 승화(업상대체)시키면 해당 분야의 최고 권위자에 오릅니다. 핏빛 돌발사고와 감정의 폭발을 평생 경계해야 합니다."},
    "괴강살": {"hanja": "魁罡殺", "desc": "【특징】 북두칠성의 으뜸을 뜻하는 극강의 주체성과 카리스마.\n【분석】 타인의 지배를 극도로 혐오하고 굽힐 줄 모르는 강직함으로 거대 조직의 우두머리가 됩니다. 길흉의 극단성이 강해 대부대귀(大富大貴)하거나 한순간에 추락할 수 있는 양날의 검입니다."},
    "양인살": {"hanja": "羊刃殺", "desc": "【특징】 양의 목을 찌르는 날카로운 칼날의 흉폭한 기운.\n【분석】 불굴의 승부욕과 잔인하리만치 집요한 추진력을 뜻합니다. 펜이나 메스를 강하게 쥐는 전문직에서 대성하지만, 성정이 지나치게 강고하여 타인과의 잦은 마찰, 수술수, 부상을 조심해야 합니다."}
}

DISASTERS_DB = {
    "충": {"hanja": "沖", "desc": "【특징】 두 기운이 정면으로 충돌하여 박살 나는 파괴적 형국.\n【분석】 주거지, 직장, 건강, 부부 관계에서의 갑작스러운 붕괴와 이동을 겪게 됩니다. 그러나 낡고 썩은 환경을 강제로 부수고 새로운 기회를 창출하는 개척의 발판이 되기도 합니다."},
    "원진": {"hanja": "怨嗔", "desc": "【특징】 서로를 까닭 없이 밀어내고 원망하는 극심한 애증의 살.\n【분석】 대인관계나 부부 사이에서 오해, 집착, 히스테리가 빈발합니다. 떨어지면 그립고 만나면 물어뜯는 소모적인 관계망에 갇히기 쉬우니 철저한 감정 분리가 필요합니다."},
    "귀문": {"hanja": "鬼門", "desc": "【특징】 귀신이 드나드는 문. 영적이고 신경학적인 초감각 상태.\n【분석】 남들이 보지 못하는 이면을 꿰뚫어 보는 비상한 통찰력과 예술적 영감을 주지만, 스트레스 임계점을 넘으면 심각한 신경쇠약, 편집증, 불면증으로 발현될 수 있으니 정신 건강 관리가 필수적입니다."},
    "천라지망": {"hanja": "天羅地網", "desc": "【특징】 하늘과 땅에 촘촘히 쳐진 피할 수 없는 옥망(그물).\n【분석】 일신의 억압과 정지를 의미합니다. 육체적/사회적 제약이 따르므로, 군경, 사법, 의료, 교육, 종교 등 '타인을 구제하고 가두는 활인업(活人業)'에 종사해야만 이 흉액을 무사히 업상대체 할 수 있습니다."},
    "형": {"hanja": "刑", "desc": "【특징】 형벌을 가하고 살을 도려내는 조정과 수술의 기운.\n【분석】 법적 구설수, 소송, 징계, 몸에 칼을 대는 수술수를 경고합니다. 본인 스스로 권력을 쥐고 메스나 법봉을 휘두르는 직업을 가지면 흉살이 오히려 거대한 권위로 탈바꿈합니다."},
    "자형": {"hanja": "自刑", "desc": "【특징】 타인이 아닌 본인 스스로 형벌을 가하는 자학적 흉살.\n【분석】 내부적인 자기분열, 비관, 자기파괴적 충동, 우울증을 야기합니다. 완벽주의적 성향을 버리고 심리적 강박에서 스스로 벗어나는 훈련이 시급합니다."},
    "파": {"hanja": "破", "desc": "【특징】 견고하던 내부 결속에 치명적인 균열이 생기는 파괴운.\n【분석】 다 완성된 계약의 돌발적인 파기, 믿었던 인간관계의 배신, 재물의 손실을 야기합니다. 일이 매듭지어질 무렵 나타나는 돌발 변수에 대한 이중 삼중의 철저한 대비가 필요합니다."},
    "해": {"hanja": "害", "desc": "【특징】 겉은 멀쩡하나 속으로 곪아들어 상처를 남기는 이간질의 기운.\n【분석】 가장 가까운 사이에서 발생하는 은밀한 배신, 오해, 서운함을 뜻합니다. 의도치 않게 서로에게 해를 끼치며 심리적 멍을 남기므로 섣부른 맹신을 금해야 합니다."},
    "육합": {"hanja": "六合", "desc": "【특징】 음양이 자석처럼 밀착하는 1:1의 가장 강력하고 은밀한 결속.\n【분석】 부부 사이에서는 끈끈한 속궁합과 뗄 수 없는 애정으로 발현되며, 비즈니스에서는 배신이 없는 단단한 동맹과 극비 프로젝트의 결성으로 이어지는 강한 상호 끌림입니다."}
}

class DynamicsEngine:
    def __init__(self):
        pass

    def _get_element(self, char: str) -> str:
        for elem, chars in ELEMENTS.items():
            if char in chars:
                return elem
        return None

    def scan_heoja(self, branches: list) -> dict:
        """
        허자(虛字) 스캐너: 공협(拱挾)과 도충(倒沖) 색출
        """
        heoja_result = {"gonghyeop": [], "dochung": []}
        
        for i in range(len(branches) - 1):
            if branches[i] == branches[i+1]:
                idx = EARTHLY_BRANCHES.index(branches[i])
                dochung_char = EARTHLY_BRANCHES[(idx + 6) % 12]
                heoja_result["dochung"].append({
                    "trigger": f"{branches[i]}{branches[i+1]}",
                    "brought_char": dochung_char,
                    "position": f"{i}열-{i+1}열 사이"
                })
                
        for i in range(len(branches) - 1):
            if branches[i] == "-" or branches[i+1] == "-": continue
            idx1 = EARTHLY_BRANCHES.index(branches[i])
            idx2 = EARTHLY_BRANCHES.index(branches[i+1])
            
            diff = abs(idx1 - idx2)
            if diff == 2 or diff == 10:
                missing_idx = (min(idx1, idx2) + 1) % 12 if diff == 2 else (max(idx1, idx2) + 1) % 12
                gong_char = EARTHLY_BRANCHES[missing_idx]
                heoja_result["gonghyeop"].append({
                    "trigger": f"{branches[i]}와 {branches[i+1]}",
                    "brought_char": gong_char,
                    "position": f"{i}열-{i+1}열 사이"
                })
                
        return heoja_result

    def scan_special_stars(self, stems_dict: dict, branches_dict: dict) -> list:
        """전문가용 심층 신살 스캐너 (객체 리스트 반환)"""
        results = []
        
        day_stem = stems_dict.get("day", "")
        day_branch = branches_dict.get("day", "")
        year_branch = branches_dict.get("year", "")

        cheon_eul = {"甲":["丑","未"], "戊":["丑","未"], "庚":["丑","未"], "乙":["子","申"], "己":["子","申"], "丙":["亥","酉"], "丁":["亥","酉"], "辛":["午","寅"], "壬":["卯","巳"], "癸":["卯","巳"]}
        mun_chang = {"甲":"巳", "乙":"午", "丙":"申", "戊":"申", "丁":"酉", "己":"酉", "庚":"亥", "辛":"子", "壬":"寅", "癸":"卯"}
        yang_in = {"甲":"卯", "丙":"午", "戊":"午", "庚":"酉", "壬":"子"}

        baekho = ["甲辰", "乙未", "丙戌", "丁丑", "戊辰", "壬戌", "癸丑"]
        goegang = ["庚辰", "庚戌", "壬辰", "壬戌", "戊戌"]

        pillar_names = {"year": "연지", "month": "월지", "day": "일지", "hour": "시지"}
        pillar_ganzhi_names = {"year": "연주", "month": "월주", "day": "일주", "hour": "시주"}

        temp_stars = {
            "천을귀인": [], "문창귀인": [], "도화살": [], "역마살": [], "화개살": [],
            "백호대살": [], "괴강살": [], "양인살": []
        }

        for pillar_key, branch in branches_dict.items():
            if branch == "-": continue
            b_name = pillar_names.get(pillar_key, "")
            gz_name = pillar_ganzhi_names.get(pillar_key, "")
            stem = stems_dict.get(pillar_key, "")
            ganzhi = stem + branch

            if branch in cheon_eul.get(day_stem, []): temp_stars["천을귀인"].append(f"{b_name}({branch})")
            if branch == mun_chang.get(day_stem): temp_stars["문창귀인"].append(f"{b_name}({branch})")
            if branch == yang_in.get(day_stem): temp_stars["양인살"].append(f"{b_name}({branch})")
                
            if ganzhi in baekho: temp_stars["백호대살"].append(f"{gz_name}({ganzhi})")
            if ganzhi in goegang: temp_stars["괴강살"].append(f"{gz_name}({ganzhi})")

        def get_12_stars(ref_branch):
            if ref_branch in ["申", "子", "辰"]: return {"도화":"酉", "역마":"寅", "화개":"辰"}
            if ref_branch in ["寅", "午", "戌"]: return {"도화":"卯", "역마":"申", "화개":"戌"}
            if ref_branch in ["亥", "卯", "未"]: return {"도화":"子", "역마":"巳", "화개":"未"}
            if ref_branch in ["巳", "酉", "丑"]: return {"도화":"午", "역마":"亥", "화개":"丑"}
            return {}

        ref_stars_day = get_12_stars(day_branch)
        ref_stars_year = get_12_stars(year_branch)

        for pillar_key, branch in branches_dict.items():
            if branch == "-": continue
            b_name = pillar_names.get(pillar_key, "")
            for star_name in ["도화", "역마", "화개"]:
                if branch in [ref_stars_day.get(star_name), ref_stars_year.get(star_name)] and branch is not None:
                    item = f"{b_name}({branch})"
                    full_name = f"{star_name}살"
                    if item not in temp_stars[full_name]:
                        temp_stars[full_name].append(item)

        # 🚨 [수정 완료] 프론트엔드가 자를 필요 없이 name_clean, hanja_clean을 명확히 전달
        for star_type, positions in temp_stars.items():
            if positions:
                db_info = SPECIAL_STARS_DB.get(star_type, {"hanja": "", "desc": "상세 정보가 업데이트 중입니다."})
                results.append({
                    "name": star_type, 
                    "name_clean": star_type,
                    "hanja_clean": db_info["hanja"],
                    "position": ", ".join(positions),
                    "desc": db_info["desc"]
                })
        return results

    def scan_disasters(self, branches: list) -> list:
        """상호작용 및 흉액 스캐너 (객체 리스트 반환)"""
        results = []
        temp_disasters = {key: [] for key in RELATIONS.keys()}
        
        for i in range(len(branches)):
            for j in range(i + 1, len(branches)):
                if branches[i] == "-" or branches[j] == "-": continue
                pair = {branches[i], branches[j]}
                
                for rel_name, rel_list in RELATIONS.items():
                    if pair in rel_list:
                        if rel_name == "천라지망":
                            if pair == {"戌", "亥"}: temp_disasters[rel_name].append(f"{branches[i]}{branches[j]}(천라)")
                            elif pair == {"辰", "巳"}: temp_disasters[rel_name].append(f"{branches[i]}{branches[j]}(지망)")
                        else:
                            item = f"{branches[i]}{branches[j]}"
                            if item not in temp_disasters[rel_name]:
                                temp_disasters[rel_name].append(item)
                                
        # 🚨 [수정 완료] 프론트엔드가 자를 필요 없이 name_clean, hanja_clean을 명확히 전달
        for d_type, positions in temp_disasters.items():
            if positions:
                db_info = DISASTERS_DB.get(d_type, {"hanja": "", "desc": "상세 정보가 업데이트 중입니다."})
                results.append({
                    "name": d_type,
                    "name_clean": d_type,
                    "hanja_clean": db_info["hanja"],
                    "position": ", ".join(positions),
                    "desc": db_info["desc"]
                })
        return results

    def check_gaedu_jeolgak(self, stem: str, branch: str) -> dict:
        """개두(蓋頭)와 절각(截脚) 판별기"""
        stem_elem = self._get_element(stem)
        branch_elem = self._get_element(branch)
        
        result = {"status": "상생/비화(안정)", "desc": "상극이 없는 안정적인 기둥"}
        
        if not stem_elem or not branch_elem:
            return result
            
        if CLASH_MAP.get(stem_elem) == branch_elem:
            result = {"status": "개두(蓋頭)", "desc": f"천간({stem_elem})이 지지({branch_elem})를 극함. 하늘이 땅을 억누르는 형국."}
        elif CLASH_MAP.get(branch_elem) == stem_elem:
            result = {"status": "절각(截脚)", "desc": f"지지({branch_elem})가 천간({stem_elem})을 극함. 땅이 머리를 치는 형국으로 실속이 떨어짐."}
            
        return result