# logic_timeline.py
from typing import Dict, List, Any
from datetime import datetime

class TimelineEngine:
    def __init__(self):
        # 천간과 지지 기본 배열
        self.stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        self.branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        # 음양(Yin/Yang) 매핑 (천간 기준)
        self.stem_yin_yang = {
            "甲": "양", "乙": "음", "丙": "양", "丁": "음", "戊": "양", 
            "己": "음", "庚": "양", "辛": "음", "壬": "양", "癸": "음"
        }

    def _get_next_pillar(self, current_stem: str, current_branch: str, direction: int) -> str:
        """60갑자를 순행(+1) 또는 역행(-1)하여 다음/이전 기둥을 반환합니다."""
        stem_idx = self.stems.index(current_stem)
        branch_idx = self.branches.index(current_branch)
        
        # 10진법(천간)과 12진법(지지)의 순환
        next_stem_idx = (stem_idx + direction) % 10
        next_branch_idx = (branch_idx + direction) % 12
        
        return f"{self.stems[next_stem_idx]}{self.branches[next_branch_idx]}"

    def calculate_daewun(self, year_stem: str, month_pillar: str, gender: str, daewun_number: int) -> List[Dict[str, Any]]:
        """
        [핵심 알고리즘] 대운(大運) 타임라인 배열 도출
        - 양남음녀(陽男陰女)는 순행, 음남양녀(陰男陽女)는 역행의 법칙 적용.
        - Phase 1에서 도출된 '초정밀 보정 월주(Month Pillar)'를 시작점으로 기둥을 세웁니다.
        """
        year_yin_yang = self.stem_yin_yang.get(year_stem, "양")
        
        # 대운 전개 방향 (순행/역행 판별)
        if (year_yin_yang == "양" and gender == "M") or (year_yin_yang == "음" and gender == "F"):
            direction = 1  # 순행
        else:
            direction = -1 # 역행

        month_stem, month_branch = month_pillar[0], month_pillar[1]
        daewun_list = []
        
        current_stem, current_branch = month_stem, month_branch
        
        # 1대운부터 8대운까지 (총 80년) 생애주기 배열 생성
        for i in range(8):
            next_pillar = self._get_next_pillar(current_stem, current_branch, direction)
            current_stem, current_branch = next_pillar[0], next_pillar[1]
            
            start_age = daewun_number + (i * 10)
            end_age = start_age + 9
            
            daewun_list.append({
                "daewun_idx": i + 1,
                "age_range": f"{start_age}~{end_age}세",
                "pillar": next_pillar,
                "direction": "순행" if direction == 1 else "역행"
            })
            
        return daewun_list

    def generate_sewun(self, base_year: int, start_year: int, count: int = 10) -> List[Dict[str, Any]]:
        """
        세운(歲運 - 1년 단위 운) 동적 도출
        특정 시작 연도(start_year)부터 지정된 N년간의 60갑자를 매핑하여 반환합니다.
        """
        # 1984년(甲子년)을 기준으로 60갑자 매핑 인덱스 도출
        offset = (start_year - 1984) % 60
        
        sewun_list = []
        for i in range(count):
            current_offset = (offset + i) % 60
            stem_idx = current_offset % 10
            branch_idx = current_offset % 12
            pillar = f"{self.stems[stem_idx]}{self.branches[branch_idx]}"
            
            sewun_list.append({
                "year": start_year + i,
                "age": (start_year + i) - base_year + 1, # 한국식 나이 (태어난 해 = 1세)
                "pillar": pillar
            })
            
        return sewun_list

# 마이크로서비스 연동용 인스턴스
logic_timeline_service = TimelineEngine()

if __name__ == "__main__":
    engine = TimelineEngine()
    
    # [테스트 시뮬레이션]
    # Phase 1에서 진기(進氣) 보정을 통해 '기해(己亥)'가 아닌 '경자(庚子)'로 
    # 완벽하게 도출된 월주를 바탕으로 대운을 세워보는 테스트
    print("--- 대운(大運) 생성 엔진 테스트 ---")
    daewun = engine.calculate_daewun(year_stem="丙", month_pillar="庚子", gender="M", daewun_number=3)
    
    for dw in daewun:
        print(f"[{dw['daewun_idx']}대운] 나이: {dw['age_range']} | 기둥: {dw['pillar']} ({dw['direction']})")
    
    # 출력 결과: 경자(庚子)를 기점으로 신축(辛丑), 임인(壬寅)... 순행 전개 확인