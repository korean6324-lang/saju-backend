class UltimateGunghapEngine:
    def __init__(self):
        # 🚨 [작업 1] 본명성 도출을 위한 별자리 기초 DB 복구
        self.stars = {
            1: "일백수성(一白水星)", 2: "이흑토성(二黑土星)", 3: "삼벽목성(三碧木星)",
            4: "사록목성(四綠木星)", 5: "오황토성(五黃土星)", 6: "육백금성(六白金星)",
            7: "칠적금성(七赤金星)", 8: "팔백토성(八白土星)", 9: "구자화성(九紫火星)"
        }

        # ==========================================
        # [데이터 통합 완료] 64구궁팔괘 매트릭스 DB (원본 100% 보존)
        # ==========================================
        self.gugung_matrix = {
            "1_1": {"status": "복위(伏位)", "classical": "輔弼知是半兒郞", "desc": "감궁(1) 남자와 감궁(1) 여자가 만나 보필성의 잔잔한 기운을 나눕니다. 평범하고 조용한 가문을 이어가는 무해무덕(無害無德)한 인연입니다."},
            "1_2": {"status": "절명(絶命)", "classical": "破軍破財孤孀", "desc": "감궁(1) 남자와 곤궁(2) 여자가 만나 서로의 명줄을 끊어내는 극흉 결합입니다. 질병이 끊이지 않고 재물이 흩어지는 뼈아픈 파국을 경고합니다."},
            "1_3": {"status": "천의(天醫)", "classical": "巨三郞", "desc": "감궁(1) 남자와 진궁(3) 여자가 만나 거문성의 치유를 얻습니다. 고질병이 낫고 부동산과 재물이 태산처럼 쌓이는 대길(大吉)의 조합입니다."},
            "1_4": {"status": "생기(生氣)", "classical": "貪生五子", "desc": "감궁(1) 남자와 손궁(4) 여자가 만나 탐랑성의 강력한 생명력을 품습니다. 맨손으로 천금을 일구며, 자손이 번창하는 대길의 인연입니다."},
            "1_6": {"status": "육살(六殺)", "classical": "文曲水星僅一子", "desc": "감궁(1) 남자와 건궁(6) 여자가 만나 문곡성의 음란하고 패악한 기운에 휩쓸립니다. 이성 문제로 가산을 탕진하고 정서적 파멸을 맞이합니다."},
            "1_7": {"status": "화해(禍害)", "classical": "祿存土宿人遭殃", "desc": "감궁(1) 남자와 태궁(7) 여자가 만나 녹존성의 시비와 관재구설에 휘말립니다. 사소한 다툼이 소송으로 번지는 피로한 흉연(凶緣)입니다."},
            "1_8": {"status": "오귀(五鬼)", "classical": "廉貞獨火鬼兩箇", "desc": "감궁(1) 남자와 간궁(8) 여자가 만나 염정성의 화마(火魔)를 부릅니다. 불화가 끊이지 않고 일순간에 파산할 수 있는 위태로운 결합입니다."},
            "1_9": {"status": "연년(延年)", "classical": "武曲金星四子强", "desc": "감궁(1) 남자와 이궁(9) 여자가 만나 무곡성의 굳건한 백년해로를 약속합니다. 재물이 불어나고 부귀쌍전(富貴雙全)을 누립니다."},
            "2_1": {"status": "절명(絶命)", "classical": "破軍破財孤孀", "desc": "곤궁(2) 남자와 감궁(1) 여자가 만나 파군성의 처참한 파산을 부릅니다. 기운이 충돌하여 가세가 기울고 수명이 꺾일 흉상입니다."},
            "2_2": {"status": "복위(伏位)", "classical": "輔弼知是半兒郞", "desc": "곤궁(2) 남자와 곤궁(2) 여자가 만나 보필성의 고요한 기운이 겹칩니다. 치명적인 재앙은 피하나 기운이 정체되어 건조한 관계로 평생을 보냅니다."},
            "2_3": {"status": "화해(禍害)", "classical": "祿存土宿人遭殃", "desc": "곤궁(2) 남자와 진궁(3) 여자가 만나 녹존성의 재앙을 입습니다. 믿었던 이에게 배신당하며 소송으로 영혼이 피폐해집니다."},
            "2_4": {"status": "오귀(五鬼)", "classical": "廉貞獨火鬼兩箇", "desc": "곤궁(2) 남자와 손궁(4) 여자가 만나 염정성의 흉액을 일으킵니다. 집안에 흉사가 겹치고 패륜하는 자손을 두어 눈물을 흘릴 수 있습니다."},
            "2_6": {"status": "천의(天醫)", "classical": "巨三郞", "desc": "곤궁(2) 남자와 건궁(6) 여자가 만나 거문성의 축복을 받아 천의무봉의 가정을 이룹니다. 가산이 폭발적으로 늘고 무병장수합니다."},
            "2_7": {"status": "연년(延年)", "classical": "武曲金星四子强", "desc": "곤궁(2) 남자와 태궁(7) 여자가 만나 무곡성의 강인한 인연을 맺습니다. 하늘이 맺어준 짝으로 재물과 권력이 당대에 마르지 않습니다."},
            "2_8": {"status": "생기(生氣)", "classical": "貪生五子", "desc": "곤궁(2) 남자와 간궁(8) 여자가 만나 탐랑성의 폭발적인 생명력을 잉태합니다. 기어코 자수성가하여 가문의 이름을 천하에 떨칩니다."},
            "2_9": {"status": "육살(六殺)", "classical": "文曲水星僅一子", "desc": "곤궁(2) 남자와 이궁(9) 여자가 만나 문곡성의 피폐한 연분을 맺습니다. 속으로는 불륜과 향락으로 멍들어 집안 기둥이 뽑히는 파국입니다."},
            "3_1": {"status": "천의(天醫)", "classical": "巨三郞", "desc": "진궁(3) 남자와 감궁(1) 여자가 만나 거문성의 치유를 봅니다. 가세가 일일신 우일신 발전하고 수명이 길어집니다."},
            "3_2": {"status": "화해(禍害)", "classical": "祿存土宿人遭殃", "desc": "진궁(3) 남자와 곤궁(2) 여자가 만나 녹존성의 파재를 몰고 옵니다. 벌어놓은 재물마저 밑빠진 독에 물 붓듯 흩어지는 고단한 결합입니다."},
            "3_3": {"status": "복위(伏位)", "classical": "輔弼知是半兒郞", "desc": "진궁(3) 남자와 진궁(3) 여자가 만나 보필성의 기운으로 안정적입니다. 큰 욕심 없이 평탄하고 무던하게 살아가는 무해한 인연입니다."},
            "3_4": {"status": "연년(延年)", "classical": "武曲金星四子强", "desc": "진궁(3) 남자와 손궁(4) 여자가 만나 무곡성의 뿌리를 내립니다. 폭풍우에도 꺾이지 않는 튼튼한 가문을 형성하며 재물이 끊이지 않습니다."},
            "3_6": {"status": "오귀(五鬼)", "classical": "廉貞獨火鬼兩箇", "desc": "진궁(3) 남자와 건궁(6) 여자가 만나 염정성의 피바람을 몹니다. 부부간 증오가 극에 달하고 참사나 중병에 걸릴 극흉의 조합입니다."},
            "3_7": {"status": "절명(絶命)", "classical": "破軍破財孤孀", "desc": "진궁(3) 남자와 태궁(7) 여자가 만나 파군성의 칼부림에 희생됩니다. 질병, 파산, 이별의 3대 액운을 피할 수 없는 흉상입니다."},
            "3_8": {"status": "육살(六殺)", "classical": "文曲水星僅一子", "desc": "진궁(3) 남자와 간궁(8) 여자가 만나 문곡성의 진흙탕에 빠집니다. 재물이 무너지고 외도나 향락으로 상처와 원한만 남게 됩니다."},
            "3_9": {"status": "생기(生氣)", "classical": "貪生五子", "desc": "진궁(3) 남자와 이궁(9) 여자가 만나 탐랑성의 활력을 얻습니다. 집안이 맹렬하게 일어서며 천하에 부러울 것이 없는 가문이 됩니다."},
            "4_1": {"status": "생기(生氣)", "classical": "貪生五子", "desc": "손궁(4) 남자와 감궁(1) 여자가 만나 탐랑성의 막강한 창조력을 받습니다. 재산이 눈덩이처럼 불어나 부귀쌍전하는 최상길의 궁합입니다."},
            "4_2": {"status": "오귀(五鬼)", "classical": "廉貞獨火鬼兩箇", "desc": "손궁(4) 남자와 곤궁(2) 여자가 만나 염정성의 화마에 휩싸입니다. 화재, 구설, 도난이 끊이지 않아 재물이 흔적 없이 사라집니다."},
            "4_3": {"status": "연년(延年)", "classical": "武曲金星四子强", "desc": "손궁(4) 남자와 진궁(3) 여자가 만나 무곡성의 질긴 인연을 맺습니다. 조화롭게 부를 쌓고 튼튼한 가문을 닦아 명예를 누립니다."},
            "4_4": {"status": "복위(伏位)", "classical": "輔弼知是半兒郞", "desc": "손궁(4) 남자와 손궁(4) 여자가 만나 보필성의 안정을 취합니다. 뜨거운 불꽃은 없어도 평생 이별 없이 조용한 가정을 지킵니다."},
            "4_6": {"status": "화해(禍害)", "classical": "祿存土宿人遭殃", "desc": "손궁(4) 남자와 건궁(6) 여자가 만나 녹존성의 상처를 입습니다. 부인의 기에 눌려 남편이 기를 펴지 못하며 관재구설로 속을 끓입니다."},
            "4_7": {"status": "육살(六殺)", "classical": "文曲水星僅一子", "desc": "손궁(4) 남자와 태궁(7) 여자가 만나 문곡성의 문란한 풍파를 겪습니다. 부부궁에 균열이 가고 재물 손실로 육체가 병드는 흉악한 늪입니다."},
            "4_8": {"status": "절명(絶命)", "classical": "破軍破財孤孀", "desc": "손궁(4) 남자와 간궁(8) 여자가 만나 파군성의 최악의 파멸을 맞습니다. 수명을 깎아 먹어 비참하고 고독하게 끝을 맺는 극흉살입니다."},
            "4_9": {"status": "천의(天醫)", "classical": "巨三郞", "desc": "손궁(4) 남자와 이궁(9) 여자가 만나 거문성의 치유와 발복을 낳습니다. 가산을 크게 일으키고 잔병 없이 천수를 누리는 으뜸 궁합입니다."},
            "6_1": {"status": "육살(六殺)", "classical": "文曲水星僅一子", "desc": "건궁(6) 남자와 감궁(1) 여자가 만나 문곡성의 음란하고 패악한 늪에 빠집니다. 주색잡기와 사치로 가산을 탕진하고 자손이 흩어지는 흉연입니다."},
            "6_2": {"status": "천의(天醫)", "classical": "巨三郞", "desc": "건궁(6) 남자와 곤궁(2) 여자가 만나 거문성의 찬란한 축복을 얻습니다. 가문이 번창하고 앓던 병마도 물러가 무병장수하는 대길의 명입니다."},
            "6_3": {"status": "오귀(五鬼)", "classical": "廉貞獨火鬼兩箇", "desc": "건궁(6) 남자와 진궁(3) 여자가 만나 염정성의 독기를 부릅니다. 거대한 끔찍한 불화가 일어나며 참사가 줄을 잇는 위태로운 결합입니다."},
            "6_4": {"status": "화해(禍害)", "classical": "祿存土宿人遭殃", "desc": "건궁(6) 남자와 손궁(4) 여자가 만나 녹존성의 지독한 구설에 휘말립니다. 재물은 뿔뿔이 흩어지고 잦은 다툼으로 수명이 줄어듭니다."},
            "6_6": {"status": "복위(伏位)", "classical": "輔弼知是半兒郞", "desc": "건궁(6) 남자와 건궁(6) 여자가 만나 보필성의 단단하고 고요한 기운을 나눕니다. 철옹성처럼 풍파를 막으나 자손 운이 다소 약할 수 있습니다."},
            "6_7": {"status": "생기(生氣)", "classical": "貪生五子", "desc": "건궁(6) 남자와 태궁(7) 여자가 만나 탐랑성의 막강한 창조력을 폭발시킵니다. 막대한 부를 쌓고 걸출한 자손을 거느려 태평성대입니다."},
            "6_8": {"status": "연년(延年)", "classical": "武曲金星四子强", "desc": "건궁(6) 남자와 간궁(8) 여자가 만나 무곡성의 백년해로를 약속합니다. 흔들림 없는 자산과 후계자가 끊이지 않는 길상입니다."},
            "6_9": {"status": "절명(絶命)", "classical": "破軍破財孤孀", "desc": "건궁(6) 남자와 이궁(9) 여자가 만나 파군성의 처참한 파멸을 맞습니다. 용광로 불길에 녹아내리듯 뼈아픈 파산과 단명이 기다립니다."},
            "7_1": {"status": "화해(禍害)", "classical": "祿存土宿人遭殃", "desc": "태궁(7) 남자와 감궁(1) 여자가 만나 녹존성의 시비와 소송을 부릅니다. 아무리 벌어도 재물이 줄줄 새어나가고 원망이 쌓입니다."},
            "7_2": {"status": "연년(延年)", "classical": "武曲金星四子强", "desc": "태궁(7) 남자와 곤궁(2) 여자가 만나 무곡성의 영광을 지킵니다. 부부의 애정이 단단하며 만금과 무병장수를 누립니다."},
            "7_3": {"status": "절명(絶命)", "classical": "破軍破財孤孀", "desc": "태궁(7) 남자와 진궁(3) 여자가 만나 파군성의 피바람에 휩쓸립니다. 생명줄을 재촉하여 패가망신하고 종국엔 고독해집니다."},
            "7_4": {"status": "육살(六殺)", "classical": "文曲水星僅一子", "desc": "태궁(7) 남자와 손궁(4) 여자가 만나 문곡성의 피폐한 연분을 맺습니다. 외도와 향락으로 영혼과 재물이 병드는 흉연입니다."},
            "7_6": {"status": "생기(生氣)", "classical": "貪生五子", "desc": "태궁(7) 남자와 건궁(6) 여자가 만나 탐랑성의 경이로운 생명력을 잉태합니다. 폭발적인 재산 증식과 자손의 번창을 하늘이 보증합니다."},
            "7_7": {"status": "복위(伏位)", "classical": "輔弼知是半兒郞", "desc": "태궁(7) 남자와 태궁(7) 여자가 만나 보필성의 호수를 이룹니다. 극적인 부의 요동은 없으나 무던하게 생을 지켜가는 동반자입니다."},
            "7_8": {"status": "천의(天醫)", "classical": "巨三郞", "desc": "태궁(7) 남자와 간궁(8) 여자가 만나 거문성의 완벽한 안식을 받습니다. 병치레 없이 천수를 누리며 귀한 자식농사에 대성합니다."},
            "7_9": {"status": "오귀(五鬼)", "classical": "廉貞獨火鬼兩箇", "desc": "태궁(7) 남자와 이궁(9) 여자가 만나 염정성의 미쳐 날뛰는 불귀신을 마주합니다. 끔찍한 사고와 갈등으로 집안이 잿더미가 됩니다."},
            "8_1": {"status": "오귀(五鬼)", "classical": "廉貞獨火鬼兩箇", "desc": "간궁(8) 남자와 감궁(1) 여자가 만나 염정성의 흉포한 화마에 휩싸입니다. 파산과 재난이 줄을 이으며 가족이 뿔뿔이 흩어집니다."},
            "8_2": {"status": "생기(生氣)", "classical": "貪生五子", "desc": "간궁(8) 남자와 곤궁(2) 여자가 만나 탐랑성의 눈부신 부활을 맞이합니다. 막대한 부를 일구며 자손이 천하를 호령합니다."},
            "8_3": {"status": "육살(六殺)", "classical": "文曲水星僅一子", "desc": "간궁(8) 남자와 진궁(3) 여자가 만나 문곡성의 타락한 결말을 봅니다. 지나친 욕망으로 집안을 망치고 자손의 맥이 끊깁니다."},
            "8_4": {"status": "절명(絶命)", "classical": "破軍破財孤孀", "desc": "간궁(8) 남자와 손궁(4) 여자가 만나 파군성의 단절을 맞이합니다. 재물은 박살 나고 수명을 깎아 비참하고 고독하게 끝을 맺습니다."},
            "8_6": {"status": "연년(延年)", "classical": "武曲金星四子强", "desc": "간궁(8) 남자와 건궁(6) 여자가 만나 무곡성의 철옹성을 세웁니다. 변치 않는 애정으로 부귀영화를 쥐고 훌륭한 자손을 봅니다."},
            "8_7": {"status": "천의(天醫)", "classical": "巨三郞", "desc": "간궁(8) 남자와 태궁(7) 여자가 만나 거문성의 융성함을 얻습니다. 몸과 마음의 상처가 낫고 거대한 자산과 다복한 자녀를 얻습니다."},
            "8_8": {"status": "복위(伏位)", "classical": "輔弼知是半兒郞", "desc": "간궁(8) 남자와 간궁(8) 여자가 만나 보필성의 무거운 안정감을 나눕니다. 극적인 횡재수는 없어도 흔들림 없이 가문을 이어갑니다."},
            "8_9": {"status": "화해(禍害)", "classical": "祿存土宿人遭殃", "desc": "간궁(8) 남자와 이궁(9) 여자가 만나 녹존성의 헛된 수고를 겪습니다. 겉보기만 상생일 뿐 관재구설과 배신으로 피땀 흘린 재산을 잃습니다."},
            "9_1": {"status": "연년(延年)", "classical": "武曲金星四子强", "desc": "이궁(9) 남자와 감궁(1) 여자가 만나 무곡성의 백년해로를 이룹니다. 수화기제의 조화를 이루어 막대한 재물을 쌓고 자손이 튼튼합니다."},
            "9_2": {"status": "육살(六殺)", "classical": "文曲水星僅一子", "desc": "이궁(9) 남자와 곤궁(2) 여자가 만나 문곡성의 건조한 비극에 빠집니다. 욕망이 유흥과 외도로 변질되어 가계를 파탄 냅니다."},
            "9_3": {"status": "생기(生氣)", "classical": "貪生五子", "desc": "이궁(9) 남자와 진궁(3) 여자가 만나 탐랑성의 번영을 일굽니다. 가문의 명예와 부가 맹렬히 솟구치며 훌륭한 자손들이 줄을 잇습니다."},
            "9_4": {"status": "천의(天醫)", "classical": "巨三郞", "desc": "이궁(9) 남자와 손궁(4) 여자가 만나 거문성의 치유를 누립니다. 죽을 병도 비껴가며 부동산과 자본이 태산처럼 쌓이는 으뜸 인연입니다."},
            "9_6": {"status": "절명(絶命)", "classical": "破軍破財孤孀", "desc": "이궁(9) 남자와 건궁(6) 여자가 만나 파군성의 소름 끼치는 파멸을 마주합니다. 명줄을 재촉하여 단명하거나 멸문의 화를 초래합니다."},
            "9_7": {"status": "오귀(五鬼)", "classical": "廉貞獨火鬼兩箇", "desc": "이궁(9) 남자와 태궁(7) 여자가 만나 염정성의 흉포한 귀신에 휩싸입니다. 미친 듯이 싸우고 파산과 사고가 겹쳐 모든 것을 잃는 대흉살입니다."},
            "9_8": {"status": "화해(禍害)", "classical": "祿存土宿人遭殃", "desc": "이궁(9) 남자와 간궁(8) 여자가 만나 녹존성의 억울한 누명을 씁니다. 뜻이 겉돌고 피땀 흘린 재산이 남의 손으로 빠져나갑니다."},
            "9_9": {"status": "복위(伏位)", "classical": "輔弼知是半兒郞", "desc": "이궁(9) 남자와 이궁(9) 여자가 만나 보필성의 따스한 온기를 유지합니다. 맹렬한 발전은 없으나 건조하고 평범하게 백년해로합니다."}
        }

        # ==========================================
        # [로직 복구 완료] 남녀혼인 멸문법 및 상부상처살 DB
        # ==========================================
        self.myeolmun_db = {
            1: 9, 2: 8, 3: 7, 4: 6, 5: 5, 
            6: 4, 7: 3, 8: 2, 9: 1, 10: 12, 11: 11, 12: 10
        }
        self.sangbu_db = {
            "子": [1, 2], "午": [1, 2], "丑": [4, 5], "未": [4, 5], "寅": [7, 8], "申": [7, 8]
        }

    # ==========================================
    # 🛡️ 추가된 헬퍼 함수: 에러 원천 차단 
    # ==========================================
    def _extract_safe_int(self, val, default=0):
        if isinstance(val, dict):
            if "number" in val:
                try: return int(val["number"])
                except: pass
            for v in val.values():
                if isinstance(v, int) or (isinstance(v, str) and v.isdigit()):
                    return int(v)
            return default
        try:
            return int(val)
        except (ValueError, TypeError):
            return default

    # ==========================================
    # 유틸리티 (본명성 추출용)
    # ==========================================
    def _split_name_hanja(self, raw_str: str) -> tuple:
        try:
            if not isinstance(raw_str, str): raw_str = str(raw_str)
            if "(" in raw_str and ")" in raw_str:
                parts = raw_str.split("(")
                return parts[0].strip(), parts[1].replace(")", "").strip()
            return raw_str, ""
        except Exception:
            return str(raw_str), ""

    def _get_root_number(self, year) -> int:
        try:
            year_str = "".join(filter(str.isdigit, str(year)))
            if not year_str: return 1
            r = sum(int(digit) for digit in year_str)
            while r > 9:
                r = sum(int(digit) for digit in str(r))
            return r
        except Exception:
            return 1

    def get_bonmyeongseong(self, year, gender) -> dict:
        try:
            root_num = self._get_root_number(year)
            if str(gender).upper() == 'M': star_num = (11 - root_num) % 9
            else: star_num = (4 + root_num) % 9
            if star_num == 0: star_num = 9
            
            star_full = self.stars.get(star_num, "일백수성(一白水星)")
            name_clean, hanja_clean = self._split_name_hanja(star_full)
            
            return {"number": star_num, "name": name_clean, "hanja": hanja_clean}
        except Exception:
            return {"number": 1, "name": "알 수 없음", "hanja": "無"}

    # ==========================================
    # 🚨 [업그레이드 1] 싱글 유저 이상형(최고의 궁합) 성별 맞춤형 역산 처방
    # ==========================================
    def get_ideal_partner(self, bazi: dict, yongshin: dict, star_num: int, gender: str) -> dict:
        """ 파트너 정보가 없을 때, 나만의 완벽한 맞춤 이상형을 남/녀 입장에 맞춰 역산(Reverse-Engineering)합니다. """
        try:
            bazi = bazi if isinstance(bazi, dict) else {}
            yongshin = yongshin if isinstance(yongshin, dict) else {}
            
            y_branch = bazi.get("year", {}).get("branch", "")
            d_branch = bazi.get("day", {}).get("branch", "")
            
            animals = {"子":"쥐", "丑":"소", "寅":"호랑이", "卯":"토끼", "辰":"용", "巳":"뱀", "午":"말", "未":"양", "申":"원숭이", "酉":"닭", "戌":"개", "亥":"돼지"}
            
            samhap = {
                "申":"쥐, 용", "子":"원숭이, 용", "辰":"원숭이, 쥐",
                "亥":"토끼, 양", "卯":"돼지, 양", "未":"돼지, 토끼",
                "寅":"말, 개", "午":"호랑이, 개", "戌":"호랑이, 말",
                "巳":"닭, 소", "酉":"뱀, 소", "丑":"뱀, 닭"
            }
            yukhap = {"子":"소", "丑":"쥐", "寅":"돼지", "亥":"호랑이", "卯":"개", "戌":"토끼", "辰":"닭", "酉":"용", "巳":"원숭이", "申":"뱀", "午":"양", "未":"말"}
            
            my_animal = animals.get(y_branch, "")
            
            y_str = str(yongshin.get("yongshin", ""))
            h_str = str(yongshin.get("huishin", ""))
            needs_list = [e for e in [y_str, h_str] if e]
            
            # 🚨 성별에 따른 십신(관성/재성) 심리적 니즈 분리
            if str(gender).upper() == 'F':
                gender_role_desc = "여성분에게는 든든한 울타리와 책임감을 상징하는 '관성(官星)'의 역할이 중요합니다. 리더십이 강하고 당신을 포용력 있게 이끌어줄 수 있는 "
            else:
                gender_role_desc = "남성분에게는 현실 감각과 결실을 상징하는 '재성(財星)'의 역할이 중요합니다. 섬세하고 지혜로우며 당신의 삶에 안정을 부여할 수 있는 "

            if needs_list:
                elements_desc = f"{gender_role_desc}사주 구조를 가진 사람이어야 합니다. 특히 당신에게 가장 절실한 수호 에너지인 [{', '.join(needs_list)}] 기운을 풍부하게 가진 사람을 만나면, 정서적 안정은 물론 재물운까지 수직 상승하게 됩니다."
            else:
                elements_desc = f"{gender_role_desc}사람을 찾으십시오. 자신의 기운이 뚜렷하여 상대의 오행에 크게 기대지 않아도 되는 독립적인 명식이므로, 서로의 페이스를 존중할 수 있는 이해심이 가장 중요합니다."

            best_stars = []
            star_num_int = self._extract_safe_int(star_num, default=1)
            for i in range(1, 10):
                if i == 5: continue
                m_t = star_num_int if str(gender).upper() == 'M' else i
                f_t = i if str(gender).upper() == 'M' else star_num_int
                m_t = 2 if m_t == 5 else m_t
                f_t = 8 if f_t == 5 else f_t
                
                key = f"{m_t}_{f_t}"
                status = self.gugung_matrix.get(key, {}).get("status", "")
                if status in ["생기(生氣)", "천의(天醫)", "연년(延年)"]:
                    best_stars.append(f"{i}성")
            
            return {
                "추천_나이와_띠": f"당신의 띠({my_animal}띠)를 기준으로 볼 때, '4살 차이'인 [{samhap.get(y_branch, '')}띠]와의 만남이 가장 이상적입니다. 4살 차이는 예로부터 궁합도 보지 않는다고 할 만큼 가치관이 잘 맞습니다. 또한 영혼의 단짝이라 불리는 육합 관계인 [{yukhap.get(y_branch, '')}띠]도 훌륭한 인연입니다.",
                "영혼의_속궁합": f"일지(배우자궁)를 기준으로 당신과 육체적/정서적 교감이 완벽히 이루어지는 상대는 지지에 [{yukhap.get(d_branch, '')}띠] 기운을 가진 사람입니다. 이 기운을 가진 사람과는 대화가 깊이 통하고 맹목적인 끌림을 느낍니다.",
                "최적의_오행과_기운": elements_desc,
                "천생연분_별자리": f"당신의 별자리와 64구궁팔괘 매트릭스를 역산해 보았을 때, 하늘의 축복을 받는 상대의 별자리(본명성)는 [{', '.join(best_stars)}]입니다. 이 별자리를 가진 사람과 맺어지면 천의(치유)와 생기(활력)를 얻어 무병장수하고 굳건한 백년해로를 이룹니다."
            }
            
        except Exception as e:
            return {"안내": "상세 이상형 처방을 계산할 수 없습니다. 사주 구조가 매우 특수합니다."}

    # ==========================================
    # 🚨 [업그레이드 2] 치명적 위기(흉살) 쌍방향 스캔
    # ==========================================
    def scan_fatal_disasters(self, m_bazi: dict, f_bazi: dict, m_lunar_m: int, f_lunar_m: int) -> list:
        warnings = []
        try:
            m_bazi = m_bazi if isinstance(m_bazi, dict) else {}
            f_bazi = f_bazi if isinstance(f_bazi, dict) else {}
            
            m_year = m_bazi.get("year", {}) if isinstance(m_bazi, dict) else {}
            m_year_branch = m_year.get("branch", "") if isinstance(m_year, dict) else ""
            
            f_year = f_bazi.get("year", {}) if isinstance(f_bazi, dict) else {}
            f_year_branch = f_year.get("branch", "") if isinstance(f_year, dict) else ""
            
            # 멸문살 (월 vs 월)
            if m_lunar_m and f_lunar_m:
                if self.myeolmun_db.get(m_lunar_m) == f_lunar_m:
                    warnings.append(
                        f"【멸문살(滅門殺) 경고】 남성의 생월({m_lunar_m}월)과 여성의 생월({f_lunar_m}월)이 충돌하여 가문을 쇠락하게 하는 흉액이 있습니다. 서로에 대한 극도의 배려와 헌신이 필요합니다."
                    )

            # 상처살 (남성 띠 vs 여성 달)
            if f_lunar_m and m_year_branch:
                 if f_lunar_m in self.sangbu_db.get(m_year_branch, []):
                     warnings.append(
                        f"【상처살(喪妻殺) 경고】 남성의 띠({m_year_branch}) 기운이 여성의 생월({f_lunar_m}월)을 강하게 극(剋)하여 여성의 건강과 수명을 위협할 수 있습니다. 각자의 사생활 존중과 주말부부 등 물리적 거리감이 액땜이 될 수 있습니다."
                     )
                     
            # 상부살 (여성 띠 vs 남성 달 - 쌍방향 스캔 로직 추가)
            if m_lunar_m and f_year_branch:
                 if m_lunar_m in self.sangbu_db.get(f_year_branch, []):
                     warnings.append(
                        f"【상부살(喪夫殺) 경고】 여성의 띠({f_year_branch}) 기운이 남성의 생월({m_lunar_m}월)을 강하게 극(剋)하여 남성의 사회적 입지와 건강을 위협할 수 있습니다. 서로 일에 간섭하지 않는 쿨한 관계 유지가 필수입니다."
                     )
        except Exception:
            pass
        return warnings

    # ==========================================
    # 🚨 [업그레이드 3] 오행 구원 쌍방향 크로스체크
    # ==========================================
    def calculate_elemental_salvation(self, m_yongshin: dict, f_elements: dict, f_yongshin: dict, m_elements: dict) -> dict:
        try:
            m_yongshin = m_yongshin if isinstance(m_yongshin, dict) else {}
            f_yongshin = f_yongshin if isinstance(f_yongshin, dict) else {}
            f_elements = f_elements if isinstance(f_elements, dict) else {}
            m_elements = m_elements if isinstance(m_elements, dict) else {}
            
            m_need = str(m_yongshin.get("yongshin", "")) + str(m_yongshin.get("huishin", ""))
            f_need = str(f_yongshin.get("yongshin", "")) + str(f_yongshin.get("huishin", ""))

            def safe_count(val):
                try: return int(val)
                except: return 0

            # 여자가 남자를 돕는가?
            m_helped = False
            if "목" in m_need and safe_count(f_elements.get("목", 0)) >= 2: m_helped = True
            if "화" in m_need and safe_count(f_elements.get("화", 0)) >= 2: m_helped = True
            if "토" in m_need and safe_count(f_elements.get("토", 0)) >= 2: m_helped = True
            if "금" in m_need and safe_count(f_elements.get("금", 0)) >= 2: m_helped = True
            if "수" in m_need and safe_count(f_elements.get("수", 0)) >= 2: m_helped = True

            # 남자가 여자를 돕는가?
            f_helped = False
            if "목" in f_need and safe_count(m_elements.get("목", 0)) >= 2: f_helped = True
            if "화" in f_need and safe_count(m_elements.get("화", 0)) >= 2: f_helped = True
            if "토" in f_need and safe_count(m_elements.get("토", 0)) >= 2: f_helped = True
            if "금" in f_need and safe_count(m_elements.get("금", 0)) >= 2: f_helped = True
            if "수" in f_need and safe_count(m_elements.get("수", 0)) >= 2: f_helped = True

            if m_helped and f_helped:
                return {
                    "score": 95, 
                    "desc": "남성의 사주와 여성의 사주가 서로에게 가장 간절히 필요한 오행(용신)을 완벽하게 채워주고 있습니다. 한쪽이 무너지면 다른 한쪽이 살려내는 끈끈한 생명 공동체이자 '쌍방향 상호구원'의 최고 길연(吉緣)입니다."
                }
            elif m_helped:
                return {
                    "score": 75, 
                    "desc": "여성의 사주에 남성이 간절히 필요로 하는 수호 에너지가 풍부하여 남성의 막힌 숨통을 틔워줍니다. 여성의 헌신적인 내조와 희생이 돋보이며, 남성이 이를 귀하게 여겨야 관계가 오래 지속됩니다."
                }
            elif f_helped:
                return {
                    "score": 75, 
                    "desc": "남성의 사주에 여성이 간절히 필요로 하는 수호 에너지가 풍부하여 여성에게 든든한 방어막이 되어줍니다. 남성의 확고한 외조와 포용력이 돋보이며, 여성이 심리적 안정을 크게 얻는 훌륭한 궁합입니다."
                }
            else:
                return {
                    "score": 50, 
                    "desc": "서로의 사주에서 특별히 강력하게 나의 부족한 오행을 구원해 주는 상생의 에너지는 보이지 않습니다. 상대방에게 일방적으로 기대기보다는, 각자의 자립심과 노력으로 위기를 헤쳐나가야 하는 각자도생의 건조한 관계입니다."
                }
        except Exception:
            return {"score": 0, "desc": "오행 분석에 필요한 데이터가 불충분합니다."}

    # 3. 입체적(3D) 속궁합 및 정신적 교감
    def analyze_3d_match(self, m_day_pillar: dict, f_day_pillar: dict) -> dict:
        try:
            m_day_pillar = m_day_pillar if isinstance(m_day_pillar, dict) else {}
            f_day_pillar = f_day_pillar if isinstance(f_day_pillar, dict) else {}
            
            m_stem = str(m_day_pillar.get("stem", ""))
            f_stem = str(f_day_pillar.get("stem", ""))
            m_branch = str(m_day_pillar.get("branch", ""))
            f_branch = str(f_day_pillar.get("branch", ""))

            mental = {"status": "평범", "desc": "정신적으로 무난하게 타협 가능한 동반자입니다."}
            if {m_stem, f_stem} in [{"甲", "己"}, {"乙", "庚"}, {"丙", "辛"}, {"丁", "壬"}, {"戊", "癸"}]:
                mental = {"status": "천간합(天干合)", "desc": "가치관이 소름 돋게 일치하며, 대화가 밤새 끊이지 않는 영혼의 단짝입니다."}
            elif {m_stem, f_stem} in [{"甲", "庚"}, {"乙", "辛"}, {"丙", "壬"}, {"丁", "癸"}]:
                mental = {"status": "천간충(天干沖)", "desc": "생각하는 방식이 정반대입니다. 잦은 언쟁이 발생하나 서로의 맹점을 깨우쳐주기도 합니다."}

            physical = {"status": "평범", "pros": "무던한 일상 유지", "cons": "다소 권태로울 수 있음"}
            if {m_branch, f_branch} in [{"子", "丑"}, {"寅", "亥"}, {"卯", "戌"}, {"辰", "酉"}, {"巳", "申"}, {"午", "未"}]:
                physical = {"status": "육합(六合)", "pros": "천생연분의 속궁합과 무한한 애정", "cons": "서로에게 갇혀 외부 대인관계가 단절될 우려"}
            elif {m_branch, f_branch} in [{"子", "午"}, {"丑", "未"}, {"寅", "申"}, {"卯", "酉"}, {"辰", "戌"}, {"巳", "亥"}]:
                physical = {"status": "충(沖)", "pros": "초반의 강렬한 스파크와 매력", "cons": "잦은 충돌과 좁혀지지 현실적 거리감"}
            elif {m_branch, f_branch} in [{"子", "未"}, {"丑", "午"}, {"寅", "酉"}, {"卯", "申"}, {"辰", "亥"}, {"巳", "戌"}]:
                physical = {"status": "원진(怨嗔)", "pros": "자석 같은 치명적 끌림과 맹목적 집착", "cons": "서로를 뜯어먹는 피말리는 감정소모"}

            return {"mental": mental, "physical": physical}
        except Exception:
            return {"mental": {"status": "분석 불가", "desc": "데이터 부족"}, "physical": {"status": "분석 불가", "pros": "-", "cons": "-"}}

    # 4. 64구궁(본명성) 매트릭스 도출
    def get_64_gugung_matrix(self, m_star: int, f_star: int) -> dict:
        try:
            if m_star is None or f_star is None or m_star == 0 or f_star == 0:
                return {"status": "알 수 없음", "classical": "無", "desc": "본명성 데이터가 부족하여 구궁팔괘 매트릭스를 계산할 수 없습니다."}
                
            m_trigram = 2 if int(m_star) == 5 else int(m_star)
            f_trigram = 8 if int(f_star) == 5 else int(f_star)
            
            combo_key = f"{m_trigram}_{f_trigram}"
            return self.gugung_matrix.get(combo_key, {
                "status": "알 수 없음", "classical": "無", "desc": "두 사람의 본명궁 조합 파동이 평범하여 극적인 길흉이 나타나지 않습니다."
            })
        except Exception:
            return {"status": "연산 오류", "classical": "無", "desc": "매트릭스 도출 중 데이터 충돌이 발생했습니다."}

    # ==========================================
    # 🚀 최종 융합 렌더링 파이프라인
    # ==========================================
    def get_ultimate_compatibility(
        self, 
        m_bazi=None, 
        f_bazi=None, 
        m_lunar_m=None, 
        f_lunar_m=None, 
        m_yongshin=None, 
        f_yongshin=None, 
        m_elements=None, 
        f_elements=None, 
        m_star=None, 
        f_star=None
    ) -> dict:
        try:
            m_bazi = m_bazi if isinstance(m_bazi, dict) else {}
            f_bazi = f_bazi if isinstance(f_bazi, dict) else {}
            
            m_day = m_bazi.get("day", {}) if isinstance(m_bazi, dict) and isinstance(m_bazi.get("day"), dict) else {}
            f_day = f_bazi.get("day", {}) if isinstance(f_bazi, dict) and isinstance(f_bazi.get("day"), dict) else {}

            m_lunar_m_int = self._extract_safe_int(m_lunar_m)
            f_lunar_m_int = self._extract_safe_int(f_lunar_m)
            m_star_int = self._extract_safe_int(m_star, default=1)
            f_star_int = self._extract_safe_int(f_star, default=1)

            return {
                "fatal_warnings": self.scan_fatal_disasters(m_bazi, f_bazi, m_lunar_m_int, f_lunar_m_int),
                "elemental_salvation": self.calculate_elemental_salvation(m_yongshin, f_elements, f_yongshin, m_elements),
                "match_3d": self.analyze_3d_match(m_day, f_day),
                "gugung_matrix": self.get_64_gugung_matrix(m_star_int, f_star_int)
            }
        except Exception as e:
            return {
                "fatal_warnings": [f"엔진 연산 중 내부 오류가 방어되었습니다. ({str(e)})"],
                "elemental_salvation": {"score": 0, "desc": "상대방 데이터 불균형으로 분석을 완료하지 못했습니다."},
                "match_3d": {"mental": {"status": "분석 불가", "desc": "-"}, "physical": {"status": "분석 불가", "pros": "-", "cons": "-"}},
                "gugung_matrix": {"status": "연산 중단", "classical": "無", "desc": "엔진 내부에서 알 수 없는 충돌을 방어했습니다."}
            }