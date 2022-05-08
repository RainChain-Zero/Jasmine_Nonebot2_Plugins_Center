from random import sample, shuffle
from pathlib import Path 
import os
import nonebot

global_config = nonebot.get_driver().config
if not hasattr(global_config, "tarot_path"):
    TAROT_PATH = os.path.join(os.path.dirname(__file__), "resource")
else:
    TAROT_PATH = global_config.tarot_path

class Cards() :
    def __init__(self, num: int):
        '''
            为了模拟抽牌过程，所以会将卡组打乱，然后从小到大进行抽牌
            所以稍微牺牲点性能没问题的对吧！
        '''
        names = list(cards.keys())
        shuffle(names)
        self.selected = [names[card_id] for card_id in sample(range(0,100), num)]
        self.showed = 0

    # 揭示牌（玄学当然要有仪式感！）
    def reveal(self):
        card_key = self.selected[self.showed]               # 牌名
        card_meaning = cards[card_key]                      # 含义
        image_file = TAROT_PATH+'/' +card_key + ".jpg" # 图片路径
        self.showed += 1
        return card_key, card_meaning, image_file


cards = {
    "圣杯1": "预示着一场新恋情和新友情的开始。\n在感情刚开始时，爱与关怀常满溢，要懂得慷慨回报对方，珍惜这份福气。若求问者这份感情已维持很久了，出现圣杯首牌，要好好看看四周的牌，小心外遇迹象。如果两个人刚刚经历了吵架，圣杯首牌意味着化解纠纷重新开始。\n若是在无关感情的推测中，出现圣杯首牌，表示这个局势需要爱来耐心化解。",
    "圣杯10": "家庭幸福，平凡的生活。或许能得到预料之外的成功与好消息。\n也可能代表一切美好都是自己的空想，会像彩虹一样消失。",
    "圣杯2": "经常与爱情产生强烈关联，此牌比较近似刚刚开始恋爱、甚至还没有明确恋爱关系的状态，男女相敬如宾，平等对待对方，不做强求。\n不只局限男女情感，也可以涉及友谊，以及任何人际关系，而这种关系往往是和谐对等，愉快的",
    "圣杯3": "通常表示以感情作为关联的团体，另外，也代表一种欢庆的场合，包括宴会、婚礼等。其丰收的含义通常代表事情有了好的结果。\n当然，有时也相反，代表团体内各藏心机，婚姻中出现第三者等。",
    "圣杯4": "表示一段消极、无聊、疲惫、退缩的时光。当事人缺乏动力，对一切事物漠不关心，不想参加社交。\n圣杯四有时也代表新机会的降临，这种情况往往因当事人缺少热情而错失机会。",
    "圣杯5": "代表的事一种悲伤痛苦的处境，情绪的混乱和缺少动力。同时，也预示着另类生活的开始。",
    "圣杯6": "除代表对往事的回忆和思乡、照顾之外，有时也提醒当事者，要像男孩一样慷慨大方，乐于付出，放下一切仇恨和不悦情绪。\n圣杯六也可以代表正在意味着一种严格有序的体系所打破，会释放出巨大的力量，会有众多的选择。",
    "圣杯7": "代表诸多新的选择，但这种选择更多的存在于当事人的内心斗争中。圣杯7也代表梦境，虚幻不切实际的东西",
    "圣杯8": "离开旧有的繁华，寻找内在的智慧。圣杯八是水的能量达到顶峰溢出。如果两个人吵架问对方状态，那么圣杯八代表他有离开的念头。",
    "圣杯9": "梦里和愿望实现，圣杯九是一场狂欢，如同婚礼现场，曲终人散，都会归于平淡。\n圣杯九还可以代表对方对你有所隐瞒，整件事情的真相你是并不知情的。",
    "圣杯侍者": "一个永久的亲密朋友，或许是分别很久的童年朋友、初恋情人。",
    "圣杯国王": "一个诚实、善意的男子，但容易草率的作出决定，因此不是一个可以依赖的人，也不要指望从他那里得到有益的忠告。",
    "圣杯王后": "一个忠诚、钟情的女人，温柔大方，惹人怜爱。",
    "圣杯骑士": "一个假朋友，一个来自远方的陌生人、勾引者，应把握当前的命运。",
    "宝剑1": "不幸，坏消息，充满嫉妒的情感",
    "宝剑10": "悲伤或监禁，否定好兆头",
    "宝剑2": "变化，分离",
    "宝剑3": "一次旅行，爱情或婚姻的不幸",
    "宝剑4": "疾病，经济困难，嫉妒，各种小灾难拖延工作的进度",
    "宝剑5": "克服困难，获得生意成功或者和谐的伙伴",
    "宝剑6": "只要有坚韧不拔的毅力，就能完成计划",
    "宝剑7": "与朋友争吵，招来许多麻烦",
    "宝剑8": "谨慎，看似朋友的人可能成为敌人",
    "宝剑9": "疾病、灾难、或各种不幸",
    "宝剑侍者": "嫉妒或者懒惰的人，事业上的障碍，或许是骗子",
    "宝剑国王": "野心勃勃、妄想驾驭一切",
    "宝剑王后": "奸诈，不忠，一个寡妇或被抛弃的人",
    "宝剑骑士": "传奇中的豪爽人物，喜好奢侈放纵，但勇敢、有创业精神",
    "权杖1": "财富与事业的成功，终生的朋友和宁静的心境",
    "权杖10": "意想不到的好运，长途旅行，但可能会失去一个亲密的朋友",
    "权杖2": "失望，来自朋友或生意伙伴的反对",
    "权杖3": "不止一次的婚姻。可能和一个人订婚很长时间之后，却突然和另一个人结婚",
    "权杖4": "谨防一个项目的失败，虚假或不可靠的朋友起到了破坏作用",
    "权杖5": "娶一个富婆",
    "权杖6": "有利可图的合伙",
    "权杖7": "好运与幸福，但应提防某个异性",
    "权杖8": "贪婪，可能花掉不属于自己的钱",
    "权杖9": "头部受伤，头疼，困兽之斗，火的能量得不到释放，进入了衰微的阶段。",
    "权杖侍者": "一个诚挚但缺乏耐心的朋友，善意的奉承",
    "权杖国王": "一个诚挚的男人，慷慨忠实",
    "权杖王后": "一个亲切善良的人，但爱发脾气",
    "权杖骑士": "幸运地得到亲人或陌生人的帮助",
    "钱币1": "重要的消息，或珍贵的礼物",
    "钱币10": "把钱作为目标，但并不一定会如愿以偿",
    "钱币2": "对两件事物的斟酌和平衡。热恋，但会遭到朋友反对",
    "钱币3": "团体合作，合作伙伴关系。争吵，官司，或家庭纠纷",
    "钱币4": "守财奴，有很强的防御心，与外界隔离。\n可能是破财、花钱不幸或秘密的背叛，来自不忠的朋友，或家庭纠纷",
    "钱币5": "传染病，异地恋，肺病，腿部毛病，困难的生活和艰难的事业。体寒，腿部有毛病。虽然艰难但有希望。",
    "钱币6": "早婚，但也会早早结束，第二次婚姻也无好兆头",
    "钱币7": "谎言，谣言，恶意的批评，运气糟透的赌徒",
    "钱币8": "晚年婚姻，或一次旅行，可能带来结合",
    "钱币9": "强烈的旅行愿望，嗜好冒险，渴望生命得到改变",
    "钱币侍者": "一个自私、嫉妒的亲戚，或一个带来坏消息的使者",
    "钱币国王": "一个脾气粗暴的男人，固执而充满复仇心，与他对抗会招来危险",
    "钱币王后": "卖弄风情的女人，乐于干涉别人的事情，诽谤和谣言",
    "钱币骑士": "一个有耐心、有恒心的男人，发明家或科学家",
    "愚者正位": "憧憬自然的地方、毫无目的地前行、喜欢尝试挑战新鲜事物、四处流浪。明知是毫无意义的冒险，错误的选择及失败的结果，却一意孤行，盲目地追求梦想而完全忽略现实；\n好冒险、寻梦人、不拘泥于传统的观念、自由奔放、一切从基础出发、四处流浪。自由恋爱、不顾及他人看法、以独特的方式获得成功、轻易坠入爱河、浪漫多彩的爱情、独特的恋人、等待交往机会。\n工作上具冒险心、追求新奇。热衷于事业或学业、以独特的方式取得意外的收获、由于好奇心对当前的学业产生浓厚的兴趣、把握重点、寻求捷径、倾向于自由的工作氛围、适合艺术类工作或从事自由职业。健康状况佳。旅行有意外收获。美好的梦想。",
    "愚者逆位":"冒险的行动，追求可能性，重视梦想，无视物质的损失，离开家园，过于信赖别人，为出外旅行而烦恼。\n心情空虚、轻率的恋情、无法长久持续的融洽感、不安的爱情的旅程、对婚姻感到束缚、彼此忽冷忽热、不顾众人反对坠入爱河、为恋人的负心所伤、感情不专一。\n工作缺乏稳定性、无责任。成绩一落千丈、没有耐心、行事缺乏计划、经常迟到、猜题错误导致考试失利、考前突击无法为你带来太大的效果。\n因不安定的生活而生病。不能放心的旅行。不能下决心、怪癖。不切实际。",
    "魔术师正位": "事情的开始，行动的改变，熟练的技术及技巧，贯彻我的意志，运用自然的力量来达到野心。",
    "魔术师逆位": "意志力薄弱，起头难，走入错误的方向，知识不足，被骗和失败。",
    "女教皇正位": " 开发出内在的神秘潜力，前途将有所变化的预言，深刻地思考，敏锐的洞察力，准确的直觉。",
    "女教皇逆位":"过于洁癖，无知，贪心，目光短浅，自尊心过高，偏差的判断，有勇无谋，自命不凡。",
    "女皇正位": "幸福，成功，收获，无忧无虑，圆满的家庭生活，良好的环境，美貌，艺术，与大自然接触，愉快的旅行，休闲。",
    "女皇逆位":"不活泼，缺乏上进心，散漫的生活习惯，无法解决的事情，不能看到成果，耽于享乐，环境险恶，与家人发生纠纷。",
    "皇帝正位": "光荣，权力，胜利，握有领导权，坚强的意志，达成目标，父亲的责任，精神上的孤单。",
    "皇帝逆位":"幼稚，无力，独裁，撒娇任性，平凡，没有自信，行动力不足，意志薄弱，被支配。",
    "教皇正位": "援助，同情，宽宏大量，可信任的人给予的劝告，良好的商量对象，得到精神上的满足，遵守规则，志愿者。\n信心十足，能正确理解事物本质，工作上外来压力过多，使你有被束缚的感觉。寻找新的工作方法，尽管会面对很大的阻力，但结果会证明这样做是值得的。\n爱情上屈从于他人的压力，只会按照对方的要求来盲目改变自己，自以为这是必要的付出，其实不过是被迫的选择。伴侣也不会对你保持忠诚，并很难满足双方真实的需要。",
    "教皇逆位":"错误的讯息，恶意的规劝，上当，援助被中断，愿望无法达成，被人利用，被放弃。\n事业上多了些灵活的态度，不再刻板遵循旧有的方式，勇于创新形成自己独特的理念，为自己的真实想法而活。\n而感情上开始正视自己对感情的真实感受与做法，尽管依旧会听取对方的意见，但以不会全盘接受。当你感到无法接受对方的意见时，会及时与其沟通，找出改善关系的做法。",
    "恋人正位": "撮合，爱情，流行，兴趣，充满希望的未来，魅力，增加朋友。\n感情和肉体对爱的渴望，它暗示恋情将向彼此关系更亲密的方向发展。\n事业上将面临重大的抉择，它将关系到你的未来前途。",
    "恋人逆位":"禁不起诱惑，纵欲过度，反覆无常，友情变淡，厌倦，争吵，华丽的打扮，优柔寡断。\n感情上表现幼稚，对成长虽有期待与希望，却希望永远躲避危险，逃避责任。\n事业上总保持着很高的戒心，让人感到很不舒服，不愿同你合作。",
    "战车正位": "努力而获得成功，胜利，克服障碍，行动力，自立，尝试，自我主张，年轻男子，交通工具，旅行运大吉。\n事业上显示出才能，办事卓有成效。自信而富理智的你将让客户更有信心，愿意与你共同合作。\n在感情上正在努力控制自己的情绪，而且控制得很好，这让你的感情发展得更顺利。",
    "战车逆位":"争论失败，发生纠纷，阻滞，违返规则，诉诸暴力，顽固的男子，突然的失败，不良少年，挫折和自私自利。\n放弃以往在事业上所坚持的，结局将会更加完美。感情上失去方向，你已经没有以往的冷静，这让对方在心中产生了不信任感，也许你要反省一下自己的所作所为了。",
    "力量正位": "大胆的行动，有勇气的决断，新发展，大转机，异动，以意志力战胜困难，健壮的女人。\n在事业上你不断突破自我，上司和客户都对你有充分的信心，成就接踵而来。\n在爱情上，你将发展一段真正亲密的感情，你们全心投入，相互倾诉，丝毫没有距离感。",
    "力量逆位":"胆小，输给强者，经不起诱惑，屈服在权威与常识之下，没有实践便告放弃，虚荣，懦弱，没有耐性。内心的恐惧使你畏首畏尾，进而遭遇事业的瓶颈，感到失去了自信。在爱情上患得患失，失去清醒的判断。",
    "隐士正位": "隐藏的事实，个别的行动，倾听他人的意见，享受孤独，自己的丢化，有益的警戒，年长者，避开危险，祖父，乡间生活。\n你在事业黄金时期引退，旁人都不了解这不过是你在为下一次黄金时期的到来进行休息。\n感情方面你将深刻思考自己在这段感情中的角色和地位，并探索彼此之间的关系。",
    "隐士逆位":"无视警，憎恨孤独，自卑，担心，幼稚思想，过于慎重导致失败，偏差，不宜旅行。\n在事业中过多的投入已经让你不愿面对其它事情，因而事业有了突破性的进展。\n在感情方面，用工作繁忙来逃避这段感情的发展，对伴侣态度冷淡，因为害怕感情的发展而在关键时刻退缩，使对方心寒。",
    "命运之轮正位": "关键性的事件，有新的机会，因的潮流，环境的变化，幸运的开端，状况好转，问题解决，幸运之神降临。\n命运之轮正转到了你人生最低迷的时刻，也许你有些无法接受，但是若能以平常心来看待，这无疑是你成长的最好时机，需要认真面对。\n感情方面所受到的挫折近乎让你崩溃，然而你还在不断努力。虽然你面前是无数的荆棘，但坚持过去将是平坦的大道。你会发现以前所付出的无谓努力，而今反而成了你前进的动力，先前的付出终于有了回报。\n命运之轮是由命运女神转动的，所以你俩之前的风风雨雨都将过去，关系将进入稳定的发展阶段。",
    "命运之轮逆位":"边疆的不行，挫折，计划泡汤，障碍，无法修正方向，往坏处发展，恶性循环，中断。",
    "正义正位": "公正、中立、诚实、心胸坦荡、表里如一、身兼二职、追求合理化、协调者、与法律有关、光明正大的交往、感情和睦。\n事业上你不会有其它太多的感觉，只是按照以前的计划认真地执行。\n你对感情生活相当满意，对于你的选择对方都是接受的态度。",
    "正义逆位":"失衡、偏见、纷扰、诉讼、独断专行、问心有愧、无法两全、表里不一、男女性格不合、情感波折、无视社会道德的恋情。\n长时间的压抑使你在事业最关键的时刻倒下了，需要认真修整一番才能再次前进。\n感情上你一直忍让着，然而这次你却爆发了，开始指责对方的不是，你们的感情将会有很大的波折。",
    "倒吊者正位": "接受考验、行动受限、牺牲、不畏艰辛、不受利诱、有失必有得、吸取经验教训、浴火重生、广泛学习、奉献的爱。\n当牌面正立时，你的事业会有短暂的停顿，但你很清楚其中的原因，再次确认自己的目标，做好出发的准备。\n感情上同样需要反省的时间，你对爱情的牺牲对会给对方很大的触动，也会成为你们关系发展的催化剂。",
    "倒吊者逆位":"无谓的牺牲、骨折、厄运、不够努力、处于劣势、任性、利己主义者、缺乏耐心、受惩罚、逃避爱情、没有结果的恋情。\n当牌面倒立时，事业上缺乏远见，迷失了努力的目标。\n感情上你没有了为对方付出的念头，而对方对你的态度依旧，这使你更想逃避。你已经忽略了内心深处正确的判断力，这让你开始遇到很多失败。",
    "死神正位": "失败、接近毁灭、生病、失业、维持停滞状态、持续的损害、交易停止、枯燥的生活、别离、重新开始、双方有很深的鸿沟、恋情终止。\n事业上你将放弃一些得到的利益，并获得全新的发展机会。\n在感情上，你将会发生深刻的变化，将开始新的阶段，接受事实你们会有更加美好的旅程。",
    "死神逆位":"抱有一线希望、起死回生、回心转意、摆脱低迷状态、挽回名誉、身体康复、突然改变计划、逃避现实、斩断情丝、与旧情人相逢。\n事业上你在试图“两全其美”，希望能够发生奇迹。\n在感情上，对方已经接受了改变，而你却在逃避现实，你俩的距离正在越来越大。",
    "节制正位": "单纯、调整、平顺、互惠互利、好感转为爱意、纯爱、深爱。\n你在事业上小心翼翼，因为处事理智让你的同事感到十分放心。\n当下你们的感情简简单单，一切都是这么的单纯、平静，正是因为彼此的沟通才让这段感情之路如此通畅。",
    "节制逆位":"消耗、下降、疲劳、损失、不安、不融洽、爱情的配合度不佳。\n在事业上，你陷入了朝令夕改的怪圈，不妨效仿一下愚人勇往直前，或许能够取得更大的成功。\n感情上彼此虽然还在不断尝试着沟通，但每次之后总是感觉没有收获，正因为如此你们之间的距离才会越拉越大。",
    "恶魔正位": "被束缚、堕落、生病、恶意、屈服、欲望的俘虏、不可抗拒的诱惑、颓废的生活、举债度日、不可告人的秘密、私密恋情。\n你将在事业中得到相当大的名声与财富，你心中的事业就是一切，财富就是你的目标。\n感情上你们开始被彼此束缚，却不希望改善这种关系，情愿忍受彼此的牵连和不满。",
    "恶魔逆位":"逃离拘束、解除困扰、治愈病痛、告别过去、暂停、别离、拒绝诱惑、舍弃私欲、别离时刻、爱恨交加的恋情。\n事业上理性开始支配欲望，找到真正值得努力的目标。\n感情上开始尝试与对方进行沟通，这让你俩的感情更加牢固。",
    "高塔正位": "破产、逆境、被开除、急病、致命的打击、巨大的变动、受牵连、信念崩溃、玩火自焚、纷扰不断、突然分离，破灭的爱。\n事业上的困难显而易见，回避不是办法，要勇于挑战，尽管它貌似强大。\n在感情方面，突然的改变让你陷入深深的痛苦中，接受改变可以让你或你们双方在未来的人生旅途中走得更好。",
    "高塔逆位":"困境、内讧、紧迫的状态、状况不佳、趋于稳定、骄傲自大将付出代价、背水一战、分离的预感、爱情危机。\n事业上开始有稳定的迹象，你不要盲目抵抗改变的发生，这只会导致更大的改变，无论你如何抵抗，改变终究会发生。\n在感情上双方的情绪终于平静下来，虽然沟通上还有些困难，但不会有太大的变化了，也许你做些让步，会让你们的感情更融洽。",
    "星星正位": "前途光明、充满希望、想象力、创造力、幻想、满足愿望、水准提高、理想的对象、美好的恋情。\n代表当你在事业上得到希望的能量时，前途会无比光明。\n在感情方面，你对自己很有信心，对两人的关系也抱有乐观的态度，相信自己能把握主动权，并努力追求对方，你们很可能就是命中注定的那一对。",
    "星星逆位":"挫折、失望、好高骛远、异想天开、仓皇失措、事与愿违、工作不顺心、情况悲观、秘密恋情、缺少爱的生活。\n在事业上，你不要全部依靠别人的给予，因为你还有希望在心中燃烧，只有靠自己才有真正的发展动力。\n感情方面你俩无法彼此信任，感觉无法把自己托付给对方，也许你们退一步，都冷静一下就能找出解决问题的途径，因为答案就在你们的心中。",
    "月亮正位": "不安、迷惑、动摇、谎言、欺骗、鬼迷心窍、动荡的爱、三角关系。\n在事业上，你可能有些不满足，希望能够把自己内在的力量全使出来，于是你开始想要晚上的时间。\n感情方面，你很敏感害怕被伤害，尽管有伴侣的承诺，你仍然犹豫不决，甚至有逃避的想法。",
    "月亮逆位":"逃脱骗局、解除误会、状况好转、预知危险、等待、正视爱情的裂缝。\n在事业上，你因为外界的压力开始退缩了，并对自己的既定目标产生了怀疑。\n在感情上，你们之间的问题开始浮现，虽然有些痛，但是只要共同面对存在的困难，问题就解决一半了。",
    "太阳正位": "活跃、丰富的生命力、充满生机、精力充沛、工作顺利、贵人相助、幸福的婚姻、健康的交际。\n事业上会有贵人相助，将会有更好的发展机遇。\n在感情方面，你们已经走出坎坷的感情之路，前面将是洒满歌声和欢乐的坦途，你们将开始规划未来的生活。",
    "太阳逆位":"消沉、体力不佳、缺乏连续性、意气消沉、生活不安、人际关系不好、感情波动、离婚。\n事业上竞争心太急切了，把对手都吓跑了，然而也让合作伙伴感到害怕，或许你该放松些。\n感情上两人间出现一些小变化，开始在乎对方的态度和自己的付出，这些怀疑也许都是没必要的。",
    "审判正位": "复活的喜悦、康复、坦白、好消息、好运气、初露锋芒、复苏的爱、重逢、爱的奇迹。\n当牌面正立时，事业上你超越了自我，在过去努力的基础上取得了成功。\n感情上双方都在认真学习和成长，虽然表面上的变化并不大，但内在的改变已经很大了。",
    "审判逆位":"一蹶不振、幻灭、隐瞒、坏消息、无法决定、缺少目标、没有进展、消除、恋恋不舍。\n在事业上缺乏清晰的判断，试图用物质填充精神的空虚。\n在感情上，不断地回忆着过去的美好时光，不愿意去正视眼前的问题，你们的关系已经是貌合神离了。",
    "世界正位": "完成、成功、完美无缺、连续不断、精神亢奋、拥有毕生奋斗的目标、完成使命、幸运降临、快乐的结束、模范情侣。\n在事业上因为努力工作，所以回报丰厚。\n感情上，你们在彼此的承诺中持续着美好的关系。" ,
    "世界逆位":"未完成、失败、准备不足、盲目接受、一时不顺利、半途而废、精神颓废、饱和状态、合谋、态度不够融洽、感情受挫。\n在事业的路上有巨大的障碍，你精神不振，丧失了挑战的动力。\n感情上，你们不再重视承诺，只是盲目接受对方。彼此最好能沟通一下，不要让痛苦继续纠缠着你们。"
}

meanings = {
    "第一张牌": "代表过去，即已经发生的事",
    "第二张牌": "代表问题导致的局面",
    "第三张牌": "表示困难可能有的解决方法",
    "切牌": "表示问卜者的主观想法",
}
