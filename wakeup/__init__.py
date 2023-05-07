from nonebot import get_driver
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import  Event, Message, MessageSegment, GroupMessageEvent
from nonebot.plugin import on_command
from .config import Config
import os,time,base64


config = Config.parse_obj(get_driver().config)

fileRoot=config.fileroot+'check/'if config.fileroot else "/home/abg/nonebot/Alice/QQbotFiles/check/"

if not os.path.exists(fileRoot):
	os.makedirs(fileRoot)
    


async def base64_path(path: str):
    ff = "空"
    with open(path, "rb") as f:
        ff = base64.b64encode(f.read()).decode()
    return f"base64://{ff}"

def get_checked(uid:str):
	date=str(time.strftime("%Y-%m-%d--%H:%M", time.localtime()))
	
	upath = fileRoot + str(uid)+'.csv'
	if not os.path.exists(upath):
		with open(upath,'w',encoding='utf-8') as f :
			f.write(date)
		return False
	with open(upath,'r',encoding='utf-8') as f:
		dates=f.read().split(",")
	if dates[-1].split('--')[0]==date.split('--')[0]:
		return True
	else :
		with open(upath,'a',encoding='utf-8') as f:
			f.write(","+date)
		return False
	
check = on_command("签到")	
@check.handle()
async def handle_check(ev: Event):
	uid=ev.get_user_id()
	th=time.localtime(time.time()).tm_hour
	if not get_checked(str(uid)):
		await check.send(f"签到成功，您是{th}点签到的")
		
		if th<8:
			await check.send(MessageSegment.image(await base64_path(fileRoot+'100.jpg')))
		elif th<9:
			await check.send(MessageSegment.image(await base64_path(fileRoot+'0.jpg')))
		else :
			await check.send(MessageSegment.image(await base64_path(fileRoot+'1.jpg')))
	else:
		await check.send("签过了")
    		
gn = on_command("晚安")	
@gn.handle()
async def handle_gn(ev: Event):
	th=time.localtime(time.time()).tm_hour
	await check.send(f"都{th}点了，还不快睡🕛🕛🕛")
		
	if 18<th<22:
		await gn.send(MessageSegment.image(await base64_path(fileRoot+'100.jpg')))
	elif 22<th<23:
		await gn.send("缺张60分捏")
	else :
		await gn.send(MessageSegment.image(await base64_path(fileRoot+'0.jpg')))

checklist = on_command("签到历史")	
@checklist.handle()
async def handle_checklist(ev: Event):
	uid=ev.get_user_id()
	upath = fileRoot + str(uid)+'.csv'
	if not os.path.exists(upath):
		await checklist.send("无记录") 
	with open(upath,'r',encoding='utf-8') as f:
		dates=f.read()
	await checklist.send(dates)
    	
# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

