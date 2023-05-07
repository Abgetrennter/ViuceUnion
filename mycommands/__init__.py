from nonebot import get_driver
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, Message, GroupMessageEvent
from nonebot.params import CommandArg
from nonebot.plugin import on_command
from .config import Config
from urllib import parse
from os import popen
from asyncio import sleep
from .spwarm import bquery, wquery
global_config = get_driver().config
config = Config.parse_obj(global_config)


bd = on_command("百度")


@bd.handle()
async def handle_bd(message: Message = CommandArg()):
    m = message.extract_plain_text()
    m = "www.baidu.com/s?wd="+parse.quote(m)
    await bd.send(m)


bkk = on_command("百科摘要")


@bkk.handle()
async def handle_bkk(bot: Bot, event: GroupMessageEvent, message: Message = CommandArg()):
    m = [i.strip() for i in str(message).split()]
    q = []
    for mes in m:
        if not mes:
            continue
        data = bquery(mes)
        if len(data) == 0:
            data = "未找到结果"

        p = {
            "type": "node",
            "data": {
                "name": mes,
                "uin": f"{bot.self_id}",
                "content": data
            },
        }
        q.append(p)
        await sleep(1)

    await bot.send_group_forward_msg(group_id=event.group_id, messages=q)
    # await bd.send(m)


wkk = on_command("wiki摘要")


@wkk.handle()
async def handle_wkk(bot: Bot, event: GroupMessageEvent, message: Message = CommandArg()):
    m = [i.strip() for i in str(message).split()]
    q = []
    for mes in m:
        if not mes:
            continue
        data = wquery(mes)
        if len(data) == 0:
            data = "未找到结果"

        p = {
            "type": "node",
            "data": {
                "name": mes,
                "uin": f"{bot.self_id}",
                "content": data
            },
        }
        q.append(p)
        await sleep(1)
    # type: ignore
    await bot.send_group_forward_msg(group_id=event.group_id, messages=q)


bi = on_command("bing")


@bi.handle()
async def handle_bi(message: Message = CommandArg()):
    m = message.extract_plain_text()
    m = "cn.bing.com/search?q="+parse.quote(m)
    await bi.send(m)


g = on_command("google")


@g.handle()
async def handle_g(message: Message = CommandArg()):
    m = message.extract_plain_text()
    m = "www.google.com/search?q="+parse.quote(m)
    await g.send(m)

i_love_you = on_command("我喜欢你")
@i_love_you.handle()
async def handle_i_love_you(message: Message = CommandArg()):
    await i_love_you.send("谢谢你的喜欢！但你的喜欢，应该给更合适的人。")

water_face = on_command("你就挺合适的")
@water_face.handle()
async def handle_water_face(message: Message = CommandArg()):
    await water_face.send("差不多得了啊😅😅")

pking = on_command("我想去北大")
@pking.handle()
async def handle_pking(message: Message = CommandArg()):
    await pking.send("北大一直是我的梦想，在波光潋滟的未名湖畔，我期待与你的携手。咱们一起努力")


bk = on_command("百科")


@bk.handle()
async def handle_bk(message: Message = CommandArg()):
    m = message.extract_plain_text()
    m = "baike.baidu.com/item/"+parse.quote(m)
    await bk.send(m)


wk = on_command("wiki")


@wk.handle()
async def handle_wk(message: Message = CommandArg()):
    m = message.extract_plain_text()
    m = "https://zh.wikipedia.org/w/index.php?search="+parse.quote(m)
    await wk.send(m)


bz = on_command("bilibili")


@bz.handle()
async def handle_bz(message: Message = CommandArg()):
    m = message.extract_plain_text()
    m = "bilibili.com/search?keyword="+parse.quote(m)
    await bz.send(m)


dy = on_command("抖音")


@dy.handle()
async def handle_dy(message: Message = CommandArg()):
    m = message.extract_plain_text()
    m = "www.douyin.com/search/"+parse.quote(m)
    await dy.send(m)

getip = on_command("getip", permission=SUPERUSER)


@getip.handle()
async def handle_getip():
    s = 'ip address show  enp3s0 | grep "inet " | awk \'{print $2}\''
    with popen(s, 'r') as f:
        await getip.send(f.read())

cmdrun = on_command("cmd", permission=SUPERUSER)


@cmdrun.handle()
async def handle_cmdrun(message: Message = CommandArg()):
    m = message.extract_plain_text()
    with popen(m, 'r') as f:
        await cmdrun.send(f.read())
# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

