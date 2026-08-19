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

# 🌟 핵심 패치: 길성의 남녀 차이를 완벽히 분리한 이원화 DB
SPECIAL_STARS_DB = {
    "천을귀인": {
        "hanja": "天乙貴人", 
        "desc_common": "인생의 치명적인 위기가 닥칠 때, 보이지 않는 귀인의 강한 조력이 개입하여 흉(凶)을 길(吉)로 탈바꿈시키는 사주 내 최고의 길성입니다.",
        "desc_M": "【남성의 기운】 주로 사회적 성공과 출세의 강력한 치트키로 작용합니다. 권력자나 직장 상사(스승)의 발탁으로 초고속 승진을 하거나, 훌륭한 처가(아내)를 만나 가세가 크게 일어나는 축복입니다.",
        "desc_F": "【여성의 기운】 주로 인덕과 든든한 보호막(남편복)으로 작용합니다. 현대에는 압도적인 인맥과 후원을 바탕으로 사회에서 성공하는 주체적인 여성 CEO나 정치가의 가장 강력한 무기가 됩니다."
    },
    "문창귀인": {
        "hanja": "文昌貴人", 
        "desc_common": "비상한 두뇌와 타고난 추리력, 암기력, 기획력과 글재주를 부여하는 학문과 지혜의 길성입니다.",
        "desc_M": "【남성의 기운】 학자, 공직, 연구, 전문직으로 진출하여 무난하게 명예를 얻고, 위기가 닥쳐도 기가 막힌 지혜로 모면하며 가문을 빛냅니다.",
        "desc_F": "【여성의 기운】 똑똑하고 지혜로워 가정을 훌륭하게 이끕니다. 현대에는 남편에게 의존하지 않고 전문직(교수, 작가, 의사)으로 자립하는 당당하고 주체적인 커리어우먼의 상징입니다."
    },
    "도화살": {
        "hanja": "桃花殺", 
        "desc_common": "대중의 강렬한 시선과 인기를 블랙홀처럼 끌어당깁니다. 방송, 연예, 마케팅 등 타인의 주목을 받아야 성공하는 현대 사회 최고의 무기입니다.",
        "desc_M": "【남성의 기운】 매력이 넘쳐 사회생활(영업)에 매우 유리합니다. 다만 자제력이 없으면 주색잡기나 유흥에 재산을 탕진하고 잦은 스캔들로 가정을 파탄 내는 '색난(色難)'을 평생 경계해야 합니다.",
        "desc_F": "【여성의 기운】 화장과 치장에 능하고 사람을 홀리는 묘한 매력이 있습니다. 다만 본인이 원치 않아도 남자가 꼬이는 형국이라 스토킹, 구설수, 피곤한 연애사에 휘말릴 위험이 남성보다 훨씬 큽니다."
    },
    "역마살": {
        "hanja": "驛馬殺", 
        "desc_common": "강제적이고 역동적인 이동과 개척의 에너지입니다. 한곳에 갇혀있으면 병이 나며, 활동 반경을 넓힐 때 폭발적으로 발복합니다.",
        "desc_M": "【남성의 기운】 무역, 외교, 운수업, 해외 영업 등 전 세계를 무대로 뛰며 거대한 부를 창출합니다. 다만 객지 생활이 길어 가정에 소홀해지기 쉬운 외로운 장수의 기운입니다.",
        "desc_F": "【여성의 기운】 살림만 하려 들면 우울증이 옵니다. 뛰어난 생활력과 활동성으로 남편 이상으로 사회에서 맹활약하는 여장부입니다. 해외와 인연이 깊습니다."
    },
    "화개살": {
        "hanja": "華蓋殺", 
        "desc_common": "예술, 철학, 종교 분야에서 천재성과 통찰력을 보입니다. 세속의 화려함을 덮고 정신적 고결함을 추구하는 내면의 고독과 번뇌가 수반됩니다.",
        "desc_M": "【남성의 기운】 학문이나 종교, 철학 등 한 분야에 깊이 빠져들어 도인이나 대가(大家)가 됩니다. 속세를 초월하려는 기질 탓에 가족들이 경제적으로 피곤할 수는 있습니다.",
        "desc_F": "【여성의 기운】 화려함을 덮고 고독을 씹는 기운이라, 남성보다 '독수공방(외로움)'의 타격이 훨씬 큽니다. 결혼 후에도 정서적 단절감을 겪기 쉬우니 예술이나 종교(봉사)로 반드시 기운을 승화시켜야 합니다."
    },
    "백호대살": {
        "hanja": "白虎大殺", 
        "desc_common": "맹호의 물어뜯는 살기이자 압도적인 프로페셔널 에너지입니다. 이를 직업으로 승화시키면 해당 분야 최고 권위자에 오르나, 돌발 사고와 감정 폭발을 경계해야 합니다.",
        "desc_M": "【남성의 기운】 욱하는 기질이 강해 군인, 사법, 의료 등 기가 센 직업에서 맹장(猛將)으로 대성합니다. 단, 처(아내)의 자리(재성)에 백호가 임하면 아내가 크게 다치거나 아플 수 있습니다.",
        "desc_F": "【여성의 기운】 전형적인 여장부이자 집안의 가장입니다. 억센 환경을 전투적으로 헤쳐 나가 돈을 법니다. 남편 자리에 백호가 임하면 상부(喪夫)할 우려가 커 본인 스스로 칼을 쥐는 직업(의사, 미용, 요리)을 가져야 흉을 면합니다."
    },
    "괴강살": {
        "hanja": "魁罡殺", 
        "desc_common": "타인의 지배를 극도로 혐오하는 북두칠성의 우두머리, 즉 극강의 주체성과 카리스마입니다. 대부대귀하거나 한순간에 추락할 수 있는 양날의 검입니다.",
        "desc_M": "【남성의 기운】 굽힐 줄 모르는 강직함과 돌파력으로 거대 조직의 리더나 재벌이 될 수 있습니다. 다만 독선적인 성격으로 주변의 적을 많이 만들고 일찍 고립될 우려가 있습니다.",
        "desc_F": "【여성의 기운】 웬만한 남자는 쳐다보지도 않는 압도적인 스케일과 기백을 가졌습니다. 남편을 무시하거나 억누를 수 있으니, 남편과 권력을 다투기보다 본인이 직접 거대한 사업을 일궈야 합니다."
    },
    "양인살": {
        "hanja": "羊刃殺", 
        "desc_common": "불굴의 승부욕과 잔인하리만치 집요한 추진력을 뜻하는 칼날(刃)의 기운입니다. 전문직에서 대성하지만 성정이 강고하여 마찰과 부상을 조심해야 합니다.",
        "desc_M": "【남성의 기운】 아내를 극하는 가장 강력하고 무자비한 기운입니다. 양인이 강하면 아내가 아프거나 생리사별할 우려가 큽니다. 칼이나 펜을 쓰는 직업으로 흉기를 대체해야 합니다.",
        "desc_F": "【여성의 기운】 남편에게 절대 져주지 않으며 끝장을 보려는 기질이 강합니다. 부부싸움 시 서로에게 씻을 수 없는 비수를 꽂기 쉬우니 한 발 물러서는 지혜가 절실합니다."
    }
}

