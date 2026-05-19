label naming:
    
    scene black with fade

    # 如果已经选择了一个名字：
    if persistent.name_mc:
        $ name_mc = persistent.name_mc
        qqq "{......}噢，{w=0.25}又见面了，{w=0.5}[name_mc]。"
        qqq "我想，{w=0.5}我们应该没必要再给你重新想个名字了吧？"
        qqq "那就让我们进入剧情吧。"
        qqq "呃，如果我没记错的话，剧情应该是被我放在{...}"
        return
    
    qqq "{......}噢，{w=0.25}嘿，{w=0.5}你好。"
    qqq "我想，{w=0.25}你应该就是玩家了。"
    qqq "首先，{w=0.5}感谢你愿意游玩我们的作品。"
    # yangsy "谁家 B-X 感谢你玩我们的游戏（"
    qqq "{......}"
    qqq "该死的，{w=0.25}我又忘记我要说什么了。"
    qqq "抱歉，{w=0.25}我早该在这之前准备好文案的，{w=0.25}我总是这样。"
    qqq "算了，{w=0.25}既然如此，{w=0.5}不妨先取个名字？"

    "试着给自己想个名字？{w=2.5}{nw}"

    qqq "——啊，{w=0.25}不好意思，{w=0.5}我得提醒你一下。"
    qqq "尽管这个游戏理论上是完全离线的，{w=0.5}但是——"
    qqq "不论如何，{w=0.5}在任何的地方暴露你的真实姓名都是一种\n{w=0.25}{red}{cps=*0.25}极其危险的行为{/cps}{/red}。"
    qqq "尽管我并不会限制你输入自己的名字（我的程序也没办法识别），\n{w=0.25}但还是请你{red}{cps=*0.5}一定一定不要这么做{/cps}{/red}，{w=0.25}好吗？{nw}"
    $ _history_list.pop()
    menu:
        qqq "尽管我并不会限制你输入自己的名字（我的程序也没办法识别），\n但还是请你{red}一定一定不要这么做{/red}，好吗？{fast}"
        "当然可以。":
            pass

    qqq "唔，{w=0.25}看来选择模块运行正常。"
    qqq "实在是不好意思，{w=0.5}让不知情的你参与了一下调试。"
    qqq "我不太擅长调用这些功能，{w=0.5}所以有时可能会出现一些小错误。"
    qqq "非常感谢你的配合。"
    qqq "咳咳，{w=0.25}扯远了。"

    jump naming_loop


