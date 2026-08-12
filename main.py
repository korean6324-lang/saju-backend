from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import copy  
from korean_lunar_calendar import KoreanLunarCalendar 

# ==========================================
# 🌟 모든 엔진 총동원 (10개의 심장)
# ==========================================
from core_astro import CoreAstroEngine
from core_mechanics import MechanicsEngine
from dictionary import DictionaryEngine
from logic_dynamics import DynamicsEngine
from logic_fengshui import FengShuiEngine
from logic_gunghap import GunghapEngine
from logic_practical import PracticalEngine
from logic_unse import UnseEngine
from logic_yongshin import YongshinEngine
from logic_classical import ClassicalEngine 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

astro = CoreAstroEngine()
mech = MechanicsEngine()
dict_db = DictionaryEngine()
dyn = DynamicsEngine()
feng = FengShuiEngine()
ghap = GunghapEngine()
prac = PracticalEngine()
unse = UnseEngine()
yong = YongshinEngine()
clas = ClassicalEngine() 

NAPEUM_RICH_DESC = {
    "ko": {
        "해중금": "바다 깊은 곳에 잠긴 보석. 겉으로 드러나지 않는 깊은 내공과 무한한 잠재력을 지니고 있습니다.", "노중화": "화로 속에서 타오르는 불꽃. 따뜻하고 보호받는 환경에서 은근한 끈기와 지성을 발휘합니다.", "대림목": "울창하고 거대한 숲. 스케일이 크고 수많은 생명을 품어내는 웅장한 포용력을 뜻합니다.", "대림토": "울창하고 거대한 숲(대림목). 스케일이 크고 수많은 생명을 품어내는 웅장한 포용력을 뜻합니다.", "노방토": "사람들이 밟고 지나가는 길가의 흙. 희생정신이 강하고 친화력이 뛰어나 대중과 잘 어울립니다.", "검봉금": "날카롭게 벼려진 명검. 불의를 참지 않는 예리한 결단력과 강력한 카리스마를 발휘합니다.", "산두화": "산봉우리에서 타오르는 횃불. 멀리서도 빛을 발하며 사람들을 이끄는 선구자적 기질이 있습니다.", "간하수": "산골짜기를 흐르는 맑은 시냇물. 잔잔하면서도 멈추지 않는 생명력과 맑고 순수한 영혼을 가졌습니다.", "성두토": "성벽을 이루는 단단한 흙. 외부의 적을 막아내는 굳건한 책임감과 흔들림 없는 원칙을 상징합니다.", "백랍금": "촛물처럼 굳어지는 부드러운 금. 유연성과 융통성이 뛰어나며 환경에 맞게 자신을 다듬어냅니다.", "백납금": "촛물처럼 굳어지는 부드러운 금. 유연성과 융통성이 뛰어나며 환경에 맞게 자신을 다듬어냅니다.", "양류목": "물가에 흐드러진 수양버들. 부드럽고 유연하며, 거센 바람에도 부러지지 않는 처세술이 뛰어납니다.", "천중수": "땅속 깊은 곳에서 솟아나는 옹달샘. 마르지 않는 지혜와 타인에게 베푸는 순수한 자비심이 있습니다.", "옥상토": "지붕 위에 덮인 기와/흙. 외부의 풍파로부터 사람들을 보호하며 높은 곳에서 세상을 굽어봅니다.", "벽력화": "어둠을 가르는 천둥 번개. 순간적으로 폭발하는 천재성과 누구도 흉내 내지 못할 독창성을 가졌습니다.", "송백목": "한겨울에도 푸른 소나무와 잣나무. 어떤 시련 속에서도 굽히지 않는 지조와 매서운 절개가 있습니다.", "장류수": "끊임없이 흘러가는 긴 강물. 멈추지 않는 도전정신과 거대한 세력을 형성하여 바다로 나아가는 기상입니다.", "사중금": "모래 속에 파묻힌 사금. 오랜 시간 다듬어지고 발견되기를 기다리는 귀하고 섬세한 가치입니다.", "산하화": "산기슭에서 타오르는 노을/불꽃. 은은하면서도 세상을 아름답게 물들이는 예술적 감각이 돋보입니다.", "평지목": "평야에 자라난 나무. 평탄한 환경 속에서 안정적으로 성장하며 무난하고 건실한 삶을 추구합니다.", "벽상토": "집을 지탱하는 벽의 흙. 겉보기엔 평범하나 사람들의 안식처를 지탱하는 보이지 않는 든든한 조력자입니다.", "금박금": "불상을 입히는 얇은 금박. 화려하고 장엄한 매력으로 타인을 돋보이게 하는 특수하고 빛나는 재능입니다.", "복등화": "어둠을 밝히는 등잔불. 고독하고 외로운 이들에게 희망을 주는 따뜻하고 헌신적인 종교적/철학적 기운입니다.", "천하수": "하늘에서 내리는 은하수/비. 만물을 적시고 생명을 부여하는 맑고 고결한 영혼과 순수함이 있습니다.", "대역토": "넓은 광야와 역마의 흙. 스케일이 방대하고 여러 지역을 아우르는 수용력과 무역/유통의 기운을 뜻합니다.", "차천금": "여인을 장식하는 비녀와 팔찌. 세련되고 섬세한 미적 감각과 귀족적이고 화려한 품격을 상징합니다.", "상자목": "비단을 짜는 누에를 치는 뽕나무. 타인을 위해 유용한 가치를 창출하고 희생으로 큰 업적을 이룹니다.", "대계수": "깊은 산에서 모여 흐르는 계곡물. 맑고 차가운 지성으로 만물의 갈증을 해소하는 학자적 기질이 있습니다.", "사중토": "모래와 섞인 흙. 비바람을 견디며 자신만의 견고한 터전을 일구어내는 강인하고 거친 끈기가 있습니다.", "천상화": "하늘 한가운데 뜬 태양. 천하를 공평하게 비추며 만물을 길러내는 압도적인 스케일과 공명정대함을 가졌습니다.", "석류목": "가을에 단단하게 익은 석류나무. 화려함 속에 꽉 찬 결실을 품고 있으며 재물과 자손의 번창을 상징합니다.", "대해수": "모든 것을 삼키는 거대한 바다. 속을 알 수 없는 깊은 지혜와 모든 선악을 포용하는 압도적인 수용력이 있습니다."
    },
    "ja": {
        "해중금": "海の底に沈んだ宝石。表に現れない深い内功と無限の潜在力を持っています。", "노중화": "炉の中で燃え上がる炎。暖かく保護された環境でひそかな粘り強さと知性を発揮します。", "대림목": "鬱蒼とした巨大な森。スケールが大きく数多くの生命を抱く雄大な包容力を意味します。", "대림토": "鬱蒼とした巨大な森（大林木）。スケールが大きく数多くの生命を抱く雄大な包容力を意味します。", "노방토": "人々が踏みしめていく道端の土。自己犠牲の精神が強く、親和性に優れ大衆とよく調和します。", "검봉금": "鋭く研がれた名剣。不正を許さない鋭い決断力と強力なカリスマを発揮します。", "산두화": "山頂で燃え上がる松明。遠くからも光を放ち人々を導く先駆者的な気質があります。", "간하수": "山谷を流れる澄んだ小川。穏やかながらも立ち止まらない生命力と清らかで純粋な魂を持っています。", "성두토": "城壁を成す固い土。外部の敵を防ぐ強固な責任感と揺るぎない原則を象徴します。", "백랍금": "蝋のようには固まる柔らかい金。柔軟性と融通性に優れ、環境に合わせて自らを磨き上げます。", "백납금": "蝋のようには固まる柔らかい金。柔軟性と融通性に優れ、環境に合わせて自らを磨き上げます。", "양류목": "水辺に咲き乱れる柳。柔らかく柔軟で、強い風にも折れない処世術に優れています。", "천중수": "地中深くに湧き出る泉。枯れることのない知恵と他人に施す純粋な慈悲心があります。", "옥상토": "屋根の上に覆われた瓦/土。外部の風波から人々を保護し、高いところから世界を見下ろします。", "벽력화": "闇を切り裂く雷妻。瞬間的に爆発する天才性と誰にも真似できない独創性を持っています。", "송백목": "真冬にも青い松と柏。いかなる試練の中でも屈しない志と厳しい節操があります。", "장류수": "絶えず流れていく長い川。立ち止まらない挑戦精神と巨大な勢力を形成し海へ進む気象です。", "사중금": "砂の中に埋もれた砂金。長い時間磨かれ発見されるのを待つ貴く繊細な価値です。", "산하화": "山の麓で燃え上がる夕焼け/炎。ほのかでありながらも世界を美しく染める芸術的感覚が際立ちます。", "평지목": "平野に育った木。平坦な環境の中で安定して成長し、無難で健実な生活を追求します。", "벽상토": "家を支える壁の土。見かけは平凡ですが人々の安息処を支える見えない頼もしい協力者です。", "금박금": "仏像に塗る薄い金箔。華やかで荘厳な魅力で他人を引き立てる特殊で輝く才能です。", "복등화": "闇を照らす灯火。孤独で寂しい人々に希望を与える暖かく献身的な宗教的/哲学的気運です。", "천하수": "天から降る天の川/雨。万物を潤し命を与える清らかで高潔な魂と純粋さがあります。", "대역토": "広い荒野と駅馬の土。スケールが膨大で複数の地域を網羅する受容力と貿易/流通の気運を意味します。", "차천금": "女性を装飾する簪と腕輪。洗練された繊細な美的感覚と貴族的に華やかな品格を象徴します。", "상자목": "絹を織る蚕を飼う桑の木。他人のために有用な価値を創出し犠牲によって大きな業績を成し遂げます。", "대계수": "深い山に集まり流れる渓谷の水。清らかで冷たい知性で万物の渇きを癒す学者的気質があります。", "사중토": "砂と混ざった土。風雨に耐え、自分だけの堅固な基盤を築き上げる強靭で荒々しい粘り強さがあります。", "천상화": "天の真ん中に浮かぶ太陽。天下を公平に照らし万物を育む圧倒的なスケールと公明正大さを持っています。", "석류목": "秋に硬く熟したザクロの木。華やかさの中にぎっしり詰まった結実を抱き、財物と子孫の繁栄を象徴します。", "대해수": "全てを飲み込む巨大な海。底知れぬ深い知恵とすべての善悪を包み込む圧倒的な受容力があります。"
    },
    "zh-CN": {
        "해중금": "沉落深海的宝石。拥有不露锋芒的深厚内功与无限潜力。", "노중화": "炉中燃烧的火焰。在温暖受保护的环境中发挥隐忍的毅力与智慧。", "대림목": "郁郁葱葱的巨大森林。格局宏大，象征孕育无数生命的雄伟包容力。", "대림토": "郁郁葱葱的巨大森林(大林木)。格局宏大，象征孕育无数生命的雄伟包容力。", "노방토": "任人践踏的路边泥土。牺牲精神强，极具亲和力，能与大众打成一片。", "검봉금": "削铁如泥的名剑。拥有对不义零容忍的锐利决断力与强大的领袖气质。", "산두화": "山顶燃烧的火炬。光芒远照，具备指引众人的先驱者气质。", "간하수": "流淌于山谷的清澈溪流。拥有波澜不惊却生生不息的生命力与纯洁的灵魂。", "성두토": "构筑城墙的坚实泥土。象征抵御外敌的坚定责任感与不可动摇的原则。", "백랍금": "如蜡般凝固的软金。极具柔软性与变通力，能顺应环境磨练自身。", "백납금": "如蜡般凝固的软金。极具柔软性与变通力，能顺应环境磨练自身。", "양류목": "水边摇曳的杨柳。柔软灵活，深谙狂风亦折不断的处世之道。", "천중수": "涌自地下深处的泉水。拥有取之不尽的智慧与施惠于人的纯粹慈悲心。", "옥상토": "覆盖屋顶的瓦片/泥土。遮挡外界风雨保护众人，居高临下俯瞰世间。", "벽력화": "划破黑暗的雷电。拥有瞬间爆发的天才性与无人能及的独创性。", "송백목": "严冬依然常青的松柏。在任何考验中都绝不屈服，拥有严寒般坚贞的节操。", "장류수": "奔流不息的长河。拥有永不止步的挑战精神，形成浩大声势奔向大海的气象。", "사중금": "埋藏沙中的沙金。历经岁月打磨，等待被发掘的珍贵且细腻的价值。", "산하화": "山脚燃烧的晚霞/火焰。光芒柔和却能绝美地染红世界，极具艺术感。", "평지목": "生长于平原的树木。在平坦的环境中稳定成长，追求平安稳健的生活。", "벽상토": "支撑房屋的墙壁之土。看似平凡，却是默默支撑他人安息之地的坚实后盾。", "금박금": "为佛像镀上的薄金箔。以华丽庄严的魅力衬托他人，是特殊而耀眼的才能。", "복등화": "照亮黑暗的灯盏。为孤独寂寞之人带来希望，充满温暖与奉献的宗教/哲学气息。", "천하수": "天上降下的银河/雨水。拥有滋润万物、赋予生命的清纯高洁灵魂。", "대역토": "广阔的原野与驿马之土。格局庞大，象征跨越地域的包容力与贸易/流通的气运。", "차천금": "装饰女子的发簪与手镯。象征洗练细腻的审美与贵族般华丽的品格。", "상자목": "养蚕织绸的桑树。为他人创造实用价值，通过牺牲铸就伟大业绩。", "대계수": "深山汇聚的溪谷之水。以清冽的理智解除万物之渴，极具学者气质。", "사중토": "混杂沙石的泥土。经受风吹雨打，开辟属于自己坚固地盘的强悍毅力。", "천상화": "悬于天顶的太阳。拥有公平普照天下、孕育万物的压倒性格局与大公无私。", "석류목": "秋日结满硬实果实的石榴树。在华丽中孕育着丰硕的果实，象征财富与子孙繁盛。", "대해수": "吞噬一切的汪洋大海。拥有深不可测的智慧与包容所有善恶的压倒性度量。"
    },
    "zh-TW": {
        "해중금": "沉落深海的寶石。擁有不露鋒芒的深厚內功與無限潛力。", "노중화": "爐中燃燒的火焰。在溫暖受保護的環境中發揮隱忍的毅力與智慧。", "대림목": "鬱鬱蔥蔥的巨大森林。格局宏大，象徵孕育無數生命的雄偉包容力。", "대림토": "鬱鬱蔥蔥的巨大森林(大林木)。格局宏大，象徵孕育無數生命的雄偉包容力。", "노방토": "任人踐踏的路邊泥土。犧牲精神強，極具親和力，能與大眾打成一片。", "검봉금": "削鐵如泥的名劍。擁有對不義零容忍的銳利決斷力與強大的領袖氣質。", "산두화": "山頂燃燒的火炬。光芒遠照，具備指引眾人的先驅者氣質。", "간하수": "流淌於山谷的清澈溪流。擁有波瀾不驚卻生生不息的生命力與純潔的靈魂。", "성두토": "構築城牆的堅實泥土。象徵抵禦外敵的堅定責任感與不可動搖的原則。", "백랍금": "如蠟般凝固的軟金。極具柔軟性與變通力，能順應環境磨練自身。", "백납금": "如蠟般凝固的軟金。極具柔軟性與變通力，能順應環境磨練自身。", "양류목": "水邊搖曳的楊柳。柔軟靈活，深諳狂風亦折不斷的處世之道。", "천중수": "湧自地下深處的泉水。擁有取之不盡的智慧與施惠於人的純粹慈悲心。", "옥상토": "覆蓋屋頂的瓦片/泥土。遮擋外界風雨保護眾人，居高臨下俯瞰世間。", "벽력화": "劃破黑暗的雷電。擁有瞬間爆發的天才性與無人能及的獨創性。", "송백목": "嚴冬依然常青的松柏。在任何考驗中都絕不屈服，擁有嚴寒般堅貞的節操。", "장류수": "奔流不息的長河。擁有永不止步的挑戰精神，形成浩大聲勢奔向大海的氣象。", "사중금": "埋藏沙中的沙金。歷經歲月打磨，等待被發掘的珍貴且細膩的價值。", "산하화": "山腳燃燒的晚霞/火焰。光芒柔和卻能絕美地染紅世界，極具藝術感。", "평지목": "生長於平原的樹木。在平坦的環境中穩定成長，追求平安穩健的生活。", "벽상토": "支撐房屋的牆壁之土。看似平凡，卻是默默支撐他人安息之地的堅實後盾。", "금박금": "為佛像鍍上的薄金箔。以華麗莊嚴的魅力襯托他人，是特殊而耀眼的才能。", "복등화": "照亮黑暗的燈盞。為孤獨寂寞之人帶來希望，充滿溫暖與奉獻的宗教/哲學氣息。", "천하수": "天上降下的銀河/雨水。擁有滋潤萬物、賦予生命的清純高潔靈魂。", "대역토": "廣闊的原野與驛馬之土。格局龐大，象徵跨越地域的包容力與貿易/流通的氣運。", "차천금": "裝飾女子的髮簪與手鐲。象徵洗練細膩的審美與貴族般華麗的品格。", "상자목": "養蠶織綢的桑樹。為他人創造實用價值，通過犧牲鑄就偉大業績。", "대계수": "深山匯聚的溪谷之水。以清冽的理智解除萬物之渴，極具學者氣質。", "사중토": "混雜沙石的泥土。經受風吹雨打，開闢屬於自己堅固地盤的強悍毅力。", "천상화": "懸於天頂的太陽。擁有公平普照天下、孕育萬物的壓倒性格局與大公無私。", "석류목": "秋日結滿硬實果實的石榴樹。在華麗中孕育著豐碩的果實，象徵財富與子孫繁盛。", "대해수": "吞噬一切的汪洋大海。擁有深不可測的智慧與包容所有善惡的壓倒性度量。"
    }
}