# 🌟 핵심 패치: 흉살의 남녀 차이를 완벽히 분리한 이원화 DB
DISASTERS_DB = {
    "충": {
        "hanja": "沖", 
        "desc_common": "두 기운이 정면으로 부딪혀 박살이 나는 파괴적 형국입니다. 낡은 것을 부수고 새로운 기회를 여는 개척의 발판이 되기도 합니다.",
        "desc_M": "【남성의 기운】 주로 사회적 위치(직장, 사업)의 급격한 변동으로 나타납니다. 강제 발령, 부도, 혹은 판을 뒤엎고 새 사업을 시작하는 폭발적인 이동수입니다.",
        "desc_F": "【여성의 기운】 직장 문제도 있지만 남성보다 '안방(가정)의 붕괴'에 훨씬 민감하게 반응합니다. 부부궁이 충을 맞으면 이혼이나 별거의 충격을 더 치명적으로 겪게 됩니다."
    },
    "원진": {
        "hanja": "怨嗔", 
        "desc_common": "서로를 까닭 없이 밀어내고 원망하는 극심한 애증과 얽힘의 살입니다.",
        "desc_M": "【남성의 기운】 주로 직장 내에서 이유 없이 상사나 부하직원과 사이가 틀어지고, 알 수 없는 억울한 오해를 뒤집어쓰는 등 사회적 스트레스로 작용하기 쉽습니다.",
        "desc_F": "【여성의 기운】 주로 고부갈등이나 남편과의 지독한 애증(만나면 싸우고 떨어지면 그립고 의심하는)으로 발현됩니다. 감정의 소모전망에 갇히기 쉬우니 철저한 거리두기가 필요합니다."
    },
    "귀문": {
        "hanja": "鬼門", 
        "desc_common": "영적이고 신경학적인 초감각 상태로, 비상한 통찰력과 천재적인 영감을 제공합니다.",
        "desc_M": "【남성의 기운】 꽂힌 일(연구, 종교, 기획)에 무서운 집중력을 보여 천재로 불리나, 임계점을 넘으면 편집증적 증세나 불면증으로 심신이 심하게 망가질 수 있습니다.",
        "desc_F": "【여성의 기운】 감수성이 극도로 예민해지고 촉(눈치)이 무섭게 빨라집니다. 우울증, 히스테리, 영적 불안감이 남성보다 크게 올 수 있으니 종교나 명상으로 마음의 짐을 비워야 합니다."
    },
    "천라지망": {
        "hanja": "天羅地網", 
        "desc_common": "하늘과 땅에 촘촘히 쳐진 피할 수 없는 옥망(그물)으로, 육체적/사회적 억압과 갇힘을 뜻합니다.",
        "desc_M": "【남성의 기운】 무리한 확장이나 투기를 하면 반드시 그물에 걸려 파산하거나 감옥에 가는 흉액이 따릅니다. 타인을 구제하고 가두는 활인업(군경, 사법, 의료)으로 대체해야 합니다.",
        "desc_F": "【여성의 기운】 자신만의 작은 세상에 갇혀 우울감이나 심리적 속박을 강하게 느낍니다. 타인을 돌보고 교육하는 봉사(종교, 교육, 보육)에 헌신해야 옥망을 뚫고 빛을 볼 수 있습니다."
    },
    "형": {
        "hanja": "刑", 
        "desc_common": "법적인 조정, 형벌, 살을 도려내는 수술의 기운입니다.",
        "desc_M": "【남성의 기운】 관재구설, 법적 소송, 폭력 사건에 휘말릴 위험이 큽니다. 법봉이나 메스를 직접 쥐는 전문 권력직(판검사, 외과, 기계)을 가지면 거대한 권위로 승화됩니다.",
        "desc_F": "【여성의 기운】 남편을 상징하는 글자에 형벌이 가해지면 남편과의 극단적인 소송(이혼)이나, 본인 스스로 몸에 칼을 대는 잦은 수술수(산부인과 등)로 발현될 위험이 큽니다."
    },
    "자형": {
        "hanja": "自刑", 
        "desc_common": "타인이 아닌 본인 스스로 마음의 감옥을 만들고 형벌을 가하는 자학적 흉살입니다.",
        "desc_M": "【남성의 기운】 강박적인 완벽주의 탓에 스스로를 혹사시키며, 사업 실패 시 자기 파괴적인 충동이나 비관(음주 등)에 쉽게 빠져듭니다.",
        "desc_F": "【여성의 기운】 내부적인 자기분열과 심한 우울증, 자책감을 야기합니다. '모든 게 내 탓'이라는 심리적 강박에서 스스로를 해방시키는 훈련이 시급합니다."
    },
    "파": {
        "hanja": "破", 
        "desc_common": "견고하던 내부 결속에 치명적인 균열과 파괴가 일어나는 기운입니다.",
        "desc_M": "【남성의 기운】 다 완성된 계약의 돌발적인 파기, 동업자의 배신 등 주로 일과 재물(사업)의 영역에서 막판에 엎어지는 변수로 작용합니다.",
        "desc_F": "【여성의 기운】 다 된 혼담이 깨지거나, 임신 중의 갑작스러운 유산, 혹은 끈끈하던 우정의 단절 등 관계와 자식의 영역에서 균열을 겪기 쉽습니다."
    },
    "해": {
        "hanja": "害", 
        "desc_common": "겉은 멀쩡하나 속으로 곪아들어 치명적인 상처를 남기는 이간질과 배신의 기운입니다.",
        "desc_M": "【남성의 기운】 직장이나 조직 내에서 믿었던 심복의 하극상, 혹은 뒤통수를 치는 은밀한 배신으로 인해 명예와 재물이 손상됩니다.",
        "desc_F": "【여성의 기운】 시댁이나 친정 식구들과의 끊임없는 마찰, 혹은 남편의 은밀한 배신(외도) 등 내밀한 가족 관계에서 가슴에 피멍이 드는 상처(천심육해)를 크게 입습니다."
    },
    "육합": {
        "hanja": "六合", 
        "desc_common": "음양이 자석처럼 밀착하는 가장 강력하고 은밀한 결속입니다. 흉한 것을 묶어두기도 하지만 좋은 것을 묶어버려 흉이 되기도 합니다.",
        "desc_M": "【남성의 기운】 비즈니스에서 배신이 없는 단단한 동맹이나 극비 프로젝트를 결성하는 좋은 작용을 하나, 잘못 얽히면 끊어내기 힘든 채무 관계나 은밀한 뇌물수수로 묶이게 됩니다.",
        "desc_F": "【여성의 기운】 남편과의 속궁합이 기가 막히게 맞아떨어지는 끈끈한 인연입니다. 단, 흉하게 작용하면 나를 절대 놓아주지 않는 스토커적인 집착이나 비밀스러운 연애사에 발목이 잡힙니다."
    }
}

