import json

from pyrogram import Client, filters
from pyrogram.types import ForceReply

import config
import datetime
import keyboards
import random
import base64

from FusionBrain_Ai import generate

bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name = "Tvůj herní kamarád"
)


def button_filter(button):
    async def func(_, __, msg):
        return msg.text == button.text

    return filters.create(func, "ButtonFilter", button=button)


@bot.on_message(filters.command("start"))
async def start(bot, message):
    await message.reply("Vítejte u bota")
    await bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEB-LZpX0pFKhuBrlaqNEeP6xsG7AiGdwACBQADwDZPE_lqX5qCa011OAQ",
                           reply_markup=keyboards.kb_main
                           )
    with open("user.json", "r") as file:
        users = json.load(file)
    if str(message.from_user.id) not in users.keys():
        users[message.from_user.id] = 100
        with open("users.json", "w") as file:
            json.dump(users, file)


@bot.on_message(filters.command("time"))
async def time(bot, message):
    await bot.send_message(message.chat.id, f"Aktuální čas: {(datetime.datetime.now())}")


@bot.on_message(filters.command("info") | button_filter(keyboards.btn_info))
async def info(bot, message):
    await bot.send_message(message.chat.id, "Seznam přikazů: /Start, "
                                            "/time, "
                                            "/game, "
                                            "/image")

@bot.on_message(filters.command("game") | button_filter(keyboards.btn_games))
async def game(bot, message):
    await message.reply("Vítejte v sekci her!", reply_markup=keyboards.kb_games)
    with open("users.json", "r") as file:
        users = json.load(file)
    if users[str(message.from_user.id)] >= 10:
        await message.reply("Vyberte si svůj tah:", reply_markup=keyboards.kb_games)
    else:
        await message.reply(
            f"Nedostatečný zůstatek. Stav účtu {users[str(message.from_user.id)]} tokenů. Pro začátek hrz musíte mít na účtu alespoň 10 tokenů.")


@bot.on_message(filters.command("back") | button_filter(keyboards.btn_back))
async def back(bot, message):
    await message.reply("S čim vám mohu pomoci", reply_markup=keyboards.kb_main)


@bot.on_message(filters.command("rps") | button_filter(keyboards.btn_rps))
async def rps(bot, message):
    await message.reply("Vyberte si svůj tah:", reply_markup=keyboards.kb_rps)


@bot.on_message(button_filter(keyboards.btn_rock) |
                button_filter(keyboards.btn_paper) |
                button_filter(keyboards.btn_scissors))
async def choice_rps(bot, message):
    with open("users.json", "r") as file:
        users = json.load(file)

    rock = keyboards.btn_rock.text
    scissors = keyboards.btn_scissors.text
    paper = keyboards.btn_paper.text
    user = message.text
    pc = random.choice([rock, scissors, paper])
    await bot.send_message(message.chat.id, f"Bot vybral:{pc}")
    if (user == rock and pc == scissors) or (user == paper and pc == rock) or (user == scissors and pc == paper):
        await bot.send_message(message.chat.id, "Hrač vyhrál!")
        users[str(message.from_user.id)] += 10
        await message.reply(f"Stav účtu: {users[str(message.from_user.id)]} tokenů")
    elif (user == rock and pc == paper) or (user == paper and pc == scissors) or (user == scissors and pc == rock):
        await bot.send_message(message.chat.id, "Bot vyhrál!")
        users[str(message.from_user.id)] -= 10
        await message.reply(f"Stav účtu {users[str(message.from_user.id)]} tokenů")
    else:
        await bot.send_message(message.chat.id, "Je to remíza!")

    with open("users.json", "w") as file:
        json.dump(users, file)


@bot.on_message(filters.command("quest") | button_filter(keyboards.btn_quest))
async def kvest(bot, message):
    await message.reply_text("Chcete se stát součástí příběhu?", reply_markup=keyboards.inline_kb_start_quest)

query_text = "Zadejte prompt pro generování obrázku"
@bot.on_message(button_filter(keyboards.btn_generation))
async def image_command(bot, message):
    await message.reply(query_text,
                        reply_markup=ForceReply(True))

