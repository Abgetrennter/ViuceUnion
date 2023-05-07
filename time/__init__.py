# from nonebot_plugin_apscheduler import scheduler
# from pathlib import Path
# import os
# from nonebot.adapters.onebot.v11 import Bot, MessageEvent,Message, MessageSegment
# from nonebot.params import CommandArg
# from nonebot.plugin import on_command
# from nonebot import get_driver, require

# from .config import Config
# require("nonebot_plugin_apscheduler")


# global_config = get_driver().config
# config = Config.parse_obj(global_config)

# fileRoot = config.fileroot + \
#     'set_time/'if config.fileroot else "./QQbotFiles/set_time/"

# if not os.path.exists(fileRoot):
#     os.makedirs(fileRoot)


# # @scheduler.scheduled_job("cron", hour="*/2", id="xxx", args=[1], kwargs={"arg2": 2})
# # async def run_every_2_hour(arg1, arg2):
# #     pass

# ss = on_command("wait")
# @ss.handle()
# async def handle_bd(message: Message = CommandArg()):
#     m=message.extract_plain_text()

#     await bd.send(m)

# scheduler.sched.add_job(my_job, 'date', run_date=date(2009, 11, 6), args=['text'])
