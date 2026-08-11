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

# 흉액 및 특수관계 정의 DB (합/형/파/해 완벽 확장)
RELATIONS = {
    "충(沖)": [{"子", "午"}, {"丑", "未"}, {"寅", "申"}, {"卯", "酉"}, {"辰", "戌"}, {"巳", "亥"}],
    "원진(怨嗔)": [{"子", "未"}, {"丑", "午"}, {"寅", "酉"}, {"卯", "申"}, {"辰", "亥"}, {"巳", "戌"}],
    "귀문(鬼門)": [{"子", "酉"}, {"丑", "午"}, {"寅", "未"}, {"卯", "申"}, {"辰", "亥"}, {"巳", "戌"}],
    "천라지망": [{"戌", "亥"}, {"辰", "巳"}],
    # [Phase 8 추가] 형, 파, 해, 합 스캔 데이터
    "형(刑)": [{"寅", "巳"}, {"巳", "申"}, {"寅", "申"}, {"丑", "戌"}, {"戌", "未"}, {"丑", "未"}, {"子", "卯"}],
    "자형(自刑)": [{"辰"}, {"午"}, {"酉"}, {"亥"}], # 자형은 같은 글자 2개 (Set 특성상 1개로 저장됨)
    "파(破)": [{"子", "酉"}, {"丑", "辰"}, {"寅", "亥"}, {"卯", "午"}, {"巳", "申"}, {"戌", "未"}],
    "해(害)": [{"子", "未"}, {"丑", "午"}, {"寅", "巳"}, {"卯", "辰"}, {"申", "亥"}, {"酉", "戌"}],
    "육합(六合)": [{"子", "丑"}, {"寅", "亥"}, {"卯", "戌"}, {"辰", "酉"}, {"巳", "申"}, {"午", "未"}]
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
        * branches: 연, 월, 일, 시 순서의 지지 리스트 (예: ["戌", "亥", "寅", "卯"])
        """
        heoja_result = {"gonghyeop": [], "dochung": []}
        
        # 1. 도충(倒沖) 스캔: 나란히 붙어있는 두 글자가 같을 때, 반대편(충) 글자를 끌어옴
        for i in range(len(branches) - 1):
            if branches[i] == branches[i+1]:
                idx = EARTHLY_BRANCHES.index(branches[i])
                dochung_char = EARTHLY_BRANCHES[(idx + 6) % 12]
                heoja_result["dochung"].append({
                    "trigger": f"{branches[i]}{branches[i+1]}",
                    "brought_char": dochung_char,
                    "position": f"{i}열-{i+1}열 사이"
                })
                
        # 2. 공협(拱挾) 스캔: 나란히 붙어있는 두 글자 사이에 정확히 한 글자만 빠져 있을 때
        for i in range(len(branches) - 1):
            idx1 = EARTHLY_BRANCHES.index(branches[i])
            idx2 = EARTHLY_BRANCHES.index(branches[i+1])
            
            # 두 글자의 인덱스 차이가 2 또는 10 (원형 큐 구조 고려)
            diff = abs(idx1 - idx2)
            if diff == 2 or diff == 10:
                # 빠진 글자 계산
                if diff == 2:
                    missing_idx = (min(idx1, idx2) + 1) % 12
                else: # diff == 10 인 경우 (예: 戌(10)과 子(0) 사이의 亥(11))
                    missing_idx = (max(idx1, idx2) + 1) % 12
                    
                gong_char = EARTHLY_BRANCHES[missing_idx]
                heoja_result["gonghyeop"].append({
                    "trigger": f"{branches[i]}와 {branches[i+1]}",
                    "brought_char": gong_char,
                    "position": f"{i}열-{i+1}열 사이"
                })
                
        return heoja_result

    def scan_disasters(self, branches: list) -> dict:
        """흉액/신살 및 합/형/파/해 교차 검증 스캐너"""
        disaster_result = {key: [] for key in RELATIONS.keys()}
        
        # 원국 내 모든 2개 조합(순서 상관없이 인접하지 않아도 스캔하되, 인접할수록 작용력이 큼)
        for i in range(len(branches)):
            for j in range(i + 1, len(branches)):
                pair = {branches[i], branches[j]}
                
                for rel_name, rel_list in RELATIONS.items():
                    if pair in rel_list:
                        # 천라지망 텍스트 디테일화
                        if rel_name == "천라지망":
                            if pair == {"戌", "亥"}:
                                disaster_result[rel_name].append(f"{branches[i]}{branches[j]}(천라)")
                            elif pair == {"辰", "巳"}:
                                disaster_result[rel_name].append(f"{branches[i]}{branches[j]}(지망)")
                        else:
                            # 합, 형, 파, 해, 충, 원진, 귀문, 자형 추가
                            item = f"{branches[i]}{branches[j]}"
                            if item not in disaster_result[rel_name]:
                                disaster_result[rel_name].append(item)
                        
        return disaster_result

    def check_gaedu_jeolgak(self, stem: str, branch: str) -> dict:
        """개두(蓋頭)와 절각(截脚) 판별기"""
        stem_elem = self._get_element(stem)
        branch_elem = self._get_element(branch)
        
        result = {"status": "상생/비화(안정)", "desc": "상극이 없는 안정적인 기둥"}
        
        if not stem_elem or not branch_elem:
            return result
            
        # 천간이 지지를 극하는가? (개두)
        if CLASH_MAP.get(stem_elem) == branch_elem:
            result = {"status": "개두(蓋頭)", "desc": f"천간({stem_elem})이 지지({branch_elem})를 극함. 하늘이 땅을 억누르는 형국."}
        # 지지가 천간을 극하는가? (절각)
        elif CLASH_MAP.get(branch_elem) == stem_elem:
            result = {"status": "절각(截脚)", "desc": f"지지({branch_elem})가 천간({stem_elem})을 극함. 땅이 머리를 치는 형국으로 실속이 떨어짐."}
            
        return result

    # ==========================================
    # [Phase 7 추가] 전문가용 심층 신살 스캐너
    # ==========================================
    def scan_special_stars(self, stems_dict: dict, branches_dict: dict) -> dict:
        """천을귀인, 문창, 도화, 역마, 화개, 백호, 괴강, 양인 도출"""
        stars = {
            "천을귀인": [], "문창귀인": [], "도화살": [], "역마살": [], "화개살": [],
            "백호대살": [], "괴강살": [], "양인살": []
        }
        
        day_stem = stems_dict.get("day", "")
        day_branch = branches_dict.get("day", "")
        year_branch = branches_dict.get("year", "")

        # 1. 일간 기준 길성 및 양인살 연산 테이블
        cheon_eul = {"甲":["丑","未"], "戊":["丑","未"], "庚":["丑","未"], "乙":["子","申"], "己":["子","申"], "丙":["亥","酉"], "丁":["亥","酉"], "辛":["午","寅"], "壬":["卯","巳"], "癸":["卯","巳"]}
        mun_chang = {"甲":"巳", "乙":"午", "丙":"申", "戊":"申", "丁":"酉", "己":"酉", "庚":"亥", "辛":"子", "壬":"寅", "癸":"卯"}
        yang_in = {"甲":"卯", "丙":"午", "戊":"午", "庚":"酉", "壬":"子"}

        # 2. 강력한 카리스마 간지(기둥 단위) 스캔
        baekho = ["甲辰", "乙未", "丙戌", "丁丑", "戊辰", "壬戌", "癸丑"]
        goegang = ["庚辰", "庚戌", "壬辰", "壬戌", "戊戌"]

        pillar_names = {"year": "연지", "month": "월지", "day": "일지", "hour": "시지"}
        pillar_ganzhi_names = {"year": "연주", "month": "월주", "day": "일주", "hour": "시주"}

        # 귀인 및 백호/괴강/양인 스캔 루프
        for pillar_key, branch in branches_dict.items():
            b_name = pillar_names.get(pillar_key, "")
            gz_name = pillar_ganzhi_names.get(pillar_key, "")
            stem = stems_dict.get(pillar_key, "")
            ganzhi = stem + branch

            if branch in cheon_eul.get(day_stem, []):
                stars["천을귀인"].append(f"{b_name}({branch})")
            if branch == mun_chang.get(day_stem):
                stars["문창귀인"].append(f"{b_name}({branch})")
            if branch == yang_in.get(day_stem):
                stars["양인살"].append(f"{b_name}({branch})")
                
            if ganzhi in baekho:
                stars["백호대살"].append(f"{gz_name}({ganzhi})")
            if ganzhi in goegang:
                stars["괴강살"].append(f"{gz_name}({ganzhi})")

        # 3. 삼합(三合) 기준 12신살 (도화, 역마, 화개) 연산 테이블
        def get_12_stars(ref_branch):
            if ref_branch in ["申", "子", "辰"]: return {"도화":"酉", "역마":"寅", "화개":"辰"}
            if ref_branch in ["寅", "午", "戌"]: return {"도화":"卯", "역마":"申", "화개":"戌"}
            if ref_branch in ["亥", "卯", "未"]: return {"도화":"子", "역마":"巳", "화개":"未"}
            if ref_branch in ["巳", "酉", "丑"]: return {"도화":"午", "역마":"亥", "화개":"丑"}
            return {}

        ref_stars_day = get_12_stars(day_branch)
        ref_stars_year = get_12_stars(year_branch)

        # 도화, 역마, 화개 스캔 (일지, 연지 교차 검증)
        for pillar_key, branch in branches_dict.items():
            b_name = pillar_names.get(pillar_key, "")
            
            for star_name in ["도화", "역마", "화개"]:
                # 연지 기준이거나 일지 기준에 해당하면 뱃지 부여
                if branch in [ref_stars_day.get(star_name), ref_stars_year.get(star_name)] and branch is not None:
                    item = f"{b_name}({branch})"
                    full_name = f"{star_name}살"
                    if item not in stars[full_name]:
                        stars[full_name].append(item)

        return stars