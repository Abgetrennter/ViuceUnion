from nonebot import get_driver
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, MessageEvent,Message, MessageSegment
from nonebot.params import CommandArg ,RegexMatched
from nonebot.plugin import on_regex,on_command
from .config import Config
from .text2pic import CreateMutiLinesPic
from urllib import parse
from asyncio import sleep
import os
from json import load,dump
from PIL import Image
from bilibili_api.video import Video
from bilibili_api.user import User
from bilibili_api.live import LiveRoom
global_config = get_driver().config
path=Config.parse_obj(global_config).fileroot+"bilibili/"
if not os.path.exists(path):
	os.makedirs(path)



async def myvideo(v:Video):
    # 实例化 Video 
    # 获取信息
    data:dict = await v.get_info()
    # print(info)  
    if not data :
        return path+'error.jpg',path+'null.jpg'
    
    stat=data['stat']
    s=[f"标题：{ data['title'] }",f" up主:{data['owner']['name']}",f"简介:{data['desc']},{data['dynamic']}".replace("\n","")
      ,f"有{stat['view']}人看过，{stat['coin']}币和{stat['danmaku']}弹幕数，共有{stat['like']}人点赞,{stat['reply']}人评论"]
    
    p=path+str(data['aid'])+'.jpg'
    CreateMutiLinesPic(s,30,p)
    return p,data["pic"]

bv1 = on_regex("[bB][vV][A-Za-z0-9]{10}")
@bv1.handle()
async def handle_bilibili(m: str = RegexMatched()):
    v=Video(bvid="BV"+m[2:])
    p,pp=await myvideo(v)
    m="bilibili.com/video/"+parse.quote(m)
    # print(pp)
    with open(p,'rb') as f:
        s=f.read()
    await bv1.send(Message([m,MessageSegment.image(pp),MessageSegment.image(s)]))

av1 = on_regex("[aA][vV][0-9]*")
@av1.handle()
async def handle_bilibilia(m: str = RegexMatched()):
    v=Video(aid=int(m[2:]))
    p,pp=await myvideo(v)
    m="bilibili.com/video/"+parse.quote(m)
    # print(pp)
    with open(p,'rb') as f:
        s=f.read()
    await av1.send(Message([m,MessageSegment.image(pp),MessageSegment.image(s)]))


def get_dict():
    try:
        with open(path+"id2name.json",encoding='utf-8') as f:
            config:dict[int,dict[str,str]]=load(f)
    except:
        with open(path+"id2name.json",'w',encoding='utf-8') as f:
            config={1265680561:{'name':"永雏塔菲","live":"22603245"}}
            dump(config,f)
    return config

id2name=get_dict()
cv1 = on_regex("space.bilibili.com/[0-9]*")
@cv1.handle()
async def handle_bilibilic(m: str = RegexMatched()):
    global id2name
    uid=int(m.split('/')[-1])
    if uid not in id2name:
        user=User(uid)
        info=await user.get_user_info()
        id2name[uid]={'name':info['name']}
        with open(path+"id2name.json",'w',encoding='utf-8') as f:
            dump(id2name,f)



live = on_command("开播")
@live.handle()
async def handle_blive(m:MessageEvent=CommandArg()):
    text=str(m)
    if text.isdigit():
        q=int(text)
        user=User(q)
    else:
        for id,name in id2name.items():
            if name['name'] == text:
                user=User(int(id))
                break
        await live.finish("没有找到")
    info=await  user.get_live_info()
    if info['liveStatus']:
        await live.send("开播了，{info['url']}")
    else:
        await live.send("没有")
