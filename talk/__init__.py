from nonebot.plugin import on_command,on_message
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Message,Bot, Event
from nonebot.typing import T_State
from nonebot.params import CommandArg,ArgPlainText,EventPlainText
from pathlib import Path
from nonebot import require
from json import dump,load
from nonebot.rule import Rule
require("nonebot_plugin_localstore")

import nonebot_plugin_localstore as store

talkspath:Path=store.get_data_file("自定义对话","1.json")
if talkspath.exists():
    with open(talkspath,encoding='utf8') as f:
      talks:dict[str,str]=load(f)
else:
    with open(talkspath,'w',encoding='utf8') as f:
        talks:dict[str,str]={"我喜欢你":"谢谢你的喜欢！但你的喜欢，应该给更合适的人。",
                               "你就挺合适的":"差不多得了啊😅😅",
                               "我想去北大":"北大一直是我的梦想，在波光潋滟的未名湖畔，我期待与你的携手。咱们一起努力"}
        dump(talks,f,ensure_ascii=False)

def dealtext()->Rule:
    async def dealtext_(event: Event, state: T_State) -> bool:
        if event.get_type() != "message":
            return False
        else:
            msg = str(event.get_message())
            return any(i==msg for i in talks)

    return Rule(dealtext_)

ttalks=on_message(rule=dealtext(), priority=950,block=True)
@ttalks.handle()
async def _(msg:str = EventPlainText()):
    await ttalks.finish(talks.get(msg,"怎么回事呢？"))

def talksadd(key:str,value:str):
    talks[key]=value
    with open(talkspath,'w',encoding='utf8') as f:
        dump(talks,f,ensure_ascii=False)
    

add_talks=on_command("加入对话",aliases={'addtalks'})
@add_talks.handle()
async def handle_function(matcher: Matcher, state:T_State,args: Message = CommandArg()):
    talk=args.extract_plain_text().strip()
    if talk:
      matcher.set_arg("tobot", args) 
    


@add_talks.got("tobot", prompt="请输入To Bot")
async def got_tobot(matcher: Matcher,state:T_State,tobot: str = ArgPlainText()):
    state['tobot']=tobot
    await add_talks.send("已添加To Bot")


@add_talks.got("touser", prompt="请输入To User")
async def got_location(state:T_State,touser: str = ArgPlainText()):
    talksadd(state['tobot'],touser)
    await add_talks.finish("已加入肯德基豪华午餐")


