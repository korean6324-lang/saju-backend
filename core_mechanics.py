# core_mechanics.py
from typing import Dict, List, Any, Optional

def build_hanja_tooltip(term: str, hanja: str, pronunciation: str, meaning: str) -> Dict[str, str]:
    """프론트엔드 호환용 한문-한글 융합 메타데이터 JSON 제너레이터"""
    return {
        "term": term,
        "hanja": hanja,
        "pronunciation": pronunciation,
        "meaning": meaning
    }

class MechanicsEngine:
    def __init__(self):
        # 1. 지장간(地支藏干) DB
        self.jijanggan = {
            "子": ["壬", "癸", "癸"], "丑": ["癸", "辛", "己"], "寅": ["戊", "丙", "甲"], "卯": ["甲", "乙", "乙"],
            "辰": ["乙", "癸", "戊"], "巳": ["戊", "庚", "丙"], "午": ["丙", "己", "丁"], "未": ["丁", "乙", "己"],
            "申": ["戊", "壬", "庚"], "酉": ["庚", "辛", "辛"], "戌": ["辛", "丁", "戊"], "亥": ["戊", "甲", "壬"]
        }
        
        # 2. 음양오행(陰陽五行) 맵핑
        self.elements = {
            "甲": ("목", "+"), "乙": ("목", "-"), "丙": ("화", "+"), "丁": ("화", "-"), "戊": ("토", "+"),
            "己": ("토", "-"), "庚": ("금", "+"), "辛": ("금", "-"), "壬": ("수", "+"), "癸": ("수", "-"),
            "寅": ("목", "+"), "卯": ("목", "-"), "巳": ("화", "+"), "午": ("화", "-"),
            "辰": ("토", "+"), "戌": ("토", "+"), "丑": ("토", "-"), "未": ("토", "-"),
            "申": ("금", "+"), "酉": ("금", "-"), "亥": ("수", "+"), "子": ("수", "-")
        }
        
        # 3. 십성(육친) 도출 로직 (일간 오행 vs 대상 오행 상생상극)
        self.ten_deities_logic = {
            ("목", "목"): 0, ("목", "화"): 1, ("목", "토"): 2, ("목", "금"): 3, ("목", "수"): 4,
            ("화", "화"): 0, ("화", "토"): 1, ("화", "금"): 2, ("화", "수"): 3, ("화", "목"): 4,
            ("토", "토"): 0, ("토", "금"): 1, ("토", "수"): 2, ("토", "목"): 3, ("토", "화"): 4,
            ("금", "금"): 0, ("금", "수"): 1, ("금", "목"): 2, ("금", "화"): 3, ("금", "토"): 4,
            ("수", "수"): 0, ("수", "목"): 1, ("수", "화"): 2, ("수", "토"): 3, ("수", "금"): 4,
        }
        
        self.deity_names = {
            0: {"same": "비견", "diff": "겁재"},
            1: {"same": "식신", "diff": "상관"},
            2: {"same": "편재", "diff": "정재"},
            3: {"same": "편관", "diff": "정관"},
            4: {"same": "편인", "diff": "정인"}
        }

        # 4. 12운성(포태법) 메타데이터 배열
        self.twelve_stars = [
            ("장생", "長生", "새로운 시작과 탄생을 의미하는 길성. 후원과 순조로운 출발."),
            ("목욕", "沐浴", "호기심과 도화, 반복되는 시행착오와 불안정을 의미."),
            ("관대", "冠帶", "성장과 발전, 제복을 입는 직업군이나 강한 고집을 의미."),
            ("건록", "建祿", "자수성가와 안정, 강한 주체성과 실질적인 독립."),
            ("제왕", "帝旺", "최고조에 달한 에너지, 압도적인 리더십과 독단적인 성향."),
            ("쇠", "衰", "정점을 지나 노련해진 상태. 무리하지 않는 지혜."),
            ("병", "病", "기운이 쇠약해지나 동정심과 정신적/예술적 재능이 발달함."),
            ("사", "死", "육체적 정지, 고요함, 철학적 사유와 고도의 집중력."),
            ("묘", "墓", "저장과 수집, 알뜰함, 내면의 고립이나 화개(종교/예술)."),
            ("절", "絶", "완전한 단절 후 새로운 전환점. 변화무쌍하고 다소 불안정함."),
            ("태", "胎", "잉태, 새로운 아이디어와 계획, 매사에 조심스러운 성향."),
            ("양", "養", "양육과 평온, 상속이나 누군가를 기르고 가르치는 것에 유리함.")
        ]
        self.branches_order = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        # 양간 순행(1), 음간 역행(-1) 및 장생(시작점) 지지 맵핑
        self.star_start_point = {
            "甲": ("亥", 1), "丙": ("寅", 1), "戊": ("寅", 1), "庚": ("巳", 1), "壬": ("申", 1),
            "乙": ("午", -1), "丁": ("酉", -1), "己": ("酉", -1), "辛": ("子", -1), "癸": ("卯", -1)
        }

    def analyze_tonggeun(self, stems: List[str], branches: List[str]) -> List[Dict[str, Any]]:
        results = []
        for stem in stems:
            rooted_branches = []
            power_score = 0
            for branch in branches:
                hidden_stems = self.jijanggan.get(branch, [])
                if stem in hidden_stems:
                    rooted_branches.append(branch)
                    if hidden_stems[2] == stem:
                        power_score += 20
                    else:
                        power_score += 10
                        
            is_rooted = bool(rooted_branches)
            if is_rooted:
                meta_info = build_hanja_tooltip("통근", "通根", "통근", f"천간 {stem}이 지지 {', '.join(rooted_branches)}에 뿌리를 내려 기운이 실(實)함")
            else:
                meta_info = build_hanja_tooltip("허투", "虛透", "허투", f"천간 {stem}이 뿌리가 없어 허공에 뜬 상태")
                
            results.append({"stem": stem, "rooted_branches": rooted_branches, "is_tonggeun": is_rooted, "power_score": power_score, "meta": meta_info})
        return results

    def get_ten_deity(self, day_stem: str, target_char: str) -> str:
        """일간 기준 십성(육친) 산출"""
        if day_stem == target_char:
            return "일간"
        my_elem, my_yin_yang = self.elements[day_stem]
        target_elem, target_yin_yang = self.elements[target_char]
        
        relation_type = self.ten_deities_logic[(my_elem, target_elem)]
        yin_yang_match = "same" if my_yin_yang == target_yin_yang else "diff"
        return self.deity_names[relation_type][yin_yang_match]

    def calculate_12_stars(self, day_stem: str, branch: str) -> Dict[str, Any]:
        """양간 순행, 음간 역행 포태법(12운성) 산출"""
        start_branch, direction = self.star_start_point[day_stem]
        start_idx = self.branches_order.index(start_branch)
        target_idx = self.branches_order.index(branch)
        
        if direction == 1:
            steps = (target_idx - start_idx) % 12
        else:
            steps = (start_idx - target_idx) % 12
            
        star_data = self.twelve_stars[steps]
        return build_hanja_tooltip(term=star_data[0], hanja=star_data[1], pronunciation=star_data[0], meaning=star_data[2])

    def analyze_pillars_full(self, stems: List[str], branches: List[str]) -> Dict[str, Any]:
        """원국 4기둥 전체의 십성과 12운성을 분석하여 근묘화실의 뼈대를 제공"""
        day_stem = stems[2] # 사주의 기준이 되는 일간(나)
        
        return {
            "year": {
                "stem_deity": self.get_ten_deity(day_stem, stems[0]),
                "branch_deity": self.get_ten_deity(day_stem, branches[0]),
                "star_12": self.calculate_12_stars(day_stem, branches[0])
            },
            "month": {
                "stem_deity": self.get_ten_deity(day_stem, stems[1]),
                "branch_deity": self.get_ten_deity(day_stem, branches[1]),
                "star_12": self.calculate_12_stars(day_stem, branches[1])
            },
            "day": {
                "stem_deity": "일간",
                "branch_deity": self.get_ten_deity(day_stem, branches[2]),
                "star_12": self.calculate_12_stars(day_stem, branches[2])
            },
            "hour": {
                "stem_deity": self.get_ten_deity(day_stem, stems[3]),
                "branch_deity": self.get_ten_deity(day_stem, branches[3]),
                "star_12": self.calculate_12_stars(day_stem, branches[3])
            }
        }

core_mechanics_service = MechanicsEngine()