@bot.on_message(filters.reply)
async def reply(bot, message):
    if message.reply_to_message.text == query_text:
        query = message.text
        await message.reply_text(f"Generuji obrázek podle promptu: {query}. Už na tom pracuji...",
                                 reply_markup = keyboards.kb_main)

        image = await generate(query)
        if image:
            image_data = base64.b64decode(image[0])
            img_num = random.randint(1, 99)
            with open(f"images/image{img_num}.jpg", "wb") as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id, f"images/image{img_num}.jpg",
                                 reply_to_message_id=message.id)
        elif image is None:
             await message.reply("⚠️ Služba je momentálně nedostupná, zkuste to prosím později.")
             return

        else:
            await message.reply_text("Došlo k chybě, zkuste to znovu.",
                                     reply_to_message_id=message.id)

@bot.on_message(filters.command("image"))
async def image(bot, message):
    if len(message.text.split()) > 1:
        query = message.text.replace("/image", "")
        await message.reply_text(f"Generuji obrázek podle promptu: {query}")
        image = await generate(query)
        if image:
            image_data = base64.b64decode(image[0])
            img_num = random.randint(1, 99)
            with open(f"images/image{img_num}.jpg", "wb") as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id, f"images/image{img_num}.jpg",
                                 reply_to_message_id=message.id)
        else:
            await message.reply_text("Došlo k chybě, zkuste to znovu.",
                                     reply_to_message_id=message.id)
    else:
        await message.reply_text("Zadejte prompt:")


@bot.on_message()
async def echo(bot, message):
    if message.text.lower() == "Ahoj":
        await message.reply("Ahoj, kamaráde!")
    elif message.text.lower() == "Na schledanou":
        await message.reply("Měj se hezky, Uvidíme se!")
    else:
        await message.reply(f"Napsal jsi:{message.text}")