label naming_loop:

    "试着给自己想个名字？{nw}"
    python:
        import time, string, unicodedata, os

        start_time = time.time()
        name_mc = renpy.input(_("试着给自己想个名字？")).strip()
        end_time = time.time()
        delta_time = end_time - start_time

    python:
        currentuser = ""
        for name in ("LOGNAME", "USER", "LNAME", "USERNAME"):
            user = os.environ.get(name)
            if user:
                currentuser = user
    
    # 如果输入的名字为空：
    if not name_mc:
        yangsy "诶等会输入的名字为空这种情况竟然没剧情的吗（"
        jump naming_loop
    
    # 否则，如果输入名字所花费的时间短于一秒：
    elif delta_time < 1:
        qqq "哇，{w=0.25}你的速度可真快，只用了[delta_time:.3f]秒就{...}"
        qqq "{...}你大概只是乱敲了下键盘吧，{w=0.25}我猜。"
        qqq "也许你是个速通玩家，{w=0.5}谁知道呢？"
        qqq "我反正不明白为什么一个galgame也会有人尝试速通。"
        jump naming_done
    
    # 否则，如果输入的名字是administrator等管理员用户名：
    elif name_mc.lower() in ("admin", "administrator", "system", "root", "wheel", currentuser.lower()):
        qqq "{......}我不明白。"
        # qqq "我应该没有调用获取系统账户名称的API吧{......}"
        # yangsy "有的兄弟有的（"
        qqq "你是觉得这样做就能获得什么“{green}管理员权限{/green}”之类的？"
        qqq "谁知道呢，{w=0.5}说不定某次更新之后作者就会为这个加点什么？"
        jump naming_done
    
    # 否则，如果输入的名字是qwq/awa等：
    elif name_mc.lower() in ("qwq", "awa", "uwu", "xwx"):
        qqq "[name_mc]"
        jump naming_done
    
    # 否则，如果输入的名字含有特殊符号（通过检查Unicode字符分类判断）：
    elif any(unicodedata.category(c) in ("So", "Zl", "Zp", "Cc", "Cf", "Cs", "Co", "Cn") for c in name_mc):
        qqq "虽然说输入框能支持，{w=0.25}但是{...}"
        qqq "你取个这样的名字，{w=0.5}我该怎么念呢？"
        qqq "还是说你在聊天框里塞了颜文字？{w=1.0}我的程序检测不出来。"
        jump naming_done

    # 否则，如果输入的名字长度大于20个字符：
    elif len(name_mc) > 20:
        qqq "哇，{w=0.25}这可真是一个很长的名字。"
        qqq "不过这么长的名字，{w=0.5}我可不确定UI能不能适配。"
        qqq "也许换个名字是个更好的选择？"
        jump naming_loop

    # 否则，如果输入的名字长度小于3字节：
    elif len(bytes(name_mc, encoding="utf-8")) < 3:
        qqq "看的出来，{w=0.5}你并不擅长取名字。"
    
    # 否则，如果输入的名字是纯数字：
    elif all(c in string.digits for c in name_mc):
        qqq "纯数字吗，{w=0.5}真是无趣，{w=0.5}像是系统分配的一样。"
        jump naming_done
    
    # 否则，如果输入的名字是纯英文字符（A-Z,a-z,0-9）：
    elif all(c in string.digits + string.ascii_letters for c in name_mc):
        qqq "英文字符，{w=0.5}很聪明的选择。"
        qqq "虽然输入框可以支持中文，{w=0.5}但是纯英文的兼容性往往更好。"
        qqq "看来你对这方面的知识的确有一点了解。"
        jump naming_done



label naming_done:

    "确定要使用这个名字吗，[name_mc]？{nw}"
    $ _history_list.pop()
    menu:
        "确定要使用这个名字吗，[name_mc]？{fast}"
        "当然。": 
            $ persistent.name_mc = name_mc
        "我再想想......": 
            jump naming_loop
    
    qqq "好的，{w=0.25}看来你想好自己叫什么了。"
    qqq "不过我还是叫你玩家吧，{w=0.5}我还是习惯这么叫你。\n{w=1.0}（主要是代码写起来方便点）"
    # yangsy "其实使用[name_mc]的名字并不麻烦就是了（"
    qqq "啊，{w=0.25}好奇我的名字吗，{w=0.5}我想这并不重要。"
    qqq "稍等一下，{w=0.5}我得找找剧情被我放在哪了{......}"
    
    scene black with fade
    return


label ut_naming:
    scene black with fade

    if persistent.name_mc:
        $ name_mc = persistent.name_mc
        mc "A name has already been chosen."
    else:
        call ut_naming_loop
    
    scene black with fade
    return


label ut_naming_loop:
    "Name the main character.{nw}"
    $ name_mc = renpy.input(_("Name the main character.{fast}"), length=56).strip()
    if not name_mc:
        "You must choose a name."
        jump ut_naming_loop
    # elif any(name_mc.lower() in n for n in ["ashell", "阿希尔"]):
    #     character.ashell("大概是取名彩蛋对话啥的")
    #     jump naming_loop
    # elif name_mc.lower() == "你的名字":
    #     name_mc = "韦一敏"
    mc "Is this name correct?{nw}"
    $ _history_list.pop()
    menu:
        mc "Is this name correct?{fast}"
        "Yes":
            $ persistent.name_mc = name_mc
            return
        "No":
            jump ut_naming_loop