GLOBAL_TERM_DB = {
    "甲": {"ja": "陽木。真っ直ぐ伸びる巨木、リーダーシップと始まりを意味します。", "zh-CN": "阳木。参天大树，象征领导力与开端。", "zh-TW": "陽木。參天大樹，象徵領導力與開端。"},
    "乙": {"ja": "陰木。粘り強い草花、柔軟性と環境適応力を意味します。", "zh-CN": "阴木。生命力顽强的花草，象征柔软与环境适应力。", "zh-TW": "陰木。生命力頑強的花草，象徵柔軟與環境適應力。"},
    "丙": {"ja": "陽火。世界を照らす太陽、情熱と華やかさを意味します。", "zh-CN": "阳火。普照世界的太阳，象征热情与华丽。", "zh-TW": "陽火。普照世界的太陽，象徵熱情與華麗。"},
    "丁": {"ja": "陰火。闇を照らす灯火、温かさと鋭い直感を意味します。", "zh-CN": "阴火。照亮黑暗的灯火，象征温暖与直觉。", "zh-TW": "陰火。照亮黑暗的燈火，象徵溫暖與直覺。"},
    "戊": {"ja": "陽土。万物を抱く巨大な山、包容力と重厚さを意味します。", "zh-CN": "阳土。包容万物的大山，象征包容与稳重。", "zh-TW": "陽土。包容萬物的大山，象徵包容與穩重。"},
    "己": {"ja": "陰土。生命を育む肥沃な田畑、育成と実用性を意味します。", "zh-CN": "阴土。孕育生命的田地，象征培养与实用。", "zh-TW": "陰土。孕育生命的田地，象徵培養與實用。"},
    "庚": {"ja": "陽金。硬く鋭い岩や鉄、決断力と変革を意味します。", "zh-CN": "阳金。坚硬锐利的铁石，象征决断力与变革。", "zh-TW": "陽金。堅硬銳利的鐵石，象徵決斷力與變革。"},
    "辛": {"ja": "陰金。精巧な宝石、繊細さと完璧主義を意味します。", "zh-CN": "阴金。精巧的宝石，象征细腻与完美主义。", "zh-TW": "陰金。精巧的寶石，象徵細膩與完美主義。"},
    "壬": {"ja": "陽水。全てを飲み込む巨大な海、深い知恵とスケールを意味します。", "zh-CN": "阳水。浩瀚的海洋，象征深邃的智慧与格局。", "zh-TW": "陽水。浩瀚的海洋，象徵深邃的智慧與格局。"},
    "癸": {"ja": "陰水。大地を潤す雨や泉、情報力と生命力を意味します。", "zh-CN": "阴水。滋润大地的雨露，象征信息力与生命力。", "zh-TW": "陰水。滋潤大地的雨露，象徵資訊力與生命力。"},
    "子": {"ja": "真冬の水気。知恵と秘密、種子を象徴します。", "zh-CN": "严冬之水。象征智慧、秘密与繁衍的种子。", "zh-TW": "嚴冬之水。象徵智慧、秘密與繁衍的種子。"},
    "丑": {"ja": "凍りついた土。忍耐と準備、大器晩成を象徴します。", "zh-CN": "冰封之土。象征忍耐、准备与大器晚成。", "zh-TW": "冰封之土。象徵忍耐、準備與大器晚成。"},
    "寅": {"ja": "初春の木気。躍動するエネルギーと権力、始まりを象徴します。", "zh-CN": "初春之木。象征跃动的能量、权力与开端。", "zh-TW": "初春之木。象徵躍動的能量、權力與開端。"},
    "卯": {"ja": "春真っ盛りの木気。純粋な生命力と芸術性、企画力を象徴します。", "zh-CN": "仲春之木。象征纯粹的生命力、艺术与企划力。", "zh-TW": "仲春之木。象徵純粹的生命力、藝術與企劃力。"},
    "辰": {"ja": "春を終える土。理想とプライド、変化に富んだ才能を象徴します。", "zh-CN": "晚春之土。象征理想、自尊与多变的才能。", "zh-TW": "晚春之土。象徵理想、自尊與多變的才能。"},
    "巳": {"ja": "初夏の火気。燃え上がる情熱と執念、鋭い直感を象徴します。", "zh-CN": "初夏之火。象征燃烧的热情、执着与锐利的直觉。", "zh-TW": "初夏之火。象徵燃燒的熱情、執著與銳利的直覺。"},
    "午": {"ja": "真夏の火気。公明正大と華やかさ、強力な推進力を象徴します。", "zh-CN": "盛夏之火。象征公明正大、华丽与强大的推进力。", "zh-TW": "盛夏之火。象徵公明正大、華麗與強大的推進力。"},
    "未": {"ja": "夏を終える土。熱気を抱いた乾燥した土、職人精神と犠牲を象徴します。", "zh-CN": "晚夏之土。内含热气的燥土，象征工匠精神与牺牲。", "zh-TW": "晚夏之土。內含熱氣的燥土，象徵工匠精神與犧牲。"},
    "申": {"ja": "初秋の金気。結実の始まり、多才多能と決断力を象徴します。", "zh-CN": "初秋之金。结实的开端，象征多才多艺与决断力。", "zh-TW": "初秋之金。結實的開端，象徵多才多藝與決斷力。"},
    "酉": {"ja": "秋真っ盛りの金気。確実な結果と鋭さ、完璧主義を象徴します。", "zh-CN": "仲秋之金。确切的结果与锐利，象征完美主义。", "zh-TW": "仲秋之金。確切的結果與銳利，象徵完美主義。"},
    "戌": {"ja": "秋を終える土。荒涼とした土、守護と忠誠、名誉を象徴します。", "zh-CN": "晚秋之土。苍凉之土，象征守护、忠诚与名誉。", "zh-TW": "晚秋之土。蒼涼之土，象徵守護、忠誠與名譽。"},
    "亥": {"ja": "初冬の水気。全てを受け入れる海、蓄積と大きなスケールを象徴します。", "zh-CN": "初冬之水。包容一切的海洋，象征积累与宏大格局。", "zh-TW": "初冬之水。包容一切的海洋，象徵積累與宏大格局。"},
    "비견": {"ja": "【自立と競争】 自分と同じ気運。独立心、競争、同僚を意味します。", "zh-CN": "【自立与竞争】 与自身相同的气运。象征独立、竞争与同僚。", "zh-TW": "【自立與競爭】 與自身相同的氣運。象徵獨立、競爭與同僚。"},
    "겁재": {"ja": "【奪取と闘争】 財を奪う気運。強力な勝負欲、野心、支出を意味します。", "zh-CN": "【夺取与斗争】 夺取财富的气运。象征强烈的胜负欲、野心与支出。", "zh-TW": "【奪取與鬥爭】 奪取財富的氣運。象徵強烈的勝負慾、野心與支出。"},
    "식신": {"ja": "【探求と表現】 自分が生み出す気運。専門性、研究、食福、寿命を意味します。", "zh-CN": "【探究与表达】 自身生出的气运。象征专业性、研究、食禄与寿命。", "zh-TW": "【探究與表達】 自身生出的氣運。象徵專業性、研究、食祿與壽命。"},
    "상관": {"ja": "【破格と芸術】 枠を壊す気運。弁舌、芸術性、反抗心、聡明さを意味します。", "zh-CN": "【破格与艺术】 打破常规的气运。象征口才、艺术性、反抗与聪颖。", "zh-TW": "【破格與藝術】 打破常規的氣運。象徵口才、藝術性、反抗與聰穎。"},
    "편재": {"ja": "【流動と事業】 偏った財物。事業運、投資、空間認識力、支配欲を意味します。", "zh-CN": "【流动与事业】 偏向的财富。象征事业运、投资、空间感知与支配欲。", "zh-TW": "【流動與事業】 偏向的財富。象徵事業運、投資、空間感知與支配慾。"},
    "정재": {"ja": "【安定と蓄積】 正当な財物。固定収入、誠実さ、正確な計算能力を意味します。", "zh-CN": "【稳定与积累】 正当的财富。象征固定收入、诚实与精确的计算能力。", "zh-TW": "【穩定與積累】 正當的財富。象徵固定收入、誠實與精確的計算能力。"},
    "편관": {"ja": "【権力と克己】 自分を厳しく統制する気運。権力、カリスマ、忍耐、名誉を意味します。", "zh-CN": "【权力与克己】 严厉控制自身的气运。象征权力、领袖气质、忍耐与名誉。", "zh-TW": "【權力與克己】 嚴厲控制自身的氣運。象徵權力、領袖氣質、忍耐與名譽。"},
    "정관": {"ja": "【規律と合理】 正当な統制。合理的な原則、法度、正しい職場、安定を意味します。", "zh-CN": "【规律与合理】 正当的控制。象征合理原则、法度、稳定的职业与安稳。", "zh-TW": "【規律與合理】 正當的控制。象徵合理原則、法度、穩定的職業與安穩。"},
    "편인": {"ja": "【直感と偏心】 偏った受容。鋭い直感力、特殊学問、疑い、孤独を意味します。", "zh-CN": "【直觉与偏心】 偏向的吸收。象征敏锐直觉、特殊学问、猜忌与孤独。", "zh-TW": "【直覺與偏心】 偏向的吸收。象徵敏銳直覺、特殊學問、猜忌與孤獨。"},
    "정인": {"ja": "【知恵と包容】 正当な受容。学問、道徳心、母親の愛、資格、文書を意味します。", "zh-CN": "【智慧与包容】 正当的吸收。象征学问、道德、母爱、资格与文书。", "zh-TW": "【智慧與包容】 正當的吸收。象徵學問、道德、母愛、資格與文書。"},
    "공망": {"ja": "【空亡】 空しく満たされない気運。その柱の長所が減少し、虚しさを感じやすいです。", "zh-CN": "【空亡】 空虚不圆满的气运。该柱的优点减弱，容易感到匮乏。", "zh-TW": "【空亡】 空虛不圓滿的氣運。該柱的優點減弱，容易感到匱乏。"}
}

