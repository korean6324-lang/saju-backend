# logic_fengshui.py
from typing import Dict, Any

class FengShuiEngine:
    def __init__(self):
        # 1백수성 ~ 9자화성의 본명궁(本命宮) 괘상 매핑
        self.gua_mapping = {
            1: "감(坎)", 2: "곤(坤)", 3: "진(震)", 4: "손(巽)",
            6: "건(乾)", 7: "태(兌)", 8: "간(艮)", 9: "이(離)"
            # 5(중궁)는 남자는 2(곤), 여자는 8(간)로 치환됨
        }
        
        # 동사택 / 서사택 분류
        self.east_west_groups = {
            1: "동사택(東四宅)", 3: "동사택(東四宅)", 4: "동사택(東四宅)", 9: "동사택(東四宅)",
            2: "서사택(西四宅)", 6: "서사택(西四宅)", 7: "서사택(西四宅)", 8: "서사택(西四宅)"
        }
        
        # 8대 길흉성(八大吉凶星) 크로스매칭 DB (팔택명경 기준)
        # 딕셔너리 구조: {본명궁: {상대방_또는_방위의_본명궁: "길흉결과"}}
        self.eight_mansions_db = {
            1: {1:"복위(吉)", 2:"절명(凶)", 3:"천을(吉)", 4:"생기(吉)", 6:"육살(凶)", 7:"화해(凶)", 8:"오귀(凶)", 9:"연년(吉)"},
            2: {1:"절명(凶)", 2:"복위(吉)", 3:"화해(凶)", 4:"오귀(凶)", 6:"연년(吉)", 7:"천을(吉)", 8:"생기(吉)", 9:"육살(凶)"},
            3: {1:"천을(吉)", 2:"화해(凶)", 3:"복위(吉)", 4:"연년(吉)", 6:"오귀(凶)", 7:"절명(凶)", 8:"육살(凶)", 9:"생기(吉)"},
            4: {1:"생기(吉)", 2:"오귀(凶)", 3:"연년(吉)", 4:"복위(吉)", 6:"화해(凶)", 7:"육살(凶)", 8:"절명(凶)", 9:"천을(吉)"},
            6: {1:"육살(凶)", 2:"연년(吉)", 3:"오귀(凶)", 4:"화해(凶)", 6:"복위(吉)", 7:"생기(吉)", 8:"천을(吉)", 9:"절명(凶)"},
            7: {1:"화해(凶)", 2:"천을(吉)", 3:"절명(凶)", 4:"육살(凶)", 6:"생기(吉)", 7:"복위(吉)", 8:"연년(吉)", 9:"오귀(凶)"},
            8: {1:"오귀(凶)", 2:"생기(吉)", 3:"육살(凶)", 4:"절명(凶)", 6:"천을(吉)", 7:"연년(吉)", 8:"복위(吉)", 9:"화해(凶)"},
            9: {1:"연년(吉)", 2:"육살(凶)", 3:"생기(吉)", 4:"천을(吉)", 6:"절명(凶)", 7:"오귀(凶)", 8:"화해(凶)", 9:"복위(吉)"}
        }

    def calculate_bonmyeonggung(self, birth_year: int, gender: str) -> Dict[str, Any]:
        """
        [핵심 알고리즘] 삼원갑자 본명궁(本命宮) 도출
        입춘(立春)을 지난 출생년도를 기준으로 남녀의 본명궁 괘(Gua)를 계산합니다.
        """
        # 년도의 각 자릿수 합산 후 단일 숫자로 축소
        year_sum = sum(int(digit) for digit in str(birth_year))
        while year_sum > 9:
            year_sum = sum(int(digit) for digit in str(year_sum))
            
        # 남녀에 따른 본명궁 수학적 도출 공식
        if gender == "M":
            gua_num = 11 - year_sum
            if gua_num > 9: gua_num -= 9
            if gua_num == 5: gua_num = 2  # 남성 5황토성은 2(곤)으로 치환
        else: # "F"
            gua_num = 4 + year_sum
            if gua_num > 9: gua_num -= 9
            if gua_num == 5: gua_num = 8  # 여성 5황토성은 8(간)으로 치환
            
        gua_name = self.gua_mapping[gua_num]
        house_group = self.east_west_groups[gua_num]
        
        return {
            "gua_number": gua_num,
            "gua_name": gua_name,
            "house_group": house_group
        }

    def evaluate_match_and_direction(self, person_a_gua: int, target_gua: int) -> Dict[str, str]:
        """
        구궁(九宮) 크로스매칭을 통한 8대 길흉 궁합 및 방위 연산
        - 사람 간의 궁합 (예: 1백수성 남성과 4록목성 여성의 파트너십)
        - 특정 방위의 길흉 (예: 1백수성인 사람이 이사갈 집의 좌향이 2(곤)방향일 때)
        """
        result = self.eight_mansions_db.get(person_a_gua, {}).get(target_gua, "알 수 없음")
        
        meaning = ""
        if "생기" in result: meaning = "생기(生氣): 활력과 재물이 솟아나는 최고 길조. 비즈니스 파트너나 대문 방향으로 최적."
        elif "천을" in result: meaning = "천을(天乙): 귀인의 도움을 받아 질병이 치유되고 안정을 찾는 심신 평안의 길조."
        elif "절명" in result: meaning = "절명(絶命): 기운이 단절되어 파재와 질병이 우려되는 대흉. 수면 방향이나 계약 파트너로 피해야 함."
        # 추가적인 길흉 해석은 딕셔너리로 분리하여 메타데이터화 가능
        else: meaning = f"{result} 방위/궁합에 해당합니다."
        
        return {
            "result": result,
            "interpretation": meaning
        }

# 마이크로서비스 연동을 위한 인스턴스
logic_fengshui_service = FengShuiEngine()

if __name__ == "__main__":
    engine = FengShuiEngine()
    
    # 1. 본명궁 도출 테스트 (1985년생 남성)
    print("--- 본명궁 및 사택 연산 ---")
    p1 = engine.calculate_bonmyeonggung(1985, "M") 
    print(f"1985년생 남성: {p1}") 
    # 예상 결과: 6(건), 서사택
    
    # 2. 본명궁 도출 테스트 (1985년생 여성)
    p2 = engine.calculate_bonmyeonggung(1985, "F")
    print(f"1985년생 여성: {p2}") 
    # 예상 결과: 9(이), 동사택
    
    # 3. 8대 길흉 크로스매칭 테스트 (남성 6(건) vs 여성 9(이))
    print("\n--- 8대 길흉 궁합 분석 ---")
    match = engine.evaluate_match_and_direction(p1["gua_number"], p2["gua_number"])
    print(f"건(乾)과 이(離)의 만남: {match}")
    # 예상 결과: 절명(凶)