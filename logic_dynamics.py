# logic_dynamics.py
from typing import Dict, List, Any

class DynamicsEngine:
    def __init__(self):
        self.branch_order = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        self.clashes = {"子": "午", "丑": "未", "寅": "申", "卯": "酉", "辰": "戌", "巳": "亥", "午": "子", "未": "丑", "申": "寅", "酉": "卯", "戌": "辰", "亥": "巳"}
        self.wonjin = {"子": "未", "未": "子", "丑": "午", "午": "丑", "寅": "酉", "酉": "寅", "卯": "申", "申": "卯", "辰": "亥", "亥": "辰", "巳": "戌", "戌": "巳"}
        
        # 특수 흉살 DB
        self.baekho_pillars = ["甲辰", "乙未", "丙戌", "丁丑", "戊辰", "壬戌", "癸丑"]
        
    def scan_heoja_gonghyeop(self, branches: List[str]) -> List[str]:
        heoja_list = []
        for i in range(len(branches) - 1):
            b1, b2 = branches[i], branches[i+1]
            if b1 not in self.branch_order or b2 not in self.branch_order: continue
            idx1, idx2 = self.branch_order.index(b1), self.branch_order.index(b2)
            distance = abs(idx1 - idx2)
            if distance == 2 or distance == 10:
                mid_idx = (idx1 + idx2) // 2 if distance == 2 else (idx1 + idx2 + 12) // 2 % 12
                heoja_list.append(self.branch_order[mid_idx])
        return list(set(heoja_list))

    def analyze_clash(self, branches: List[str]) -> List[Dict[str, str]]:
        clash_results = []
        for i in range(len(branches)):
            for j in range(i + 1, len(branches)):
                if self.clashes.get(branches[i]) == branches[j]:
                    clash_results.append({
                        "type": "충(沖)",
                        "target": f"{branches[i]}-{branches[j]}",
                        "meaning": f"{branches[i]}와 {branches[j]}가 상충하여 해당 궁(宮)의 기운이 흔들리고 변화가 잦음."
                    })
        return clash_results

    # 🚀 [핵심 추가] 흉살 정밀 스캐너
    def scan_special_shinsal(self, pillars: List[str]) -> List[str]:
        detected_sals = []
        branches = [p[1] for p in pillars]

        # 1. 백호대살 스캔 (해당 기둥이 백호 간지인지 확인)
        for p in pillars:
            if p in self.baekho_pillars and "백호대살" not in detected_sals:
                detected_sals.append("백호대살")

        # 2. 원진살 스캔 (인접한 지지끼리 원진 관계인지 확인)
        for i in range(len(branches) - 1):
            if self.wonjin.get(branches[i]) == branches[i+1]:
                if "원진살" not in detected_sals: detected_sals.append("원진살")

        # 3. 천라지망 스캔 (원국에 戌-亥 또는 辰-巳가 모두 있는지 확인)
        if "戌" in branches and "亥" in branches:
            if "천라지망" not in detected_sals: detected_sals.append("천라지망")
        if "辰" in branches and "巳" in branches:
            if "천라지망" not in detected_sals: detected_sals.append("천라지망")

        return detected_sals

logic_dynamics_service = DynamicsEngine()