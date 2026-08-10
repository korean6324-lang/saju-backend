# db_dictionary.py
from typing import Dict, Any, List

class ExpertPrescriptionDB:
    def __init__(self):
        # 1. 특수 격국(外格) 및 일반 격국 DB
        self.gyeokguk_db = {
            "종살격": {"hanja": "從殺格", "desc": "나를 버리고 관살(권력/조직)의 기운에 순응하는 격. 강한 카리스마와 권력 지향."},
            "식신제살격": {"hanja": "食神制殺格", "desc": "식신의 기운으로 칠살의 흉폭함을 제압하는 격. 난제를 해결하는 전문가적 기질."}
            # 향후 일행득기격, 종아격 등 수십 여종의 전문가용 격국 확장
        }
        
        # 2. 흉액 직언(Disease) 및 업상대체(Prescription) DB
        self.prescription_db = {
            "백호대살": {
                "hanja": "白虎大殺",
                "disease": "혈광지사(血光之死)라 하여 과거에는 피를 보는 흉살로 보았음. 기운이 맹렬하여 감정 기복이 크고 돌발적인 사고 위험이 내재됨.",
                "prescription": "강한 압력을 다루는 직업(의료, 군경, 법조, IT 서버 관리 등)으로 업상대체(業象代替)하거나, 주기적인 헌혈을 통해 물리적 액땜(약·藥)을 권장함.",
                "blessing": "맹호의 기상을 긍정적으로 발현하면 특정 분야에서 타의 추종을 불허하는 압도적인 프로페셔널로 대성할 수 있습니다."
            },
            "원진살": {
                "hanja": "怨嗔殺",
                "disease": "이유 없는 미움과 원망이 교차하는 기운. 대인관계나 부부, 동업자 사이에 신경전과 감정의 소모전이 발생하기 쉬움.",
                "prescription": "사람을 직접 부대끼며 상대하기보다 사물, 데이터, 예술 작품에 몰두하는 직무로 승화하거나, 주말부부 등 물리적 거리를 두는 것이 개운의 열쇠가 됨.",
                "blessing": "타인이 보지 못하는 미세한 디테일을 짚어내는 탁월한 직관력과 예술적 감수성으로 빛을 발할 것입니다."
            },
            "천라지망": {
                "hanja": "天羅地網",
                "disease": "하늘과 땅에 그물이 쳐진 형국으로, 섣불리 움직이면 그물에 얽매여 관재구설(官災口舌)이나 답보 상태에 빠지기 쉬움.",
                "prescription": "자신을 낮추고 남을 살리는 활인업(의료, 교육, 심리상담, 명리학)이나 타인을 감금/구속하는 직업(교도관, 경찰)에 종사하여 흉을 길로 전환해야 함.",
                "blessing": "하늘이 내린 촘촘한 그물은, 사람을 돕고 살리는 일에 쓰일 때 세상을 품는 가장 거대한 캔버스가 됩니다."
            }
        }

    def diagnose_salsal(self, shinsal_list: List[str]) -> List[Dict[str, Any]]:
        """
        [핵심 알고리즘] 신살 및 흉액 진단기
        원국 및 대운에서 발견된 흉살에 대해 가감 없는 진단과 업상대체 처방을 JSON 배열로 반환
        """
        results = []
        for sal in shinsal_list:
            if sal in self.prescription_db:
                data = self.prescription_db[sal]
                results.append({
                    "term": sal,
                    "hanja": data["hanja"],
                    "disease_diagnosis": data["disease"],
                    "prescription_eopsang": data["prescription"],
                    "final_blessing": data["blessing"]
                })
        return results

    def identify_gyeokguk(self, element_scores: Dict[str, int]) -> Dict[str, str]:
        """
        [격국/용신 판별기]
        오행의 세력 분포(element_scores)와 월지 지장간 투간 여부를 기반으로 격국 도출.
        (현재는 MSA 파이프라인 연결을 위한 템플릿 반환)
        """
        # TODO: Phase 2의 통근 점수와 오행 분포를 융합한 복합 분기 로직 가동
        target_gyeokguk = "식신제살격" 
        
        return {
            "name": target_gyeokguk,
            "hanja": self.gyeokguk_db[target_gyeokguk]["hanja"],
            "description": self.gyeokguk_db[target_gyeokguk]["desc"]
        }

# 마이크로서비스 연동을 위한 인스턴스
db_dictionary_service = ExpertPrescriptionDB()

if __name__ == "__main__":
    db = ExpertPrescriptionDB()
    
    print("--- 흉액 직언 및 업상대체 처방 시뮬레이션 ---")
    # 원국 분석 모듈에서 도출된 신살 리스트 (Mock)
    detected_sals = ["백호대살", "원진살"]
    
    diagnoses = db.diagnose_salsal(detected_sals)
    for diag in diagnoses:
        print(f"[{diag['term']} ({diag['hanja']})]")
        print(f" ⚠️ 진단: {diag['disease_diagnosis']}")
        print(f" 💊 처방: {diag['prescription_eopsang']}")
        print(f" ✨ 축언: {diag['final_blessing']}\n")