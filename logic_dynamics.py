# logic_dynamics.py
from typing import Dict, List, Any

class DynamicsEngine:
    def __init__(self):
        # 12지지 순서 (공협 스캐닝 기준 배열)
        self.branch_order = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        # 지지 6충(六沖) DB
        self.clashes = {
            "子": "午", "丑": "未", "寅": "申", "卯": "酉", "辰": "戌", "巳": "亥",
            "午": "子", "未": "丑", "申": "寅", "酉": "卯", "戌": "辰", "亥": "巳"
        }
        
        # 오행(五行) 맵핑 (개두/절각 분석용)
        self.elements = {
            "甲": "목", "乙": "목", "寅": "목", "卯": "목",
            "丙": "화", "丁": "화", "巳": "화", "午": "화",
            "戊": "토", "己": "토", "辰": "토", "戌": "토", "丑": "토", "未": "토",
            "庚": "금", "辛": "금", "申": "금", "酉": "금",
            "壬": "수", "癸": "수", "亥": "수", "子": "수"
        }
        
        # 오행 상극(相剋) 관계표
        self.overcomes = {"목": "토", "토": "수", "수": "화", "화": "금", "금": "목"}

    def scan_heoja_gonghyeop(self, branches: List[str]) -> List[str]:
        """
        [허자론] 공협(拱挾) 스캐너
        원국에 없는 글자를 끌어오는 보이지 않는 기운을 도출합니다.
        예: 지지에 '子(자)'와 '寅(인)'이 나란히 있으면 그 사이의 '丑(축)'을 허자로 끌어옴.
        """
        heoja_list = []
        # 인접한 지지들을 스캔
        for i in range(len(branches) - 1):
            b1, b2 = branches[i], branches[i+1]
            if b1 not in self.branch_order or b2 not in self.branch_order:
                continue
                
            idx1, idx2 = self.branch_order.index(b1), self.branch_order.index(b2)
            
            # 두 글자가 딱 한 칸 떨어져 있을 때 (순행/역행 거리 계산)
            distance = abs(idx1 - idx2)
            if distance == 2 or distance == 10:
                # 중간에 끼인 글자 인덱스 도출
                if distance == 2:
                    mid_idx = (idx1 + idx2) // 2
                else:
                    mid_idx = (idx1 + idx2 + 12) // 2 % 12
                heoja_list.append(self.branch_order[mid_idx])
                
        return list(set(heoja_list))

    def analyze_clash(self, branches: List[str]) -> List[Dict[str, str]]:
        """합충형해파(合沖刑害破) 중 충(沖)을 정밀 분석하여 길흉의 변동성 색출"""
        clash_results = []
        for i in range(len(branches)):
            for j in range(i + 1, len(branches)):
                if self.clashes.get(branches[i]) == branches[j]:
                    clash_results.append({
                        "type": "충(沖)",
                        "target": f"{branches[i]}-{branches[j]}",
                        "meaning": f"{branches[i]}와 {branches[j]}가 상충하여 해당 궁(宮)의 기운이 흔들리고 극적인 변화가 잦음."
                    })
        return clash_results

    def analyze_gaedu_jeolgak(self, stem: str, branch: str) -> Dict[str, Any]:
        """
        개두(蓋頭)와 절각(截脚) 분석 알고리즘
        대운이나 세운 기둥의 상하 상극 관계를 분석하여 운의 '실질적 파워'를 판별합니다.
        """
        stem_element = self.elements.get(stem)
        branch_element = self.elements.get(branch)
        
        result = {
            "pillar": f"{stem}{branch}", 
            "stem_element": stem_element, 
            "branch_element": branch_element, 
            "status": "상생(相生) 또는 비화(比和)"
        }
        
        # 천간이 지지를 극하는 경우 (개두)
        if self.overcomes.get(stem_element) == branch_element:
            result["status"] = "개두(蓋頭)"
            result["description"] = "머리가 덮였다는 뜻으로, 천간이 지지를 극함. 겉은 화려하고 그럴싸하나 속빈 강정처럼 실속이 약해질 수 있음."
            result["power_modifier"] = 0.6  # 운의 힘이 60%로 감소
            
        # 지지가 천간을 극하는 경우 (절각)
        elif self.overcomes.get(branch_element) == stem_element:
            result["status"] = "절각(截脚)"
            result["description"] = "다리가 부러졌다는 뜻으로, 지지가 천간을 극함. 뜻은 높으나 현실의 장벽에 부딪혀 중도 좌절이나 지연이 발생하기 쉬움."
            result["power_modifier"] = 0.4  # 운의 힘이 40%로 감소
            
        else:
             result["power_modifier"] = 1.0 # 상생하면 100% 발현
             
        return result

# 마이크로서비스 연동을 위한 인스턴스
logic_dynamics_service = DynamicsEngine()

if __name__ == "__main__":
    engine = DynamicsEngine()
    
    # 1. 허자(공협) 테스트
    test_branches = ["子", "寅", "辰", "申"]
    print("--- 공협(拱挾) 스캔 ---")
    print(f"원국 지지 {test_branches}에서 도출된 허자: {engine.scan_heoja_gonghyeop(test_branches)}") 
    # 예상 결과: '丑' (子와 寅 사이), '卯' (寅과 辰 사이)
    
    # 2. 개두/절각 테스트 (갑신 대운)
    print("\n--- 개두/절각 분석 ---")
    daewun = engine.analyze_gaedu_jeolgak("甲", "申") # 갑목(목)과 신금(금)
    print(daewun)
    # 예상 결과: 절각 (금이 목을 극함)