class DynamicsEngine:
    def __init__(self):
        pass

    def _get_element(self, char: str) -> str:
        if not char: return None
        for elem, chars in ELEMENTS.items():
            if char in chars:
                return elem
        return None

    def scan_heoja(self, branches: list) -> dict:
        heoja_result = {"gonghyeop": [], "dochung": []}
        if not isinstance(branches, list): return heoja_result
            
        for i in range(len(branches) - 1):
            if branches[i] == branches[i+1] and branches[i] in EARTHLY_BRANCHES:
                idx = EARTHLY_BRANCHES.index(branches[i])
                dochung_char = EARTHLY_BRANCHES[(idx + 6) % 12]
                heoja_result["dochung"].append({"trigger": f"{branches[i]}{branches[i+1]}", "brought_char": dochung_char, "position": f"{i}열-{i+1}열 사이"})
                
        for i in range(len(branches) - 1):
            if branches[i] not in EARTHLY_BRANCHES or branches[i+1] not in EARTHLY_BRANCHES: continue
            idx1, idx2 = EARTHLY_BRANCHES.index(branches[i]), EARTHLY_BRANCHES.index(branches[i+1])
            diff = abs(idx1 - idx2)
            if diff == 2 or diff == 10:
                missing_idx = (min(idx1, idx2) + 1) % 12 if diff == 2 else (max(idx1, idx2) + 1) % 12
                gong_char = EARTHLY_BRANCHES[missing_idx]
                heoja_result["gonghyeop"].append({"trigger": f"{branches[i]}와 {branches[i+1]}", "brought_char": gong_char, "position": f"{i}열-{i+1}열 사이"})
        return heoja_result

    # 🌟 핵심 패치: gender 변수를 받아 성별에 맞는 통변을 반환하도록 수정
    def scan_special_stars(self, stems_dict: dict, branches_dict: dict, gender: str = "M") -> list:
        results = []
        if not isinstance(stems_dict, dict): stems_dict = {}
        if not isinstance(branches_dict, dict): branches_dict = {}
        
        day_stem, day_branch, year_branch = stems_dict.get("day", ""), branches_dict.get("day", ""), branches_dict.get("year", "")
        cheon_eul = {"甲":["丑","未"], "戊":["丑","未"], "庚":["丑","未"], "乙":["子","申"], "己":["子","申"], "丙":["亥","酉"], "丁":["亥","酉"], "辛":["午","寅"], "壬":["卯","巳"], "癸":["卯","巳"]}
        mun_chang = {"甲":"巳", "乙":"午", "丙":"申", "戊":"申", "丁":"酉", "己":"酉", "庚":"亥", "辛":"子", "壬":"寅", "癸":"卯"}
        yang_in = {"甲":"卯", "丙":"午", "戊":"午", "庚":"酉", "壬":"子"}
        baekho = ["甲辰", "乙未", "丙戌", "丁丑", "戊辰", "壬戌", "癸丑"]
        goegang = ["庚辰", "庚戌", "壬辰", "壬戌", "戊戌"]

        pillar_names, pillar_ganzhi_names = {"year": "연지", "month": "월지", "day": "일지", "hour": "시지"}, {"year": "연주", "month": "월주", "day": "일주", "hour": "시주"}
        temp_stars = {"천을귀인": [], "문창귀인": [], "도화살": [], "역마살": [], "화개살": [], "백호대살": [], "괴강살": [], "양인살": []}

        for p_key, branch in branches_dict.items():
            if branch == "-" or not branch: continue
            b_name, gz_name = pillar_names.get(p_key, ""), pillar_ganzhi_names.get(p_key, "")
            stem = str(stems_dict.get(p_key, "") or "")
            ganzhi = stem + str(branch)

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

        ref_stars_day, ref_stars_year = get_12_stars(day_branch), get_12_stars(year_branch)

        for p_key, branch in branches_dict.items():
            if branch == "-" or not branch: continue
            b_name = pillar_names.get(p_key, "")
            for star_name in ["도화", "역마", "화개"]:
                if branch in [ref_stars_day.get(star_name), ref_stars_year.get(star_name)]:
                    item = f"{b_name}({branch})"
                    if item not in temp_stars[f"{star_name}살"]: temp_stars[f"{star_name}살"].append(item)

        # 🌟 핵심 패치: 성별에 맞는 통변을 하나로 합쳐서(desc_common + desc_성별) 반환
        for star_type, positions in temp_stars.items():
            if positions:
                db_info = SPECIAL_STARS_DB.get(star_type, {"hanja": "", "desc_common": "", "desc_M": "", "desc_F": ""})
                gender_desc = db_info["desc_M"] if gender.upper() == 'M' else db_info["desc_F"]
                full_desc = f"【특징】 {db_info['desc_common']}\n{gender_desc}"
                
                results.append({
                    "name": star_type, 
                    "name_clean": star_type,
                    "hanja_clean": db_info["hanja"],
                    "position": ", ".join(positions),
                    "desc": full_desc
                })
        return results

    # 🌟 핵심 패치: gender 변수를 받아 성별에 맞는 통변을 반환하도록 수정
    def scan_disasters(self, branches: list, gender: str = "M") -> list:
        results = []
        temp_disasters = {key: [] for key in RELATIONS.keys()}
        
        if not isinstance(branches, list): return results
            
        for i in range(len(branches)):
            for j in range(i + 1, len(branches)):
                if branches[i] == "-" or branches[j] == "-" or not branches[i] or not branches[j]: continue
                pair = {branches[i], branches[j]}
                for rel_name, rel_list in RELATIONS.items():
                    if pair in rel_list:
                        if rel_name == "천라지망":
                            if pair == {"戌", "亥"}: temp_disasters[rel_name].append(f"{branches[i]}{branches[j]}(천라)")
                            elif pair == {"辰", "巳"}: temp_disasters[rel_name].append(f"{branches[i]}{branches[j]}(지망)")
                        else:
                            item = f"{branches[i]}{branches[j]}"
                            if item not in temp_disasters[rel_name]: temp_disasters[rel_name].append(item)
                                
        # 🌟 핵심 패치: 성별에 맞는 통변을 하나로 합쳐서 반환
        for d_type, positions in temp_disasters.items():
            if positions:
                db_info = DISASTERS_DB.get(d_type, {"hanja": "", "desc_common": "", "desc_M": "", "desc_F": ""})
                gender_desc = db_info["desc_M"] if gender.upper() == 'M' else db_info["desc_F"]
                full_desc = f"【특징】 {db_info['desc_common']}\n{gender_desc}"
                
                results.append({
                    "name": d_type,
                    "name_clean": d_type,
                    "hanja_clean": db_info["hanja"],
                    "position": ", ".join(positions),
                    "desc": full_desc
                })
        return results

    def check_gaedu_jeolgak(self, stem: str, branch: str) -> dict:
        stem, branch = str(stem).strip() if stem else "", str(branch).strip() if branch else ""
        stem_elem, branch_elem = self._get_element(stem), self._get_element(branch)
        result = {"status": "상생/비화(안정)", "desc": "상극이 없는 안정적인 기둥"}
        
        if not stem_elem or not branch_elem: return result
        if CLASH_MAP.get(stem_elem) == branch_elem: result = {"status": "개두(蓋頭)", "desc": f"천간({stem_elem})이 지지({branch_elem})를 극함. 하늘이 땅을 억누르는 형국."}
        elif CLASH_MAP.get(branch_elem) == stem_elem: result = {"status": "절각(截脚)", "desc": f"지지({branch_elem})가 천간({stem_elem})을 극함. 땅이 머리를 치는 형국으로 실속이 떨어짐."}
            
        return result