FAQ_DB = {
    "ko": [
        {"q": "대운수 수동 지정은 언제 사용하는 기능인가요?", "a": "명리학에서 대운(10년 주기의 운)이 바뀌는 나이는 태어난 날과 절기(節氣)의 거리를 계산하여 도출됩니다. 하지만 절기와 절기의 경계선(교운기)에 태어난 경우, 학파나 간명자의 관점에 따라 대운수를 1~2년 정도 당기거나 늦춰서 해석해야 할 때가 있습니다. 이 기능은 정해진 천문학적 대운수 대신, 스스로의 체감 운기에 맞춰 대운수를 강제로 보정할 수 있게 하는 상위 1% 전문가용 옵션입니다. 미입력 시 천문학 데이터에 기반해 자동으로 연산됩니다."},
        {"q": "고법(古法) 둔월법이란 무엇인가요?", "a": "현대 사주명리학(신법)은 무조건 태양의 궤도인 '24절기(입춘, 경칩 등)'를 기준으로 월주(태어난 달의 기둥)를 세웁니다. 반면, 과거의 고법(古法) 명리나 일부 특수 학파에서는 절기를 무시하고 오직 '순수 음력 달(月)'을 기준으로 월주를 세우는 방식을 사용하기도 합니다. '고법 둔월법'을 체크하고 음력 월을 지정하시면, 절기와 상관없이 강제로 해당 음력 월의 기운으로 사주 원국을 덮어씌워 간명하는 심층 비교 분석이 가능해집니다."},
        {"q": "마스터 엔진의 파트너 궁합은 일반 궁합과 무엇이 다른가요?", "a": "본 시스템의 궁합은 단순한 오행의 개수나 띠(연지)만 맞추는 가벼운 궁합이 아닙니다. 다음 3가지 핵심 엔진을 크로스체크하여 인연의 밑바닥까지 팩트폭행합니다.\n\n1. 일지(日支) 속궁합: 부부의 침실이자 내면을 상징하는 일지의 글자를 대조하여 육합, 삼합의 완벽한 융합부터 원진, 귀문, 충의 애증과 파국까지 적나라하게 분석합니다.\n2. 구궁 팔괘: 남녀의 타고난 본명성을 바탕으로, 부부 사이의 권력 구조(남극녀, 여극남 등)와 발현 타이밍을 도출합니다.\n3. 삼원갑자: 두 영혼이 속한 우주적 시대 배경을 대조하여 영혼의 파장이 근본적으로 닿아 있는지를 판별합니다."}
    ],
    "ja": [
        {"q": "大運数の手動指定はいつ使用する機能ですか？", "a": "四柱推命において大運（10年周期の運）が変わる年齢は、生まれた日と節気の距離を計算して導き出されます。しかし、節気と節気の境界線（交運期）に生まれた場合、学派や鑑定者の観点によって大運数を1〜2年程度前後にずらして解釈すべき時があります。この機能は、定められた天文学的な大運数の代わりに、自身の体感する運気に合わせて大運数を強制的に補正できる上位1%の専門家向けオプションです。未入力の場合は天文学データに基づいて自動演算されます。"},
        {"q": "古法遁月法とは何ですか？", "a": "現代の四柱推命（新法）は無条件に太陽の軌道である「二十四節気」を基準に月柱（生まれた月の柱）を立てます。一方、過去の古法推命や一部の特殊学派では、節気を無視して純粋な「陰暦の月」のみを基準に月柱を立てる方式を使用することがあります。「古法遁月法」にチェックを入れ陰暦月を指定すると、節気に関係なく強制的に該当する陰暦月の気運で四柱原局を上書きし、深層比較分析が可能になります。"},
        {"q": "マスターエンジンのパートナー相性は一般的な相性と何が違うのですか？", "a": "本システムの相性は、単純な五行の数や干支だけを合わせる軽い相性ではありません。次の3つの核心エンジンをクロスチェックし、縁の底辺まで赤裸々に分析します。\n\n1. 日支の裏相性：夫婦の寝室と内面を象徴する日支の文字を照らし合わせ、六合・三合の完璧な融合から、怨嗔・鬼門・冲の愛憎と破局まで赤裸々に分析します。\n2. 九宮八卦：男女の生まれ持った本命星に基づき、夫婦間の権力構造（男剋女、女剋男など）と発現のタイミングを導き出します。\n3. 三元甲子：二つの魂が属する宇宙的な時代背景を照らし合わせ、魂の波長が根本的に触れ合っているかを判別します。"}
    ],
    "zh-CN": [
        {"q": "大运数手动指定是什么时候使用的功能？", "a": "在命理学中，大运（10年周期的运势）交接的年龄是根据出生日与节气的距离计算得出的。但若是出生在节气交接边缘（交运期），根据学派或命理师的观点，有时需要将大运数提前或推后1~2年进行解析。该功能是专为前1%专业人士提供的选项，允许不使用天文计算的大运数，而是根据自身体感的运势强制校正大运数。若不填写，则默认基于天文数据自动计算。"},
        {"q": "古法遁月法是什么？", "a": "现代四柱命理学（新法）无条件以太阳轨道的“二十四节气”为基准来确立月柱。相反，过去的古法命理或部分特殊学派，有时会忽略节气，仅以“纯农历月份”为基准来确立月柱。勾选“古法遁月法”并指定农历月份，系统将无视节气，强制以该农历月的力量覆盖命局，从而实现深度的对比分析。"},
        {"q": "Master Engine的伴侣合婚与普通合婚有什么区别？", "a": "本系统的合婚绝非仅看五行个数或生肖的简单合婚。我们将交叉比对以下3大核心引擎，将缘分的本质赤裸裸地呈现出来：\n\n1. 日支内合（床笫之合）：比对象征夫妻卧室与内心的日支，从六合、三合的完美交融，到怨嗔、鬼门、冲的爱恨与破局，进行直白的剖析。\n2. 九宫八卦：基于男女先天的本命星，推导出夫妻间的权力结构（如男克女、女克男等）及吉凶爆发的时机。\n3. 三元甲子：对比两个灵魂所属的宇宙时代背景，判断灵魂的磁场是否从根本上产生共鸣。"}
    ],
    "zh-TW": [
        {"q": "大運數手動指定是什麼時候使用的功能？", "a": "在命理學中，大運（10年週期的運勢）交接的年齡是根據出生日與節氣的距離計算得出的。但若是出生在節氣交接邊緣（交運期），根據學派或命理師的觀點，有時需要將大運數提前或推後1~2年進行解析。該功能是專為前1%專業人士提供的選項，允許不使用天文計算的大運數，而是根據自身體感的運勢強制校正大運數。若不填寫，則預設基於天文數據自動計算。"},
        {"q": "古法遁月法是什麼？", "a": "現代四柱命理學（新法）無條件以太陽軌道的「二十四節氣」為基準來確立月柱。相反，過去的古法命理或部分特殊學派，有時會忽略節氣，僅以「純農曆月份」為基準來確立月柱。勾選「古法遁月法」並指定農曆月份，系統將無視節氣，強制以該農曆月的力量覆蓋命局，從而實現深度的對比分析。"},
        {"q": "Master Engine的伴侶合婚與普通合婚有什麼區別？", "a": "本系統的合婚絕非僅看五行個數或生肖的簡單合婚。我們將交叉比對以下3大核心引擎，將緣分的本質赤裸裸地呈現出來：\n\n1. 日支內合（床笫之合）：比對象徵夫妻臥室與內心的日支，從六合、三合的完美交融，到怨嗔、鬼門、衝的愛恨與破局，進行直白的剖析。\n2. 九宮八卦：基於男女先天的本命星，推導出夫妻間的權力結構（如男剋女、女剋男等）及吉凶爆發的時機。\n3. 三元甲子：對比兩個靈魂所屬的宇宙時代背景，判斷靈魂的磁場是否從根本上產生共鳴。"}
    ]
}

