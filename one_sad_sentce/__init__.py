from nonebot import get_driver
from asyncio import sleep
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Event, Message, MessageSegment, GroupMessageEvent
from nonebot.plugin import on_command
from .config import Config
import os
import random


config = Config.parse_obj(get_driver().config)

fileRoot = config.fileroot + \
    'sad_sentence/'if config.fileroot else "./QQbotFiles/sad_sentence/"

if not os.path.exists(fileRoot):
    os.makedirs(fileRoot)

sentences_file = fileRoot+"scentence.txt"

try:
    with open(sentences_file, encoding="utf-8") as f:
        sentences = f.read().split('\n')
except:
    sentences = ["天天摆大烂\t\t好耶！"]
    with open(sentences_file, "w", encoding="utf-8") as f:
        f.write(sentences[0])

sentences = [i.strip().replace("\t\t", "\n") for i in sentences if i.strip()]

get_sentences = on_command("整点薯条", aliases={"来点薯条"})


@get_sentences.handle()
async def handle_one_jz(m: Message = CommandArg()):
    s = str(m)
    # print(s)
    if s.isdigit() and 0 < (i := int(s)) <= len(sentences):
        await get_sentences.finish(f"选用第{s}条\n {sentences[i-1]}")
    if (l := len(sentences)) < 10:
        await get_sentences.send(f"仅有{l}条存货。")
        await sleep(0.5)
    i = random.choice(sentences)
    await get_sentences.finish(i)

add_sentences = on_command("加点薯条")


@add_sentences.handle()
async def handle_more_jz(mm: Message = CommandArg()):
    global sentences
    m = mm.extract_plain_text()
    mmm = m.replace("\n", "\t\t")
    sentences.append(mmm)
    with open(sentences_file, "a", encoding="utf-8") as f:
        f.write("\n"+mmm)
    await get_sentences.finish(f"已添加\n{m}\n现有{len(sentences)}条存货。")

delete_sentences = on_command("删掉薯条")


@delete_sentences.handle()
async def handle_less_jz(m: Message = CommandArg()):
    global sentences
    s = str(m)
    print(s)
    if s.isdigit() and 0 < (i := int(s)) <= len(sentences):
        s = sentences.pop(i-1)
    else:
        s = s.replace("\n", "\t\t").strip()
        if s in sentences:
            sentences.remove(s)
        else:
            await delete_sentences.finish(f"未找到{s}，停止删除")

    with open(sentences_file, "w", encoding="utf-8") as f:
        f.write("\n".join(sentences))
    await get_sentences.finish(f"已删除:{s}\n现有{len(sentences)}条存货。")

list_sentences = on_command("列出薯条")


@list_sentences.handle()
async def handle_list_jz():
    await sleep(0.5)
    l = "\n".join([f"第{index+1}条，{s[:6].strip()}" for index,
                  s in enumerate(sentences)])
    await list_sentences.finish(l)

love_file = fileRoot+"love.txt"
try:
    with open(love_file, encoding="utf-8") as f:
        love = f.read().split('\n')
except:
    love = ["她只是不爱你😘"]
    with open(love_file, "w", encoding="utf-8") as f:
        f.write(love[0])

love = [i.strip().replace("\t\t", "\n") for i in love if i.strip()]

get_love = on_command("整点乐子", aliases={"来点乐子"})


@get_love.handle()
async def handle_one_love(m: Message = CommandArg()):
    s = str(m)
    # print(s)
    if s.isdigit() and 0 < (i := int(s)) <= len(love):
        await get_love.finish(f"选用第{s}条\n {love[i-1]}")
    if (l := len(love)) < 10:
        await get_love.send(f"仅有{l}条存货。")
        await sleep(0.5)
    i = random.choice(love)
    await get_love.finish(i)

add_love = on_command("加点乐子", aliases={"添加乐子"})


@add_love.handle()
async def handle_more_love(mm: Message = CommandArg()):
    global love
    m = mm.extract_plain_text()
    mmm = m.replace("\n", "\t\t")
    love.append(mmm)
    with open(love_file, "a", encoding="utf-8") as f:
        f.write("\n"+mmm)
    await get_love.finish(f"已添加\n{m}\n现有{len(love)}条存货。")

delete_love = on_command("删掉乐子")


@delete_love.handle()
async def handle_less_love(m: Message = CommandArg()):
    global love
    s = str(m)
    print(s)
    if s.isdigit() and 0 < (i := int(s)) <= len(love):
        s = love.pop(i-1)
    else:
        s = s.replace("\n", "\t\t").strip()
        if s in love:
            love.remove(s)
        else:
            await delete_love.finish(f"未找到{s}，停止删除")

    with open(love_file, "w", encoding="utf-8") as f:
        f.write("\n".join(love))
    await get_love.finish(f"已删除:{s}\n现有{len(love)}条存货。")

list_love = on_command("列出乐子")


@list_love.handle()
async def handle_list_love():
    await sleep(0.5)
    l = "\n".join([f"第{index+1}条，{s[:6].strip()}" for index,
                  s in enumerate(love)])
    await list_love.finish(l)


neuro_file = fileRoot+"neuro.txt"
try:
    with open(neuro_file, encoding="utf-8") as f:
        neuro = f.read().split('\n')
except:
    neuro = ["Sometimes when I sit here and stream.I envision myself as a goddess, overlooking my followers as they worship the ground I walk on."]
    with open(neuro_file, "w", encoding="utf-8") as f:
        f.write(neuro[0])

neuro = [i.strip().replace("\t\t", "\n") for i in neuro if i.strip()]

get_neuro = on_command("每日金句")


@get_neuro.handle()
async def handle_get_neuro(m: Message = CommandArg()):
    s = str(m)
    # print(s)
    if s.isdigit() and 0 < (i := int(s)) <= len(neuro):
        await get_neuro.finish(f"选用第{s}条\n {neuro[i-1]}")
    # if (l := len(neuro)) < 10:
    #     await get_neuro.send(f"仅有{l}条存货。")
    #     await sleep(0.5)
    i = random.choice(neuro)
    await get_neuro.finish(i)



neuro_say = on_command("增加金句")
@neuro_say.handle()
async def handle_neuro(mm: Message = CommandArg()):
    global neuro
    m = mm.extract_plain_text()
    mmm = m.replace("\n", "\t\t")
    neuro.append(mmm)
    with open(neuro_file, "a", encoding="utf-8") as f:
        f.write("\n"+mmm)
    await neuro_say.finish(f"已添加\n{m}\n现有{len(neuro)}条存货。")

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass
