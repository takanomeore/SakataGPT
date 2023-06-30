import discord
import random
import time
import openai
import asyncio
import MySQLdb

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'Your DiscordBOT TOKEN KEY'
# OpenAI
openai.api_key = "Your OpenAI API KEY"

intents = discord.Intents.default()
intents.typing = False
intents.reactions = True
intents.message_content = True
# 接続に必要なオブジェクトを生成
client = discord.Client(intents=intents)

#MariaDB
tables = ["Players","Enemys"]

class Player:
    id = 0
    name = ""
    hp = 0
    atp = 0
    dfp = 0
    spd = 0

    def set(self,name,hp,atp,dfp,spd):
        self.name = name
        self.hp = hp
        self.atp = atp
        self.dfp = dfp
        self.spd = spd
    def attack(self):
        return self.atp
    def changeHP(self,enATP):
        self.hp -= enATP
    def deffence(self):
        return self.dfp

class Enemy:
    name = ""
    hp = 0
    atp = 0
    dfp = 0
    id = 0
    def set(self,name,hp,atp,dfp,id):
        self.name = name
        self.hp = hp
        self.atp = atp
        self.dfp = dfp
        self.id = id
    def attack(self):
        return self.atp
    def changeHP(self,enATP):
        self.hp -= enATP
    def deffence(self):
        return self.dfp


messageId = ""
checkEmoji = ""
isEmoji = False
digits = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣']
selNum = 0

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('We have logged in {0:user}')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    def check(msg):
        return msg.author == message.author
    if not message.author.bot:
        if message.content.startswith('Hey'):
            if(message.author.id == 714065796317577257):
                await message.channel.send("管理者権限で実行します.")
            identityMode = ["",""]
            identityMode = message.content.split('y')
            numMode = 0
            gameModeStr = ""
            try:
                numMode = int(identityMode[1])
            except ValueError:
                await message.channel.send("遊びたいゲームモードを選んでね！\n1.指立て　2.坂田じゃんけん　3.ドラクエモンスターズ\n4.ダイスロール　5.ShatGPT")
                try:
                    gamemode = await client.wait_for("message", check=check,timeout = 20)
                    gameModeStr = gamemode.content
                except asyncio.TimeoutError:
                    await message.channel.send("待ち時間上限を超えました。処理を中断します.")
                    return
            if (gameModeStr == "1" or numMode == 1):
                await message.channel.typing()
                time.sleep(0.5)
                await message.channel.send("何指を立てるか選んでください\n1.親指　2.小指　3.ここ")
                while (1):
                    time.sleep(0.3)
                    try:
                        wait = await client.wait_for("message", check=check,timeout = 20)
                    except asyncio.TimeoutError:
                        await message.channel.send("待ち時間上限を超えました。処理を中断します.")
                        return
                    if (wait.content != '1' and wait.content != '2' and wait.content != '3'):
                        await message.channel.send("半角数字を入力してね!??!?!!")
                    else:
                        break
                finger = int(wait.content)
                await message.channel.typing()
                time.sleep(0.7)
                if (finger == 1):
                    await message.channel.send("親指を立てました")
                elif (finger == 2):
                    await message.channel.send("小指を立てました")
                else:
                    await message.channel.send("ボロン")
            elif (gameModeStr == "2" or numMode == 2):
                roop = True
                playFinger = 'グー'
                myfinger = 1
                await message.channel.typing()
                time.sleep(0.5)
                await message.channel.send(":girl:ねえねえお兄ちゃん、私とじゃんけんしよ？\nもし勝ったら・・・")
                await message.channel.typing()
                time.sleep(1.5)
                while (roop):
                    await message.channel.typing()
                    time.sleep(0.8)
                    await message.channel.send(":girl:じゃあいくよ？最初はグー")
                    await message.channel.typing()
                    time.sleep(0.5)
                    await message.channel.send("じゃんけん・・・")
                    try:
                        finger = await client.wait_for("message", check=check,timeout = 15)
                    except asyncio.TimeoutError:
                        await message.channel.send("待ち時間上限を超えました。処理を中断します.")
                        return
                    if (finger.content == "グー" or finger.content == "チョキ" or finger.content == "パー"):
                        playFinger = finger.content
                        roop = False
                    else:
                        time.sleep(0.3)
                        await message.channel.send(":girl:もーお兄ちゃん、じゃんけんやったことないの？\nグーチョキパーのどれかを出してよ")
                girlfinger = random.randint(0 , 2)
                if (playFinger == "グー"):
                    myfinger = 0
                elif (playFinger == "チョキ"):
                    myfinger = 1
                else:
                    myfinger = 2
                time.sleep ( 0.5 )
                await message.channel.typing()
                if (girlfinger == 0):
                    await message.channel.send(":girl:グー！")
                elif (girlfinger == 1):
                    await message.channel.send(":girl:チョキ！")
                else:
                    await message.channel.send(":girl:パー！")
                battle = myfinger - girlfinger
                await message.channel.typing()
                time.sleep ( 1 )
                if (battle == 0):
                    await message.channel.send(":cat:あいこでしたね")
                elif (battle == -1 or battle == 2):
                    await message.channel.send(":cat:おお、あなたの勝ちです")
                else:
                    await message.channel.send(":cat:残念、あなたの負けです:cry:")
            elif(gameModeStr == "3" or numMode == 3):
                try:
                    conn = connectDB()

                    cur = conn.cursor()
                    plData = Player()
                    plStatus = ['','','','']
                    myinsertSQL = ""
                    result = []
                    try:
                        cur.execute(f"SELECT * FROM Players WHERE id = {message.author.id}")
                        result = cur.fetchall()
                    except MySQLdb.Error as e:
                        print('データベースエラー',e)
                    if(len(result) == 0):
                        await message.channel.send("```初めまして！勇者{0}さん！\
                            \n初めてプレイする勇者さんには、プレイヤー登録をしてもらいます。所定の形式で入力してください\
                            \n入力例：　takanomeore,100,50,50,30\
                            \nステータスを自分で決めてください。左から名前、体力、攻撃力、防御力、素早さです\
                            \nステータスの合計値が250以下になるように振り分けてください。ステータスは半角コロン（,）で区切ります。```".format(message.author.name))
                        while(1):
                            try:
                                waitStatus = await client.wait_for("message", check = check,timeout = 60)
                            except TimeoutError:
                                await message.channel.send("待ち時間上限を超えました。処理を中断します.")
                                return
                            tmpStatus = waitStatus.content.split(',')
                            plName = tmpStatus[0]
                            myinsertSQL = f"'{plName}'"
                            try:
                                for i in range(4):
                                    plStatus[i] = tmpStatus[i + 1]
                                    myinsertSQL += f",{plStatus[i]}"
                                myinsertSQL += f",{message.author.id}"
                            except (ValueError, IndexError):
                                await message.channel.send("入力が不正です\
                                        \n入力例：　takanomeore,100,50,50,30\
                                        \nステータスを自分で決めてください。左から名前、体力、攻撃力、防御力、素早さです\
                                        \nステータスの合計値が250以下になるように振り分けてください。ステータスは半角コロン（,）で区切ります。```")
                            else:
                                await message.channel.send("{0}さん、登録が完了しました！".format(plName))
                                cur.execute(f"INSERT INTO Players (pName,hp,atp,dfp,spd,id) VALUES({myinsertSQL});")
                                conn.commit()
                                break
                    cur.execute(f"SELECT * FROM Players WHERE id = {message.author.id}")
                    datas = cur.fetchall()
                    plData.set(datas[0][0],datas[0][1],datas[0][2],datas[0][3],datas[0][4])
                    welcomeTemplate = f"{plData.name}さん。ようこそ。何をしますか？\n1.冒険の旅へ　2.ステータス確認　3.ギルド登録者一覧\n4.敵エディット　5.残存敵勢力一覧\n6.ギルド実績一覧　7.英霊の石碑" 
                    editString = await message.channel.send(f"```{welcomeTemplate}```")
                    global isEmoji
                    global selNum
                    enData = Enemy()
                    enStatus = ['','','']
                    myinsertSQL = ""
                    while(1):
                        for i in range(7):
                            await editString.add_reaction(digits[i])
                        await asyncio.wait_for(waitChoiceEmoji(),timeout = 60)
                        if(selNum == 1):
                            break
                        elif(selNum == 2):
                            currentStatus = f"```勇者{plData.name}のステータス\
                                \n体力：{plData.hp}　攻撃力：{plData.atp}　防御力：{plData.dfp}　素早さ：{plData.spd}```"
                            currentStatus += f"```{welcomeTemplate}```"
                            await editString.edit(content= f"{currentStatus}")
                        elif(selNum == 3):
                            cur.execute(f"SELECT * FROM Players")
                            allChara = cur.fetchall()
                            allStatus = ""
                            for i in range(len(allChara)):
                                allStatus += f"```登録名：{allChara[i][0]}\
                                    \n体力：{allChara[i][1]}　攻撃力：{allChara[i][2]}　防御力：{allChara[i][3]}　素早さ：{allChara[i][4]}```"
                            allStatus += f"```{welcomeTemplate}```"
                            await editString.edit(content= f"{allStatus}")
                        elif(selNum == 4):
                            await editString.edit(content= "```あなたと戦うことになる敵をあなたの手で作りましょう\
                                                  \n入力例：メオレ,100,50,30```")
                            wait = await client.wait_for("message",check= check)
                            editString = await message.channel.send("```データベースと通信しています・・・```")
                            tmpStatus = wait.content.split(',')
                            enName = tmpStatus[0]
                            myinsertSQL = f"'{enName}',"
                            try:
                                for i in range(3):
                                    myinsertSQL += f"{tmpStatus[i + 1]},"
                                k = 0
                                while(1):
                                    cur.execute(f"SELECT * FROM Enemys WHERE id = {k + 1}")
                                    tmpList = cur.fetchall()
                                    if(len(tmpList) == 0):
                                        break
                                    await asyncio.sleep(0.5)
                                    k+=1
                                myinsertSQL += f"{k + 1},'{message.author.name}'"
                                cur.execute(f"INSERT INTO Enemys(enName,enHP,enATP,enDFP,id,author) VALUES({myinsertSQL});")
                                conn.commit()
                                await editString.edit(content= f"```敵情報の登録が完了しました\
                                                      \n\n{welcomeTemplate}```")
                            except (ValueError, IndexError):
                                await editString.edit(content= f"```入力が不正です\n{welcomeTemplate}```")
                                asyncio.sleep(1)
                        elif(selNum == 5):
                            cur.execute("SELECT * FROM Enemys")
                            enList = cur.fetchall()
                            enListStr = ""
                            for i in range(len(enList)):
                                enListStr += f"```{enList[i][0]}　作成者：{enList[i][5]}\
                                    \n体力：{enList[i][1]}　攻撃力：{enList[i][2]}　防御力：{enList[i][3]}\n```"
                            enListStr += f"\n```{welcomeTemplate}```"
                            await editString.edit(content= enListStr)
                        elif(selNum == 6):
                            cur.execute("SELECT * FROM Deaths WHERE superID LIKE 'EN%';")
                            guildList = cur.fetchall()
                            guildStr = "```ギルド　モンスター討伐実績\n"
                            for i in range(len(guildList)):
                                guildStr+= f"\n通称：{guildList[i][0]}　討伐者：{guildList[i][1]}"
                            guildStr += f"\n\n\n{welcomeTemplate}```"
                            await editString.edit(content= guildStr)
                        elif(selNum == 7):
                            cur.execute("SELECT * FROM Deaths WHERE superID LIKE 'PL%';")
                            guildList = cur.fetchall()
                            guildStr = "```英霊の石碑に刻まれた勇者一覧\n"
                            for i in range(len(guildList)):
                                guildStr += f"\n{guildList[i][0]}　{guildList[i][1]}との戦闘中に殉死"
                            guildStr += f"\n\n\n{welcomeTemplate}```"
                            await editString.edit(content= guildStr)
                        await editString.clear_reactions()
                    await editString.clear_reactions()
                    await editString.edit(content= f"```どこへ行きますか？\
                                            \n1.戒めの森(レベル１)　2.闇の神殿(レベル２)　3.伊勢原市（レベル３)```")
                    for i in range(3):
                        await editString.add_reaction(digits[i])
                    global messageId
                    global checkEmoji

                    enemys = [Enemy()] * 3
                    tmpenStatus = [None for i in range(5)]
                    enStatus = [None] * 5
                    messageId = editString
                    enNum = 0
                    enRand = [0] * 3
                    maps = ['戒めの森','闇の神殿','伊勢原市']
                    await asyncio.wait_for(waitChoiceEmoji(),timeout = 60)
                    cur.execute("SELECT COUNT( * ) FROM Enemys;")
                    enCount = cur.fetchall()
                    if(enCount[0][0] == 0):
                        await editString(content= "```どうやら存在していたモンスター達はすべて私たちの手で\
                                         \n倒されてしまったみたいです。ついにこの世界に平和が訪れました\
                                         \nHappyEnd...```")
                        return
                    cur.execute("SELECT MAX( id ) FROM Enemys;")
                    enMax = cur.fetchall()
                    enNum = selNum
                    for i in range(selNum):
                        if(i >= enCount[0][0]):#敵の数がselNumに満たなかったら
                            enNum = i
                            break
                        enemys[i] = Enemy()
                        tmpRand = random.randint(1,int(enMax[0][0]))
                        while(1):
                            cur.execute(f"SELECT * FROM Enemys WHERE id = {tmpRand};")
                            enExist = cur.fetchall()
                            if(i >= 1):
                                if((len(enExist) == 0) or (tmpRand in enRand)):
                                    tmpRand = random.randint(1,int(enMax[0][0]))
                                else:
                                    enRand[i] = tmpRand
                                    break
                            else:
                                while(1):
                                    if(len(enExist) != 0):
                                        enRand[i] = tmpRand
                                        break
                                    tmpRand = random.randint(1,int(enMax[0][0]))
                                    cur.execute(f"SELECT * FROM Enemys WHERE id = {tmpRand};")
                                    enExist = cur.fetchall()
                                break
                        cur.execute(f"SELECT * FROM Enemys WHERE id = {enRand[i]}")
                        tmpenStatus = cur.fetchall()
                        for row in tmpenStatus:
                            enStatus = row
                        enemys[i].set(enStatus[0],enStatus[1],enStatus[2],enStatus[3],enStatus[4])
                        #DBから数字で敵キャラを抜き出す方法を考える必要あり

                    await editString.clear_reactions()
                    for i in range(3):
                        if(i == enNum - 1):
                            await editString.edit(content= f"```{maps[i]}へ向かっています・・・```")
                            break
                    time.sleep(1)
                    j = 0
                    battleText = f"```敵が{enNum}体現れました\n"
                    for i in range(enNum):
                            battleText += f"{i+1}.{enemys[i].name} 残りHP={enemys[i].hp}\n"
                    battleText += f"\n\n{plData.name}　残りHP：{plData.hp}\n1.攻撃　2.逃げる```"
                    await editString.edit(content= battleText)
                    await asyncio.sleep(3)
                    killer = ""
                    while(1):
                        battleText = "```"
                        for i in range(enNum):
                            battleText += f"{i+1}.{enemys[i].name} 残りHP={enemys[i].hp}\n"
                        battleText += f"\n\n{plData.name}　残りHP：{plData.hp}\n1.攻撃　2.逃げる```"
                        await editString.edit(content= battleText)
                        for i in range(2):
                            await editString.add_reaction(digits[i])
                        await asyncio.wait_for(waitChoiceEmoji(),timeout = 60)
                        battleText = "```"
                        for i in range(enNum):
                            battleText += f"{i+1}.{enemys[i].name} 残りHP={enemys[i].hp}\n"
                        if(selNum == 1):
                            await editString.clear_reactions()
                            battleText += f"\n{plData.name}　残りHP={plData.hp}\
                                \n攻撃対象を選んでください```"
                            await editString.edit(content= battleText)
                            for i in range(enNum):
                                await editString.add_reaction(digits[i])
                            await asyncio.wait_for(waitChoiceEmoji(),timeout = 60)
                            if(selNum == 1):
                                if(enemys[selNum - 1].hp <= 0):
                                    battleText = "```死んだ敵には攻撃できません```"
                                    await editString.edit(content= battleText)
                                    await asyncio.sleep(2)
                                    continue
                                battleText = f"```{plData.name}の攻撃！\n{enemys[selNum - 1].name}は{plData.attack()}のダメージを受けた```"
                                await editString.edit(content= battleText)
                                enemys[selNum - 1].changeHP(plData.attack())
                                await asyncio.sleep(3)
                            elif(selNum == 2):
                                if(enemys[selNum - 1].hp <= 0):
                                    battleText = "```死んだ敵には攻撃できません```"
                                    await editString.edit(content= battleText)
                                    await asyncio.sleep(3)
                                    continue
                                battleText = f"```{plData.name}の攻撃！\n{enemys[selNum - 1].name}は{plData.attack()}のダメージを受けた```"
                                await editString.edit(content= battleText)
                                enemys[selNum - 1].changeHP(plData.attack())
                                await asyncio.sleep(3)
                            elif(selNum == 3):
                                if(enemys[selNum - 1].hp <= 0):
                                    battleText = "```死んだ敵には攻撃できません```"
                                    await editString.edit(content= battleText)
                                    await asyncio.sleep(3)
                                    continue
                                battleText = f"```{plData.name}の攻撃！\n{enemys[selNum - 1].name}は{plData.attack()}のダメージを受けた```"
                                await editString.edit(content= battleText)
                                enemys[selNum - 1].changeHP(plData.attack())
                                await asyncio.sleep(3)
                            for i in range(enNum):
                                if(enemys[i].hp <= 0):
                                    continue
                                battleText = battleText[:-3]
                                battleText  += f"\n\n{enemys[i].name}の攻撃！\n{plData.name}は{enemys[i].attack()}のダメージを受けた。```"
                                await editString.edit(content= battleText)
                                plData.changeHP(enemys[i].attack())
                                await asyncio.sleep(3)
                                if(plData.hp <= 0):
                                    killer = enemys[i].name
                                    break
                            if(plData.hp <= 0):
                                    battleText = battleText[:-3]
                                    battleText+= f"\n{plData.name}は死んでしまった・・・```"
                                    await editString.edit(content= battleText)
                                    await asyncio.sleep(5)
                                    battleText = battleText[:-3]
                                    battleText += f"\n{plData.name}の勇敢な戦いぶりは、我がギルドのメンバーたちに多大なる影響を与えていた・・・\
                                        \n彼の魂は受け継がれ、永遠に消えることはない・・・\n{plData.name}の名前を英霊の石碑に刻み\
                                        彼の亡骸はJの意思へ献上されていった・・・```"
                                    await editString.edit(content= battleText)
                                    break
                        elif(selNum == 2):
                            await message.channel.send(f"```{plData.name}は逃げ出した！```")
                            await asyncio.sleep(5)
                            break
                        await editString.clear_reactions()
                    if(plData.hp <= 0):
                        k= 1
                        while(1):
                            cur.execute(f"SELECT * FROM Deaths WHERE superID = 'PL{k}'")
                            deathList = cur.fetchall()
                            if(len(deathList) != 0):
                                k+= 1
                                continue
                            cur.execute(f"INSERT INTO Deaths(pName,id,superID,killer) VALUES('{plData.name}',{message.author.id},'PL{k}','{killer}');")
                            conn.commit()
                            cur.execute(f"DELETE FROM Players WHERE id = {message.author.id};")
                            conn.commit()
                            break
                    else:
                        cur.execute(f"UPDATE Players SET hp = {plData.hp} WHERE id = {message.author.id};")
                        conn.commit()
                    for i in range(enNum):
                        k= 1
                        if(enemys[i].hp <= 0):
                            while(1):
                                cur.execute(f"SELECT * FROM Deaths WHERE superID = 'EN{k}';")
                                deathList = cur.fetchall()
                                if(len(deathList) != 0):
                                    k+= 1
                                    continue
                                cur.execute(f"INSERT INTO Deaths(pName,id,superID,killer) VALUES('{enemys[i].name}',{k},'EN{k}','{plData.name}');")
                                conn.commit()
                                cur.execute(f"DELETE FROM Enemys WHERE id = {enemys[i].id}")
                                conn.commit()
                                break
                        else:
                            cur.execute(f"UPDATE Enemys SET enHP = {enemys[i].hp} WHERE id = {enemys[i].id};")
                            conn.commit()
                except TimeoutError:
                    await message.channel.send("待ち時間上限を超えました。処理を中断します")
                finally:
                    cur.close()
                    conn.close()
                    await message.channel.send(content= "```接続を終了します・・・```")
            elif (gameModeStr == "4" or numMode == 4):
                await message.channel.typing()
                time.sleep(0.5)
                try:
                    await message.channel.send("```回数と範囲を指定してね！\n例：?1d5```")
                    wait = await client.wait_for("message",check=check,timeout = 20)
                    while (1):
                        if (wait.content.startswith('?')):
                            j = 0
                            while (1):
                                if (j >= 1):
                                    wait = await client.wait_for ("message",check = check,timeout = 20)
                                num = []
                                dice = wait.content
                                dice = dice.lstrip('?')
                                if (dice.find ('d') == 0):
                                    dice = dice.lstrip('d')
                                    roopN = 1
                                    rangeN = int (dice)
                                else:
                                    num = dice.split('d')
                                    roopN = int(num[0])
                                    rangeN = int(num[1])
                                if (roopN > 20):
                                    await message.channel.send("回数が多すぎるよ！\n20以下にしてね。")
                                    j += 1
                                else:
                                    break
                            i = 0
                            deme = ''
                            while (1):
                                if(i >= roopN):
                                    break
                                jnum = random.randint(1,rangeN)
                                deme += f"出目：{jnum}\n"
                                i += 1
                            await message.channel.send (f"{deme}")
                            break
                        else:
                            await message.channel.send("きめられた形式で入力してね。")
                            wait = await client.wait_for("message",check=check,timeout = 20)
                except asyncio.TimeoutError:
                    await message.channel.send("待ち時間上限を超えました。処理を中断します.")
                    return
            elif (gameModeStr == "5" or numMode == 5):
                try:
                    id = message.author.id
                    name = message.author.name
                    useToken = 0 #使用トークン数概算
                    usages = 0
                    await message.channel.send("{0}さん、こんにちは。私はShatGptです。ChatGptを利用して会話をします。\n3回まで会話を記憶します。\n終了する場合は「さよなら」と入力".format(name))
                    i = 0
                    chatRes = ""
                    while (i < 3):
                        try:
                            wait = await client.wait_for("message", check = check,timeout = 30)
                        except asyncio.TimeoutError:
                            await message.channel.send("{0}さん、待ち時間上限を超えました。処理を中断します.".format(name))
                            return
                        await message.channel.typing()
                        if wait.content == "さよなら" :
                            await message.channel.send("{0}さんから、終了命令を受信しました。処理を中断します.".format(name))
                            return
                        response = openai.ChatCompletion.create(
                            model = "gpt-3.5-turbo",
                            messages = [
                                {
                                    "role": "assistant",
                                    "content": chatRes
                                },
                                {
                                    "role": "user",
                                    "content": wait.content
                                },
                            ],
                        )
                        await message.channel.typing()
                        chatRes = response['choices'][0]['message']['content']
                        await message.channel.send(chatRes)
                        usages += 1
                        useToken += (len(chatRes) + len(wait.content))
                        i += 1
                    await message.channel.send("{0}さん、レスポンスが３回を超えました。会話を終了します".format(name))
                finally:
                    conn = connectDB()
                    cur = conn.cursor()
                    cur.execute(f"SELECT usages,useToken FROM ChatGPTUsages WHERE id = {id}")
                    usageList = cur.fetchall()
                    if(len(usageList) == 0):
                        cur.execute(f"INSERT INTO ChatGPTUsages(id,uName,usages,useToken) VALUES({id},'{name}',{usages},{useToken});")
                        conn.commit()
                    else:
                        usages += usageList[0][0]
                        useToken += usageList[0][1]
                        cur.execute(f"UPDATE ChatGPTUsages SET usages = {usages},useToken = {useToken} WHERE id = {id}")
                        conn.commit()

                    cur.close()
                    conn.close()
            elif(gameModeStr == "6" or numMode == 6):
                return
                
@client.event
async def on_raw_reaction_add(payload):
    global messageId
    global checkEmoji
    global isEmoji
    global selNum
    if payload.member.bot:
        return
    #if payload.message_id == messageId.message_id:
    if(str(payload.emoji) == '1️⃣'):
        selNum = 1
    elif(str(payload.emoji) == '2️⃣'):
        selNum = 2
    elif(str(payload.emoji) == '3️⃣'):
        selNum = 3
    elif(str(payload.emoji) == '4️⃣'):
        selNum = 4
    elif(str(payload.emoji) == '5️⃣'):
        selNum = 5
    elif(str(payload.emoji) == '6️⃣'):
        selNum = 6
    elif(str(payload.emoji) == '7️⃣'):
        selNum = 7
    else:
        selNum = -1
        print(str(payload.emoji))
    isEmoji = True

async def waitChoiceEmoji():
    global isEmoji
    while(isEmoji == False):
        await asyncio.sleep(1)
    isEmoji = False

def connectDB():
    conn = MySQLdb.connect(
        user= '',
        passwd= '',
        host= '',
        db= '',
        port= 3306
    )
    
    return conn


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