@bot.on_callback_query()
async def handle_query(bot, query):
    if query.data == "start_quest":
        await bot.answer_callback_query(query.id,
                                        text="V tomto příběhu se pustíte do vyšetřování a pokusíte se odhalit vraha slavné herečky Esther Elliot. Hodně štěstí!",
                                        show_alert=True)
        await query.message.reply_text("Blížil se večer. Sedíte v kanceláři, probíráte se dokumenty "
                                       "a kontrolujete údaje před jejich odesláním k soudu. Od práce vás vyruší váš nadřízený, "
                                       "který vstoupí do místnosti. "
                                       "- Detektiv Alane Fletchere? "
                                       "- Ano, pane. "
                                       "- Máme pro vás novou práci. Dnes došlo k vraždě Esther Elliot. "
                                       "Zde jsou všechny dosud dostupné informace k případu. Po jejich prostudování se vydejte na místo činu. "
                                       "Do ruky vám podá několik listů papíru s informacemi o případu.",
                                       reply_markup=keyboards.inline_kb_read_papers)
    elif query.data == "read_papers":
        await query.message.reply_text("Prohlížíte si dostupné informace. Z dokumentu se dozvídáte, že Esther Elliot byla zabita"
                                       "přibližně před hodinou výstřelem do krku přímo na jevišti během představení."
                                       "Podle všeho se pachatel po činu ztratil v davu."
                                       "Po kontrole adresy si sbalíte všechny potřebné věci spolu se spisem a vyrážíte do divadla."
                                    ,
                                       reply_markup=keyboards.inline_kb_theather)
    elif query.data == "theather":
        await query.message.reply_text("Poměrně rychle dorazíte na místo činu. Policista vás přivítá a zavede dovnitř budovy."
                                       "Uprostřed jeviště leží tělo Esther. Na krku je viditelná stopa po výstřelu. Po podlaze se rozlévá krev."
                                       "Za vámi stojí policista a mladá žena."
                                        "— Ta dívka je svědkyně?"
                                        "— Ano. To je Honori Dane, jedna z hereček tohoto divadla."
                                        "— Mohu s ní mluvit?"
                                        "— Samozřejmě.",
                                       reply_markup=keyboards.inline_kb_talk)
    elif query.data == "talk":
        await query.message.reply_text("Dobrý den, slečno, jsem detektiv pověřený vyšetřováním vraždy Esther Elliot."
                                       "Můžete mi podrobně popsat, co se stalo v okamžiku vraždy?"
                                        "— Dobrý den… ano, samozřejmě. No… stalo se to během jejího sólového tance podle scénáře."
                                       "Já jsem spolu s ostatními herečkami stála v levém zákulisí. Esther v tu chvíli vycházela na jeviště."
                                       "Ostatní kolegyně si opakovaly texty a převlékaly se na další výstup, a já jsem sledovala její vystoupení."
                                       "Víte… obdivovala jsem ji už od mládí… A pak… pak jsem uslyšela ostrý zvuk výstřelu z levé části hlediště"
                                       "a… a v příštím okamžiku vytryskla krev a ona spadla na zem. Všichni byli v šoku a začali v panice utíkat z sálu,"
                                       "a já… já jsem utekla do šatny za jevištěm."
                                        "Dívka byla stále velmi vyděšená a v šoku."
                                        "— Děkuji, slečno Dane, vaše svědectví je opravdu cenné.",
                                       reply_markup=keyboards.inline_kb_question)
    elif query.data == "ask_about_Esther":
        await query.message.reply_text("Rád bych položil ještě jednu otázku. Všimla jste si v poslední době u Esther nějakého zvláštního chování?"
                                        "— Dejte mi chvilku… asi ano. Poslední dobou vypadala velmi vyčerpaně. Měla na sobě obrovské množství práce spojené s rolí,"
                                        "ale překvapivě působila, jako by vůbec nebyla unavená. Také se začala jakoby vzdalovat ostatním. Měla jsem podezření, že jí někdo…"
                                        "nebo možná ona sama… bere nějaké látky, aby zvládala pracovat efektivněji."
                                        "— Ještě jednou vám děkuji, slečno Dane."
                                        "Rozhodl jste se, že tyto informace vám prozatím postačí.",
                                       reply_markup=keyboards.inline_kb_look_body)
    elif query.data == "look_body":
        await query.message.reply_text("Rozhodnete se už nepokládat další otázky a znovu se vrátíte k prohlídce těla. Na podlaze si všimnete cákanců krve, o kterých mluvila Honori Dane."
                                       "Poloha a délka stop potvrzují, že výstřel přišel z levé strany hlediště, pod úhlem ze sedadel blíže k východu a z malé výšky – pravděpodobně ze zadních řad."
                                        "Začnete procházet pravděpodobná místa, odkud mohl být výstřel veden. Pachatel by se neodvážil držet zbraň na očích,"
                                       "a tak se vám podaří určit oblast mezi dvěma sedadly v zadní řadě. To by mohlo pomoci při hledání podezřelých.",
                                       reply_markup=keyboards.inline_kb_ask)
    elif query.data == "ask":
        await query.message.reply_text("Přistoupíte k pokladně u vstupu do divadla. Na žádost policie zde zůstal jeden ze zaměstnanců."
                                        "— Dobrý den, jsem detektiv vyšetřující případ Esther Elliot. Mohl byste mi poskytnout seznam hostů a jejich místa z posledního představení?"
                                        "— Dobrý den, hned se podívám. Máte nějaké podezření na konkrétní osoby?"
                                        "— Zkontrolujte, prosím, místa v 9. řadě, čísla 16 a 17."
                                        "Zaměstnanec se posadí k počítači a začne procházet seznam jmen a míst."
                                        "— Zjistil jsem jména vašich podezřelých. Místo 16 bylo registrováno na jméno Lionela de Curie. Hned vedle, na sedadle číslo 17, dnes seděl Stefan Elliot."
                                        "Ještě něco?"
                                        "— To stačí, děkuji vám."
                                        "Nyní máte seznam podezřelých.",
                                       reply_markup=keyboards.inline_kb_alibi)

    elif query.data == "go_Curie":
        await query.message.reply_text("Po přípravě se nejprve rozhodnete prověřit Lionela de Curie. Jste přivítáni a je vám dovoleno vstoupit do jeho sídla."
                                        "— Pane de Curie, povězte mi svou verzi událostí. Co jste dělal před vraždou Esther Elliot?"
                                        "— Ten den jsem se chystal odjet z města za prací. Ráno jsem si předem sbalil všechny věci. Před odjezdem měl být v divadle představení s Esther v hlavní roli."
                                        "Je to moje sestřenice, a tak jsem se s ní chtěl po skončení představení rozloučit. Ale byla zabita přímo na jevišti a já byl nucen zůstat zde."
                                        "Po položení několika dalších otázek se rozhodnete zeptat na zbraň."
                                        "— Měl jste ten den u sebe zbraň?"
                                        "— Obvykle s sebou nosím revolver pro sebeobranu, mám na něj povolení. Ale toho dne jsem ho celé ráno nemohl najít a odešel jsem bez něj s tím,"
                                        "že se před odjezdem ještě vrátím domů a zkusím ho najít."
                                        "— Revolver s vyrytým vaším jménem byl nalezen na místě činu, odhozený poblíž vchodu do sálu. Byly na něm pouze vaše otisky prstů."
                                        "Lionel de Curie viditelně znejistí a překvapeně se nadechne."
                                        "— Nevím, jak se tam mohl dostat, přísahám, že jsem ho u sebe neměl. Možná ho někdo ukradl, aby mě mohl obvinit?"
                                        "— Tvrdíte tedy, že jste nevinný?"
                                        "— Ano."
                                        "S těmito informacemi dialog brzy ukončíte a s novými poznatky opouštíte sídlo.",
            reply_markup=keyboards.inline_kb_L_guilty)
    elif query.data == "Curie_guilty":
        await query.message.reply_text( "Rozhodnete se, že informace, které máte k dispozici, jsou dostačující. V kanceláři znovu projdete celý případ. Místo de Curieho během představení,"
                                        "revolver s vyrytým jménem a otisky prstů, stejně jako nesrovnalosti v jeho alibi, se vám jeví jako jasné důkazy viny Lionela de Curie."
                                        "Brzy shromáždíte dokumenty a odešlete je k soudu. Během soudního řízení je obžalovaný na základě předložených důkazů shledán vinným a odsouzen za vraždu."
                                        "Vaše práce je hotova… ale i přes všechny důkazy ve vás zůstává nepříjemný pocit, že něco nesedí. Možná jste se mýlil?",
                                       )
    elif query.data == "go_Elliot":
        await query.message.reply_text("Po přípravě dorazíte k domu Stefana Elliota. Jste přivítáni a je vám dovoleno vstoupit dovnitř."
                                        "— Pane Elliote, povězte mi svou verzi událostí. Co jste dělal před vraždou své ženy?"
                                        "Stefan je viditelně nervózní."
                                        "— Ach, detektive Fletchere… o tom se velmi těžko mluví. Ten den začal tak krásně. S mou milovanou jsme spolu posnídali, pak odešla na zkoušku a já otevřel svůj obchod."
                                        "Den se neskutečně vlekl, pořád jsem čekal na večer a na vystoupení své ženy, nemohl jsem se dočkat zavírací hodiny. Hned po práci jsem se připravil a vyrazil do divadla."
                                        "A jaké to bylo nádherné představení! A pak… když moje žena vyšla na jeviště… vražda za bílého dne! Uslyšel jsem výstřel z revolveru a v tom okamžiku…"
                                        "moje milá Esther se zhroutila na podlahu jeviště! Pocítil jsem hrůzu a zoufalství a utekl jsem ze sálu spolu s davem. Byl to strašný okamžik!"
                                        "Pan Elliot během vyprávění působil velmi rozrušeně, ale mluvil až příliš teatrálně. Nebylo jasné, zda je to jen jeho zvláštní způsob vyjadřování, nebo se snaží něco skrýt."
                                        "V každém případě to vzbuzovalo podezření."
                                        "Položíte Stefanovi několik dalších otázek."
                                        "— Nevšiml jste si u své ženy v poslední době nějakého zvláštního chování?"
                                        "Ze Stefanových úst unikne nervózní smích."
                                        "— Heh… ne, proč byste si to myslel? Byla úplně v pořádku! Hned bych si všiml, kdyby s mou milovanou bylo něco v nepořádku, a určitě by mi všechno řekla."
                                        "Měli jsme mezi sebou důvěru a… a žádné problémy nebyly!"
                                        "Chování pana Elliota vás silně znepokojuje. Rozhodnete se prohlédnout dům Elliotových a pokusit se najít další stopy.",
                                       reply_markup=keyboards.inline_kb_Look_house)
    elif query.data == "Look_house":
        await query.message.reply_text("Požádáte pana Elliota o možnost prohlédnout si dům. Na vaši žádost reaguje vyděšeně a snaží se odvést vaši pozornost od prohlídky."
                                        "— Vaše chování je příliš podezřelé, pane. Nechte mě prohlédnout dům."
                                        "Stefan téměř nereaguje, ale nakonec vás přece jen pustí dovnitř."
                                        "Začnete pečlivě hledat stopy. Na stole leží pár pánských látkových rukavic. Pokud je Stefan vinen, mohly sloužit k tomu, aby nezanechal otisky."
                                        "Dále v zásuvce stolu nacházíte paklíč – pravděpodobně použitý ke krádeži zbraně. Ve druhé zásuvce leží ukrytý sešit. Rozhodnete se ho vytáhnout a přečíst si jeho obsah."
                                        "Uvnitř je, mírně řečeno, šokující text."
                                        "Možná Esther tvrdila, že je všechno v pořádku, ale v sešitě jsou popsány její děsivé sebevražedné myšlenky… a co je nejvíce zarážející – plán,ve kterém ji má zabít její vlastní manžel."
                                        "Bohužel se zdá, že její plán vyšel."
                                        "Při dalším ohledání si všimnete skryté videokamery.",
                                       reply_markup=keyboards.inline_kb_look_camera)
    elif query.data == "look_camera":
        await query.message.reply_text( "Prohlížíte si obsah videokamery. Zachovaly se na ní pouze krátké útržky záznamu – možná se je někdo pokusil smazat. Na záběrech je vidět hádka."
                                        "Z nahrávek jsou také slyšet útržky jejich rozhovoru."
                                        "— Už takhle nemůžu dál žít, Stefane."
                                        "— To neudělám. Uvědomuješ si vůbec, o čem mluvíš?"
                                        "— Jaký má smysl pokračovat v životě, když přináší jen utrpení? Je snad příjemné dívat se, jak ten, koho miluješ, trpí? Můžeme to ukončit, miláčku… a ani ty, ani já už nebudeme trpět."
                                        "V tomto okamžiku se záznam přeruší."
                                        "Shromáždíte všechny nalezené důkazy a vrátíte se ke Stefanovi."
                                        "— Pane Elliote, mám na vás otázku. Nemluvila vaše manželka o tom, že by chtěla zemřít?"
                                        "— Z… z čeho to soudíte?"
                                        "— Při prohlídce byla nalezena sešit vaší ženy, kde psala o myšlenkách na smrt a o plánu své vraždy, a také záznamy z videokamery."
                                        "Po těchto slovech se ve Stefanově tváři objeví výraz zděšení a hrůzy. Jeho hlas se začne silně třást."
                                        "— Já… já… já nechtěl… Nechtěl jsem ji zabít! Ale… ale já… neměl jinou možnost…"
                                        "Poté Stefan tiše cosi mumlá pod vousy, z jeho slov zachytíte pouze slovo 'sešit'."
                                        "Rychle ukončíte rozhovor a s novými důkazy se vracíte do kanceláře.",
                                       reply_markup=keyboards.inline_kb_Elliot_guilty)

    elif query.data == "Elliot_guilty":
        await query.message.reply_text("Důkazů bylo více než dost. Shromáždíte všechny materiály – od deníku a záznamů z videokamery až po revolver ukradený Lionelu de Curie – a sepíšete závěrečnou zprávu k případu pro soud."
                                        "Brzy je Stefan Elliot u soudu uznán vinným z vraždy a krádeže zbraně a odsouzen k trestu odnětí svobody. Vaše práce je hotova. Tento případ vám zůstane v paměti ještě velmi dlouho.")


bot.run()
