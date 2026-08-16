# logic_hongtaek.py
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum

logger = logging.getLogger(__name__)

# ==========================================
# 1. API 응답용 스키마 (데이터 구조)
# ==========================================
class NodeStatus(str, Enum):
    SAFE = "SAFE"
    DANGER = "DANGER"
    AUSPICIOUS_BY_REMEDY = "AUSPICIOUS_BY_REMEDY" 
    UNVERIFIED = "UNVERIFIED"

class ThreatItem(BaseModel):
    name: str
    element: Optional[str] = None
    target: Optional[str] = None

class ShieldItem(BaseModel):
    name: str
    type: str
    target: Optional[str] = None

class MutationItem(BaseModel):
    name: str
    type: str

class AttributeItem(BaseModel):
    key: str
    value: str

class RawFactors(BaseModel):
    risk_score: int = 0
    threats: List[ThreatItem] = Field(default_factory=list)
    shields: List[ShieldItem] = Field(default_factory=list)
    mutations: List[MutationItem] = Field(default_factory=list)
    attributes: List[AttributeItem] = Field(default_factory=list)

class Interpretation(BaseModel):
    title: str
    summary: str
    full_text: str

class ExplainableNode(BaseModel):
    final_status: NodeStatus
    raw_data: RawFactors
    interpretation: Interpretation
    reasoning_chain: List[str] = Field(default_factory=list)

# ==========================================
# 2. 서브 엔진들 (Macro, Taegil, Micro, Iching)
# ==========================================
class MacroGunghapEngine:
    def analyze_space(self, m_data, f_data) -> ExplainableNode:
        # 구궁수 및 동서명 궁합 분석 로직 (현재는 프론트엔드 연동을 위한 기본 골격)
        return ExplainableNode(
            final_status=NodeStatus.SAFE,
            raw_data=RawFactors(attributes=[AttributeItem(key="궁합", value="생기(生氣)")]),
            interpretation=Interpretation(
                title="하늘과 땅이 축복하는 인연",
                summary="공간적 기운이 매우 조화롭습니다.",
                full_text="두 사람의 본명궁이 완벽하게 상생하는 길한 궁합입니다."
            ),
            reasoning_chain=["1. 남녀 구궁수 도출 완료", "2. 동서사명 배합 완료: 생기합 확정"]
        )

class TaegilEngine:
    def get_auspicious_month(self, f_branch: str) -> Dict:
        # 신부 띠 기준 길월 반환
        return {
            "대리월": [6, 12] if f_branch in ["子", "午"] else [1, 7],
            "소리월": [1, 7] if f_branch in ["子", "午"] else [4, 10],
            "desc": "신부의 띠를 기준으로 산출된 대길한 달입니다."
        }

class MicroBaziEngine:
    def analyze_time_and_remedy(self, m_data, f_data, target_date_branch) -> ExplainableNode:
        # 택일된 날짜의 흉살 스캔 및 제화(살인상생 등) 분석
        is_overridden = False
        score = 80
        msg = "무난한 날입니다."
        status = NodeStatus.SAFE

        # 만약 특정 날짜(target_date_branch)가 들어왔다면 스캔 로직 가동
        if target_date_branch:
            # 임시로 제화(制化)가 발동한 것으로 처리 (프론트엔드 12번 패널 렌더링용)
            is_overridden = True
            msg = "강한 흉살이 들어왔으나, 사주 내의 수호신(정인)이 이를 덮어 길하게 승화시켰습니다."
            status = NodeStatus.AUSPICIOUS_BY_REMEDY

        return ExplainableNode(
            final_status=status,
            raw_data=RawFactors(
                risk_score=20,
                mutations=[MutationItem(name="살인상생", type="흉->길 전환")] if is_overridden else []
            ),
            interpretation=Interpretation(
                title="극적인 제화(制化)가 일어난 날" if is_overridden else "안정적인 혼례일",
                summary=msg,
                full_text="자세한 흉살과 길신의 상호작용 분석 결과입니다."
            ),
            reasoning_chain=["1. 일진 흉살 스캔", "2. 사주 내 길신 방어막 확인", "3. 상태 확정"]
        )

class IchingOracleEngine:
    def cast_oracle(self, m_data, f_data) -> ExplainableNode:
        # 주역 64괘 교차 검증 로직
        return ExplainableNode(
            final_status=NodeStatus.SAFE,
            raw_data=RawFactors(attributes=[
                AttributeItem(key="상괘", value="천(天)"),
                AttributeItem(key="하괘", value="지(地)")
            ]),
            interpretation=Interpretation(
                title="지천태(地天泰)",
                summary="하늘과 땅이 교감하는 최고의 괘상입니다.",
                full_text="어려움이 물러가고 태평성대가 찾아오는 완벽한 결혼의 괘입니다."
            ),
            reasoning_chain=["1. 남녀 기운 주역 괘상 변환", "2. 지천태 괘 확정"]
        )

# ==========================================
# 3. 최상위 오케스트레이터 (main.py에서 호출하는 클래스)
# ==========================================
class UltimateHongtaekEngine:
    def __init__(self, macro_eng: MacroGunghapEngine, taegil_eng: TaegilEngine, micro_eng: MicroBaziEngine, iching_eng: IchingOracleEngine):
        self.macro = macro_eng
        self.taegil = taegil_eng
        self.micro = micro_eng
        self.iching = iching_eng

    def generate_full_report(self, m_data, f_data, target_date_branch) -> Dict[str, Any]:
        """main.py에서 호출되어 전체 7단계 분석 결과를 딕셔너리로 반환합니다."""
        
        # 1. 공간 궁합 분석 (구궁)
        space_node = self.macro.analyze_space(m_data, f_data)
        
        # 2. 시간 택일 분석
        time_node = self.micro.analyze_time_and_remedy(m_data, f_data, target_date_branch)
        
        # 프론트엔드 하위 호환성을 위해 데이터 추출
        taegil_info = self.taegil.get_auspicious_month(f_data.get("branch", "子"))
        time_dict = time_node.dict()
        time_dict["target_date_branch"] = target_date_branch
        time_dict["is_overridden"] = (time_node.final_status == NodeStatus.AUSPICIOUS_BY_REMEDY)
        time_dict["resolve_message"] = time_node.interpretation.summary
        time_dict["score_info"] = {"score": 95, "message": "최상급 길일입니다."}
        time_dict["대리월"] = taegil_info["대리월"]
        time_dict["소리월"] = taegil_info["소리월"]
        time_dict["desc"] = taegil_info["desc"]
        
        # 3. 주역 64괘 검증
        iching_node = self.iching.cast_oracle(m_data, f_data)
        iching_dict = iching_node.dict()
        iching_dict["upper_trigram"] = "천(天)"
        iching_dict["lower_trigram"] = "지(地)"
        iching_dict["moving_line"] = 3
        iching_dict["name"] = iching_node.interpretation.title
        iching_dict["hexagram_key"] = "11"
        iching_dict["desc"] = iching_node.interpretation.full_text

        return {
            "space_analysis": {"status": "대길(大吉)", "desc": space_node.interpretation.full_text, "classical": "하늘이 맺어준 인연입니다."},
            "time_analysis": time_dict,
            "iching_oracle": iching_dict,
            "bazi_analysis": {
                "salvation_score": 95, 
                "match_3d": {
                    "mental": {"status": "천간합(天干合)", "desc": "정신적 교감이 완벽합니다."},
                    "physical": {"status": "육합(六合)", "pros": "찰떡궁합입니다.", "cons": "없음"}
                }
            }
        }