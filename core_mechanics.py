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
        # 1. 지장간(地支藏干) DB: [초기, 중기, 정기] 
        # 지지 속에 숨겨진 천간의 기운을 분할 매핑
        self.jijanggan = {
            "子": ["壬", "癸", "癸"],
            "丑": ["癸", "辛", "己"],
            "寅": ["戊", "丙", "甲"],
            "卯": ["甲", "乙", "乙"],
            "辰": ["乙", "癸", "戊"],
            "巳": ["戊", "庚", "丙"],
            "午": ["丙", "己", "丁"],
            "未": ["丁", "乙", "己"],
            "申": ["戊", "壬", "庚"],
            "酉": ["庚", "辛", "辛"],
            "戌": ["辛", "丁", "戊"],
            "亥": ["戊", "甲", "壬"]
        }

    def analyze_tonggeun(self, stems: List[str], branches: List[str]) -> List[Dict[str, Any]]:
        """
        [핵심 알고리즘] 투간(透干)과 통근(通根) 정밀 분석
        천간의 글자가 원국 지지의 지장간에 뿌리를 내렸는지 교집합 스캔 및 수치화
        """
        results = []
        for stem in stems:
            rooted_branches = []
            power_score = 0
            
            for branch in branches:
                hidden_stems = self.jijanggan.get(branch, [])
                if stem in hidden_stems:
                    rooted_branches.append(branch)
                    # 정기(Main qi)에 통근시 더 높은 가중치 부여 등 세밀한 수치화 로직
                    if hidden_stems[2] == stem:
                        power_score += 20
                    else:
                        power_score += 10
                        
            is_rooted = bool(rooted_branches)
            
            # 상태에 따른 맞춤형 툴팁 생성
            if is_rooted:
                meaning = f"천간 {stem}이 지지 {', '.join(rooted_branches)}에 뿌리를 내려 기운이 실(實)함"
                meta_info = build_hanja_tooltip("통근", "通根", "통근", meaning)
            else:
                meaning = f"천간 {stem}이 뿌리가 없어 허공에 뜬 상태 (허투)"
                meta_info = build_hanja_tooltip("허투", "虛透", "허투", meaning)
                
            results.append({
                "stem": stem,
                "rooted_branches": rooted_branches,
                "is_tonggeun": is_rooted,
                "power_score": power_score,
                "meta": meta_info
            })
            
        return results

    def calculate_12_stars(self, day_stem: str, branch: str) -> Dict[str, Any]:
        """
        12운성(十二運星) 산출 알고리즘
        양간 순행 / 음간 역행 포태법(胞胎法) 적용
        """
        # TODO: 양간/음간에 따른 12운성 인덱스 순환 계산식 구현
        # (임시 목업 반환값)
        star_name = "제왕"
        
        return build_hanja_tooltip(
            term=star_name,
            hanja="帝旺",
            pronunciation="제왕",
            meaning="만물이 정점에 달하여 가장 강력한 기운을 뿜어내는 시기. 프로페셔널과 독립성의 상징."
        )

# 마이크로서비스 연동을 위한 인스턴스
core_mechanics_service = MechanicsEngine()

if __name__ == "__main__":
    # 테스트 구동: 천간 [甲, 丙]과 지지 [寅, 子, 辰, 申]의 통근 여부
    test_stems = ["甲", "丙"]
    test_branches = ["寅", "子", "辰", "申"]
    
    print("--- 통근(通根) 분석 결과 ---")
    tonggeun_result = core_mechanics_service.analyze_tonggeun(test_stems, test_branches)
    for res in tonggeun_result:
        print(f"Stem: {res['stem']} -> Score: {res['power_score']}, Meta: {res['meta']}")