def build_full_response(dt_kst, astro_res, gender, daewun_num=1, partner_info=None, apply_trad=False, lunar_m=None, unknown_time=False, lang="ko"):
    bazi_raw = astro_res.get("bazi", {})
    
    y_stem, y_branch = bazi_raw["year_pillar"][0], bazi_raw["year_pillar"][1]
    m_stem, m_branch = bazi_raw["month_pillar"][0], bazi_raw["month_pillar"][1]
    d_stem, d_branch = bazi_raw["day_pillar"][0], bazi_raw["day_pillar"][1]
    
    if unknown_time:
        h_stem, h_branch = "-", "-"
    else:
        h_stem, h_branch = bazi_raw["hour_pillar"][0], bazi_raw["hour_pillar"][1]
    
    if apply_trad and lunar_m:
        trad_m_stem, trad_m_branch = mech.get_traditional_month_pillar(y_stem, lunar_m)
        if trad_m_stem and trad_m_branch: m_stem, m_branch = trad_m_stem, trad_m_branch

    day_master = d_stem

    def get_pillar(stem, branch):
        if stem == "-" or branch == "-": return {"stem": "-", "branch": "-", "stem_tg": "-", "branch_tg": "-", "napeum": "-"}
        return {"stem": stem, "branch": branch, "stem_tg": mech.get_ten_god(day_master, stem), "branch_tg": mech.get_ten_god(day_master, branch), "napeum": mech.get_napeum(stem, branch)}

    bazi = {"year": get_pillar(y_stem, y_branch), "month": get_pillar(m_stem, m_branch), "day": get_pillar(d_stem, d_branch), "hour": get_pillar(h_stem, h_branch)}

    hidden_stems = {"year": mech.get_hidden_stems(y_branch), "month": mech.get_hidden_stems(m_branch), "day": mech.get_hidden_stems(d_branch), "hour": {"initial": ["-"], "middle": ["-"], "main": ["-"]} if unknown_time else mech.get_hidden_stems(h_branch)}
    
    gongmang = mech.get_gongmang(d_stem, d_branch)
    valid_stems = [s for s in [y_stem, m_stem, d_stem, h_stem] if s != "-"]
    valid_branches = [b for b in [y_branch, m_branch, d_branch, h_branch] if b != "-"]
    
    elements_dist = mech.get_five_elements_distribution(valid_stems, valid_branches)
    
    tonggeun_branches = {"year": y_branch, "month": m_branch, "day": d_branch}
    if not unknown_time: tonggeun_branches["hour"] = h_branch
    tonggeun = mech.check_tonggeun(day_master, tonggeun_branches)

    geokguk = yong.determine_geokguk(bazi, hidden_stems)
    strength = yong.determine_strength(bazi)
    yongshin_data = yong.determine_yongshin(bazi, strength)

    career = prac.analyze_career(geokguk, yongshin_data)
    health_raw = prac.analyze_health(elements_dist)
    
    elements_imbalance = []
    for h in health_raw:
        if h["element"] != "종합":
            elements_imbalance.append({"element": h["element"], "type": h["status"].split(" ")[0], "count": elements_dist.get(h["element"], 0), "desc": h["advice"]})

    special_stars = dyn.scan_special_stars({"year": y_stem, "month": m_stem, "day": d_stem, "hour": h_stem}, {"year": y_branch, "month": m_branch, "day": d_branch, "hour": h_branch})
    disasters = dyn.scan_disasters(valid_branches)

    daewun_raw = mech.get_daewun_sequence(gender, y_stem, m_stem, m_branch, int(daewun_num), 10)
    sewun_raw = mech.get_sewun_sequence(datetime.now().year - 4, 10)

    for dw in daewun_raw["timeline"]:
        dw["stem_tg"] = mech.get_ten_god(day_master, dw["stem"])
        dw["branch_tg"] = mech.get_ten_god(day_master, dw["branch"])
    
    for sw in sewun_raw:
        sw["stem_tg"] = mech.get_ten_god(day_master, sw["stem"])
        sw["branch_tg"] = mech.get_ten_god(day_master, sw["branch"])

    now_astro = astro.calculate_bazi(datetime.now(), gender, 127.0, True, True)
    now_y, now_y_b = now_astro["bazi"]["year_pillar"][0], now_astro["bazi"]["year_pillar"][1]
    now_m, now_m_b = now_astro["bazi"]["month_pillar"][0], now_astro["bazi"]["month_pillar"][1]
    now_d, now_d_b = now_astro["bazi"]["day_pillar"][0], now_astro["bazi"]["day_pillar"][1]

    unse_data = {
        "year": {**unse.analyze_sewun(bazi, now_y_b, mech.get_ten_god(day_master, now_y_b), yongshin_data), "stem": now_y, "branch": now_y_b},
        "month": {"month_num": datetime.now().month, "stem": now_m, "branch": now_m_b, "data": unse.analyze_wolgeon(bazi, now_m_b, mech.get_ten_god(day_master, now_m_b), yongshin_data)},
        "day": {"day_num": datetime.now().day, "stem": now_d, "branch": now_d_b, "data": unse.analyze_iljin(bazi, now_d_b, mech.get_ten_god(day_master, now_d_b), yongshin_data)}
    }

    gunghap_data = None
    if partner_info:
        p_dt = partner_info["dt"]
        p_gender = partner_info["gender"]
        p_lon = partner_info["longitude"]
        p_unk_time = partner_info["unknown_time"]
        
        my_year = dt_kst.year
        p_year = p_dt.year
        
        p_apply_true_solar = False if p_unk_time else True
        p_astro = astro.calculate_bazi(p_dt, p_gender, p_lon, p_apply_true_solar, True)
        p_day_branch = p_astro["bazi"]["day_pillar"][1]

        my_star = ghap.get_bonmyeongseong(my_year, gender)
        p_star = ghap.get_bonmyeongseong(p_year, p_gender)
        
        gunghap_data = {
            "my_samwon": ghap.get_samwon_gapja(my_year, lang), "my_star": my_star,
            "partner_samwon": ghap.get_samwon_gapja(p_year, lang), "partner_star": p_star,
            "gugung": ghap.get_gugung_compatibility(my_star["number"], gender, p_star["number"], p_gender, lang),
            "inner": ghap.get_inner_compatibility(d_branch, p_day_branch, lang)
        }

    classical_stars_branches = {"year": y_branch, "month": m_branch, "day": d_branch}
    if not unknown_time: classical_stars_branches["hour"] = h_branch
        
    classical_stars = clas.get_four_pillars_stars(classical_stars_branches, lang)
    classical_reading = clas.generate_classical_reading(bazi, disasters, yongshin_data, gender, lang)

    metadata = {}
    terms_to_fetch = set(["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "비견", "겁재", "식신", "상관", "편재", "정재", "편관", "정관", "편인", "정인", "공망"])
    for p in bazi.values():
        terms_to_fetch.add(p['stem_tg'])
        terms_to_fetch.add(p['branch_tg'])
        
    for term in terms_to_fetch:
        if term and term != "일간" and term != "-": 
            original_meta = mech.get_metadata(term)
            
            # 🚨 [치명적 버그 수정 1] 강제 딕셔너리화 안전장치
            if isinstance(original_meta, str):
                meta = {"hanja": "", "meaning": original_meta}
            elif isinstance(original_meta, dict):
                meta = copy.deepcopy(original_meta)
            else:
                meta = {"hanja": "", "meaning": ""}
                
            lookup_key = term if term in GLOBAL_TERM_DB else meta.get("hanja", "")
            if lookup_key in GLOBAL_TERM_DB and lang != "ko":
                meta["meaning"] = GLOBAL_TERM_DB[lookup_key].get(lang, meta.get("meaning", ""))
            metadata[term] = meta

    ui_map = {
        "ko": {"y": "연주 (초년)", "m": "월주 (청년)", "d": "일주 (중년)", "h": "시주 (말년)", "u_time": "시간 모름 (보정 생략)", "u_desc": "납음오행 정보가 없습니다.", "b1": "초년과 조상궁에 이 웅장한 파동이 깃들어 있습니다.", "b2": "청년기와 사회적 성취(직업)에 이 파동이 핵심적으로 작용합니다.", "b3": "중년기와 본인/배우자의 내면 깊은 곳에 이 파동이 흐르고 있습니다.", "b4": "말년과 자식궁, 그리고 남모르는 비밀스러운 영혼의 파동입니다."},
        "ja": {"y": "年柱 (初年)", "m": "月柱 (青年)", "d": "日柱 (中年)", "h": "時柱 (晩年)", "u_time": "時間不明 (補正省略)", "u_desc": "納音五行の情報がありません。", "b1": "初年と先祖宮にこの壮大な波動が宿っています。", "b2": "青年期と社会的成就（職業）にこの波動が核心的に作用します。", "b3": "中年期と本人/配偶者の内面深くにこの波動が流れています。", "b4": "晩年と子孫宮、そして人知れぬ秘密の魂の波動です。"},
        "zh-CN": {"y": "年柱 (早年)", "m": "月柱 (青年)", "d": "日柱 (中年)", "h": "时柱 (晚年)", "u_time": "未知时间 (省略校正)", "u_desc": "无纳音五行信息。", "b1": "早年与祖上宫蕴含着这雄伟的波动。", "b2": "青年期与社会成就(职业)中，此波动起着核心作用。", "b3": "中年期与本人/配偶的内心深处流淌着这股波动。", "b4": "晚年与子孙宫，以及不为人知的隐秘灵魂之波动。"},
        "zh-TW": {"y": "年柱 (早年)", "m": "月柱 (青年)", "d": "日柱 (中年)", "h": "時柱 (晚年)", "u_time": "未知時間 (省略校正)", "u_desc": "無納音五行資訊。", "b1": "早年與祖上宮蘊含著這雄偉的波動。", "b2": "青年期與社會成就(職業)中，此波動起著核心作用。", "b3": "中年期與本人/配偶的內心深處流淌著這股波動。", "b4": "晚年與子孫宮，以及不為人知的隱秘靈魂之波動。"}
    }
    lm = ui_map.get(lang, ui_map["ko"])
    l_napeum = NAPEUM_RICH_DESC.get(lang, NAPEUM_RICH_DESC["ko"])

    def get_napeum_desc(pillar_type, napeum_full):
        if not napeum_full or napeum_full == "-" or napeum_full == "알수없음": return lm["u_desc"]
        core_name = napeum_full[:3]
        base_desc = l_napeum.get(core_name, "-")
        if pillar_type == "year": return f"{base_desc} {lm['b1']}"
        elif pillar_type == "month": return f"{base_desc} {lm['b2']}"
        elif pillar_type == "day": return f"{base_desc} {lm['b3']}"
        else: return f"{base_desc} {lm['b4']}"

    napeum_reading = [
        {"pillar": lm["y"], "full": bazi["year"]["napeum"], "desc": get_napeum_desc("year", bazi["year"]["napeum"])},
        {"pillar": lm["m"], "full": bazi["month"]["napeum"], "desc": get_napeum_desc("month", bazi["month"]["napeum"])},
        {"pillar": lm["d"], "full": bazi["day"]["napeum"], "desc": get_napeum_desc("day", bazi["day"]["napeum"])},
    ]
    if not unknown_time:
        napeum_reading.append({"pillar": lm["h"], "full": bazi["hour"]["napeum"], "desc": get_napeum_desc("hour", bazi["hour"]["napeum"])})

    return {
        "status": "success",
        "origin_time": astro_res["origin_time"],
        "corrected_time": lm["u_time"] if unknown_time else astro_res["corrected_time"],
        "gender": "Male" if gender == "M" else "Female",
        "applied_traditional": apply_trad,
        "bazi": bazi,
        "mechanics": {"hidden_stems": hidden_stems, "gongmang": gongmang, "elements_dist": elements_dist, "tonggeun": tonggeun, "metadata": metadata},
        "yongshin": {"geokguk": geokguk, "strength": strength, "yongshin": yongshin_data},
        "practical": {"career": career, "health": health_raw},
        "elements_imbalance": elements_imbalance,
        "dynamics": {"special_stars": special_stars, "disasters": disasters},
        "unse": unse_data,
        "napeum_reading": napeum_reading,
        "timeline": {"daewun": daewun_raw, "sewun": sewun_raw},
        "gunghap": gunghap_data,
        "classical": {"stars": classical_stars, "reading": classical_reading}
    }

@app.get("/api/dictionary")
def dictionary_endpoint(q: str = "", lang: str = "ko"):
    results = dict_db.search(q)
    # 🚨 [치명적 버그 수정 2] 사전 결과가 리스트 형식이 아닐 때 즉시 반환하여 에러 방어
    if lang == "ko" or not isinstance(results, list):
        return results
    
    translated = []
    for r in results:
        t_term = r.get("term", "")
        t_hanja = r.get("hanja", "")
        t_meaning = r.get("meaning", "")
        t_category = r.get("category", "")
        
        cat_map = {
            "ja": {"천간":"天干", "지지":"地支", "십성":"十星", "신살":"神殺", "기타":"その他"},
            "zh-CN": {"천간":"天干", "지지":"地支", "십성":"十神", "신살":"神煞", "기타":"其他"},
            "zh-TW": {"천간":"天干", "지지":"地支", "십성":"十神", "신살":"神煞", "기타":"其他"}
        }
        if lang in cat_map:
            t_category = cat_map[lang].get(t_category, t_category)
            
        lookup_key = t_term if t_term in GLOBAL_TERM_DB else t_hanja
        if lookup_key in GLOBAL_TERM_DB:
            t_meaning = GLOBAL_TERM_DB[lookup_key].get(lang, t_meaning)
            
        translated.append({"term": t_term, "hanja": t_hanja, "category": t_category, "meaning": t_meaning})
        
    return translated

@app.get("/api/faq")
def faq_endpoint(lang: str = "ko"):
    return FAQ_DB.get(lang, FAQ_DB["ko"])

@app.post("/api/bazi")
async def bazi_endpoint(request: Request):
    try:
        user_data = await request.json()
        
        datetime_str = user_data.get("datetime_str")
        calendar_type = user_data.get("calendar_type", "solar")
        gender = user_data.get("gender")
        
        longitude = float(user_data.get("longitude", 127.0))
        timezone = int(user_data.get("timezone", 9)) 
        unknown_time = user_data.get("unknown_time", False)
        
        lang = user_data.get("language", "ko")
        
        apply_true_solar = False if unknown_time else user_data.get("apply_true_solar", True)
        apply_yaja = user_data.get("apply_yaja", True)
        daewun_num = user_data.get("daewun_num", 1)
        apply_trad = user_data.get("apply_traditional_lunar", False)
        lunar_m = user_data.get("lunar_month")
        
        dt_input = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        
        if timezone != 9:
            dt_input = dt_input - timedelta(hours=timezone) + timedelta(hours=9)
        
        if calendar_type in ["lunar", "lunar_leap"]:
            cal = KoreanLunarCalendar()
            is_leap = (calendar_type == "lunar_leap")
            if cal.setLunarDate(dt_input.year, dt_input.month, dt_input.day, is_leap):
                dt_kst = datetime(cal.solarYear, cal.solarMonth, cal.solarDay, dt_input.hour, dt_input.minute)
            else:
                return {"status": "error", "message": "Invalid Lunar Date."}
        else:
            dt_kst = dt_input
            
        astro_res = astro.calculate_bazi(dt_kst, gender, longitude, apply_true_solar, apply_yaja)
        
        partner_info = None
        p_dt_str = user_data.get("partner_datetime_str")
        
        if p_dt_str:
            p_calendar_type = user_data.get("partner_calendar_type", "solar")
            p_gender = user_data.get("partner_gender")
            p_lon = float(user_data.get("partner_longitude", 127.0))
            p_tz = int(user_data.get("partner_timezone", 9))
            p_unk_time = user_data.get("partner_unknown_time", False)
            
            p_dt_input = datetime.strptime(p_dt_str, "%Y-%m-%d %H:%M")
            if p_tz != 9:
                p_dt_input = p_dt_input - timedelta(hours=p_tz) + timedelta(hours=9)
                
            if p_calendar_type in ["lunar", "lunar_leap"]:
                p_cal = KoreanLunarCalendar()
                p_is_leap = (p_calendar_type == "lunar_leap")
                if p_cal.setLunarDate(p_dt_input.year, p_dt_input.month, p_dt_input.day, p_is_leap):
                    partner_dt = datetime(p_cal.solarYear, p_cal.solarMonth, p_cal.solarDay, p_dt_input.hour, p_dt_input.minute)
                else:
                    partner_dt = p_dt_input
            else:
                partner_dt = p_dt_input
                
            partner_info = {"dt": partner_dt, "gender": p_gender, "longitude": p_lon, "unknown_time": p_unk_time}

        final_result = build_full_response(dt_kst, astro_res, gender, daewun_num, partner_info, apply_trad, lunar_m, unknown_time, lang)

        return final_result

    except Exception as e:
        print("Backend Error:", str(e), flush=True)
        return {"status": "error", "message": str(e)}

@app.get("/")
def read_root():
    return {"message": "마스터 엔진 가동 중 (4개국어 듀얼 언어팩 및 글로벌 타임존 완벽 지원)"}