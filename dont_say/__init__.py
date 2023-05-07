from nonebot import get_driver
import re
import base64
from json import load, dump
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg
from asyncio import sleep
from .config import Config
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment, GroupMessageEvent
from nonebot.plugin import on_message, on_command
from nonebot.typing import T_State

from pathlib import Path
from nonebot import require

require("nonebot_plugin_localstore")

import nonebot_plugin_localstore as store

async def base64_path(path: str|Path):
    ff = "空"
    with open(path, "rb") as f:
        ff = base64.b64encode(f.read()).decode()
    return f"base64://{ff}"


file_root: Path = store.get_data_dir("mingan")
config_root:Path=store.get_config_dir("mingan")

#敏感词
if (ww:=file_root/"words.txt").exists():
    with open(ww, encoding='utf-8') as f:
        words = set(_.strip() for _ in f.read().split() if _.strip())
else:
    with open(ww, 'w', encoding='utf-8') as f:
        f.write("丁真")
    words={"丁真"}

#得分
if (dd:=file_root/"score.json").exists():
    with open(dd, encoding='utf-8') as f:
        scores: dict[str, float] = load(f)
else:
    with open(dd, 'w', encoding='utf-8') as f:
        scores: dict[str, float] = {"514": 100}
        dump(scores, f)

#配置
if (cc:=config_root/"config.json").exists():
    with open(cc, encoding='utf-8') as f:
        myconfig: dict[str, float | str] = load(f)
else:
    with open(cc, 'w', encoding='utf-8') as f:
        myconfig: dict[str, float | str] = {
                "delay": 0.5,
                "powerful": 2,
                "tip": "请谨言慎行"
            }
        dump(myconfig, f)






async def write_score():
    with open(dd, "w", encoding="utf-8") as f:
        dump(scores, f)

sa = on_command("信誉分", permission=SUPERUSER)


@sa.handle()
async def sa_handle():
    m = "\n".join([f"{i}:{scores[i]}"for i in scores])
    await sa.send(m)
    await write_score()


ad = on_command("addword", block=True)
@ad.handle()
async def addword_handle(keys: Message = CommandArg()):
    global words
    new_words = [i.strip() for i in str(keys).split()]
    new_words = set([i for i in new_words if i])
    words.update(new_words)

    with open(ww, "a", encoding="utf-8") as f:
        for i in new_words:
            f.write("\n"+i)

    new_words = "  ".join(new_words)
    # print(new_words)
    await ad.finish("已添加 "+new_words)


def isforbiden() -> Rule:
    async def isforbiden_(bot: Bot, event: Event, state: T_State) -> bool:
        if event.get_type() != "message":
            return False
        else:
            msg = str(event.get_message())
            if s := check(msg):
                state['donot_say'] = s
                return True
            else:
                return False

    return Rule(isforbiden_)


def check(msg: str) -> list[str]:
    l = []
    for word in words:
        if word in msg:
            l.append(word)

    if myconfig["powerful"] == 1:
        msg = re.sub(r'[\W]', '', msg)

        for word in words:
            if word in msg:
                l.append(word)

    return l

fd = on_message(rule=isforbiden(), priority=999)
@fd.handle()
async def getwords(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = event.get_plaintext()
    mid = event.message_id
    # words = state['ssss']
    words: list[str] = state.get('donot_say', check(msg))
    # if 'ssss' in state:
    #     words=state['ssss']
    # else :
    #     words= check(msg)
    if not words:
        # print("no")
        return
    id = str(event.user_id)
    scores[id] = scores.get(str(id), 100)-len(words)
    await sleep(float(myconfig["delay"]))
    name = event.sender.card or event.sender.nickname or id  # 我真是个小天才

    words = ["😨".join(i) for i in words]
    tip = Message([MessageSegment.reply(mid),
                   f"关键词: {','.join(words)}\n",
                   f"{name}仅剩{scores[id]}分",    # type: ignore
                    MessageSegment.image(await base64_path(file_root.joinpath('dont_say.jpg')))])
    # print(tip)
    await write_score()
    if myconfig["powerful"] == 2:
        await fd.finish(tip)

    # print(tip)
    try:
        await bot.delete_msg(message_id=mid)
    except:
        await fd.send("Cann't drop back")
    await fd.finish(tip)
