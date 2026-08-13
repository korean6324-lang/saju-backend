# logic_unse.py

class UnseEngine:
    def __init__(self):
        # 오행 정의
        self.stem_elem = {
            "甲": "목", "乙": "목", "丙": "화", "丁": "화", "戊": "토",
            "己": "토", "庚": "금", "辛": "금", "壬": "수", "癸": "수"
        }
        self.branch_elem = {
            "子": "수", "丑": "토", "寅": "목", "卯": "목", "辰": "토", "巳": "화",
            "午": "화", "未": "토", "申": "금", "酉": "금", "戌": "토", "亥": "수"
        }
        # 지지 충(沖) 관계
        self.chungs = {
            "子": "午", "午": "子", "丑": "未", "未": "丑", "寅": "申", "申": "寅",
            "卯": "酉", "酉": "卯", "辰": "戌", "戌": "辰", "巳": "亥", "亥": "巳"
        }
        # 지지 육합(六合) 관계
        self.habs = {
            "子": "丑", "丑": "子", "寅": "亥", "亥": "寅", "卯": "戌", "戌": "卯",
            "辰": "酉", "酉": "辰", "巳": "申", "申": "巳", "午": "未", "未": "午"
        }

    def _get_element(self, char: str) -> str:
        return self.stem_elem.get(char, self.branch_elem.get(char, ""))

    def _eval_luck_score(self, luck_branch: str, tg: str, yongshin_data: dict) -> int:
        """
        운의 지지(luck_branch) 오행과 십신(tg)을 용신/희신/기신과 대조하여 정밀 점수(-2 ~ +2) 계산
        """
        luck_elem = self._get_element(luck_branch)
        score = 0

        # 용신/희신/기신 텍스트 extraction
        y_text = ""
        h_text = ""
        g_text = ""

        if isinstance(yongshin_data, dict):
            y_info = yongshin_data.get("yongshin", {})
            if isinstance(y_info, dict):
                y_text = str(y_info.get("yongshin", ""))
                h_text = str(y_info.get("huishin", ""))
                g_text = str(y_info.get("gishin", ""))
            elif isinstance(y_info, str):
                y_text = y_info

        # 오행 적합도 체킹
        if luck_elem:
            if luck_elem in y_text:
                score += 2
            elif luck_elem in h_text:
                score += 1
            elif luck_elem in g_text:
                score -= 2

        # 십신 고유 성향 가산점
        if tg in ["식신", "정재", "정관", "정인"]:
            score += 1
        elif tg in ["편관", "상관", "겁재"]:
            score -= 1

        return score

    def _scan_interactions(self, formatted_bazi: dict, luck_branch: str) -> list:
        """ 🚨 [팩트폭행 적용] 원국 지지들과의 충(沖), 합(合) 반응을 적나라하게 스캔 """
        events = []

        for p_key, p_info in formatted_bazi.items():
            b_char = p_info["branch"]

            if self.chungs.get(luck_branch) == b_char:
                if p_key == "day":
                    events.append({"type": "bad", "title": f"⚡ 부부궁 파괴 ({luck_branch}{b_char}沖)", "desc": "배우자 자리가 정면으로 부딪혀 깨지는 흉상입니다. 이혼수, 별거, 금전적 손실, 하체 및 생식기 관련 질환 발현의 위험이 매우 높습니다."})
                elif p_key == "month":
                    events.append({"type": "bad", "title": f"⚡ 직업/사회궁 붕괴 ({luck_branch}{b_char}沖)", "desc": "직장이나 사업의 기반이 흔들립니다. 강제적인 퇴사, 부서 이동, 사업체 축소 및 부모형제와의 심각한 마찰이 발생할 수 있습니다."})
                elif p_key == "year":
                    events.append({"type": "bad", "title": f"⚡ 주거지/환경 변동 ({luck_branch}{b_char}沖)", "desc": "근본적인 삶의 환경이 충돌합니다. 예기치 못한 이사, 타의에 의한 발령(해외 등), 조상 및 가문과 연관된 관재구설에 주의하십시오."})
                elif p_key == "hour":
                    events.append({"type": "bad", "title": f"⚡ 말년/자식궁 타격 ({luck_branch}{b_char}沖)", "desc": "추진하던 프로젝트의 막판 엎어짐, 아랫사람(직원)의 배신, 자식과의 심한 불화나 건강 악화를 경계해야 합니다."})

            elif self.habs.get(luck_branch) == b_char:
                if p_key == "day":
                    events.append({"type": "good", "title": f"✨ 부부궁 은밀한 결속 ({luck_branch}{b_char}合)", "desc": "이성과의 강한 육체적/정서적 결속력이 발현됩니다. 미혼자는 강렬한 연애운이 터지나, 기혼자는 숨겨진 외도수를 경계해야 합니다."})
                elif p_key == "month":
                    events.append({"type": "good", "title": f"✨ 직업/사회궁 동맹 ({luck_branch}{b_char}合)", "desc": "사회에서 뜻이 맞는 강력한 조력자나 비즈니스 동맹을 맺습니다. 유리한 계약 성사 및 직장 내 입지가 굳건해집니다."})

        return events

    def analyze_sewun(self, formatted_bazi: dict, branch: str, tg: str, yongshin_data: dict) -> dict:
        """ 🚨 [팩트폭행 적용] [1년 단위 - 세운] 거시적 인생의 큰 줄기와 대변동 예측 """
        score = self._eval_luck_score(branch, tg, yongshin_data)
        events = self._scan_interactions(formatted_bazi, branch)

        if score >= 2:
            status = "🔥 대도약과 폭발적 득재(得財)"
            desc = f"수호신(용신)의 기운과 [{tg}]의 에너지가 결합하는 최고의 길기(吉期)입니다. 뚜렷한 재물 축적, 확고한 지위 상승(승진/합격), 귀인의 전폭적인 개입이 발생하므로 공격적인 확장과 베팅이 필요합니다."
        elif score == 1:
            status = "✨ 뚜렷한 성과와 발전"
            desc = f"길운이 작용하여 노력한 만큼의 확실한 보상이 따릅니다. [{tg}]의 긍정적 특성이 발현되어 업무적 성취가 발생하니, 세워둔 계획을 망설임 없이 실행에 옮기십시오."
        elif score == 0:
            status = "⚖️ 길흉 상쇄와 교착기"
            desc = f"폭발적인 상승도, 치명적인 하락도 없는 보합세입니다. 현상 유지에 주력하며, 다가올 대운을 위해 자본과 기술을 비축해야 하는 현실적인 인내의 구간입니다."
        else:
            status = "⚠️ 파재(破財)와 관재구설 경계"
            desc = f"사주의 기신(악귀)과 [{tg}]의 부정적 흉폭함이 극대화되는 대흉기입니다. 현금 흐름의 경색(파산), 소송, 건강 악화, 인간관계의 단절이 발생할 확률이 매우 높으니 철저히 엎드려 방어해야 합니다."

        return {"overall_status": status, "overall_desc": desc, "events": events}

    def analyze_wolgeon(self, formatted_bazi: dict, branch: str, tg: str, yongshin_data: dict) -> dict:
        """ 🚨 [팩트폭행 적용] [1달 단위 - 월건] 한 달간의 단기 업무, 대인관계, 컨디션 흐름 예측 """
        score = self._eval_luck_score(branch, tg, yongshin_data)

        if score >= 2:
            status = "🚀 단기적 자금 유입과 쾌거"
            desc = f"[{tg}] 및 용희신의 작용으로 막혔던 자금줄이 풀리고 유의미한 계약이나 실적이 꽂히는 팩트 기반의 상승 달입니다."
        elif score == 1:
            status = "🌿 순행과 실속의 달"
            desc = f"업무와 대인관계에서 [{tg}]의 길조가 뚜렷합니다. 불필요한 마찰이 줄어들고 뿌린 만큼의 금전적, 심리적 이득을 챙깁니다."
        elif score == 0:
            status = "☕ 변동성 없는 보합 유지"
            desc = f"유의미한 이득도 손실도 발생하지 않는 달입니다. 무리한 이직, 투자, 거주지 변동을 지양하고 현재의 시스템을 방어하십시오."
        else:
            status = "🌧️ 자금 경색 및 마찰 노출"
            desc = f"[{tg}]의 흉작용으로 직장 내 극심한 스트레스, 단기적 자금 묶임, 예기치 않은 건강 손실이 수면 위로 드러나는 흉월(凶月)입니다."

        return {"overall_status": status, "overall_desc": desc, "events": []}

    def analyze_iljin(self, formatted_bazi: dict, branch: str, tg: str, yongshin_data: dict) -> dict:
        """ 🚨 [팩트폭행 적용] [하루 단위 - 일진] 오늘 하루의 컨디션, 약속, 소소한 기운 예측 """
        score = self._eval_luck_score(branch, tg, yongshin_data)

        if score >= 2:
            status = "☀️ 승부수를 던져야 할 호재일"
            desc = f"[{tg}] 길운이 터지는 날입니다. 중요한 계약, 이직 면접, 거액의 결제 등 무게감 있는 결단을 내리기에 완벽한 타이밍입니다."
        elif score == 1:
            status = "🌸 일정의 원만한 진행"
            desc = f"[{tg}]의 조력으로 계획된 스케줄이 오차 없이 진행되며, 비즈니스 및 대인관계에서 소소한 이득이 발생합니다."
        elif score == 0:
            status = "🍃 특이사항 없는 평일"
            desc = f"길흉의 충돌이 없는 조용한 일진입니다. 새로운 일을 벌이기보다는 밀린 업무를 정리하는 데 적합합니다."
        else:
            status = "☔ 돌발적 손실과 충돌 경계"
            desc = f"[{tg}]의 흉운이 발동합니다. 사소한 말실수가 법적 다툼으로 번지거나 예상치 못한 자산 손실이 발생할 수 있으니 외부 약속을 철회하십시오."

        return {"overall_status": status, "overall_desc": desc, "events": []}