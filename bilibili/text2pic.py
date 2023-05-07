import math
from PIL import Image,ImageFont,ImageDraw

font_conf = {
   'type':'NotoSansCJK-Light',
   'size':20,
   'rgb':tuple([0,0,0])
}
bg_conf = {
    'rgb':tuple([255,255,255])
}
margin=15

def CreateMutiLinesPic(texts:list[str],line_size,pic_path=None):
    """
    Create a fixed-width picture with the height depend on the length of the text
    
    Parameters
    ----------
    text: words to render in picture
    
    line_size: words length per line
    
    pic_path: the path of the new picture to save in if it is not None
        
    Returns
    -------
    None
    """
    line_counts=[math.ceil(len(text)/line_size) for text in texts]
    line_count=sum(line_counts)  # type: ignore
    # print(line_counts)
    font = ImageFont.truetype(font_conf['type'],font_conf['size'])
    
    # calculate the picture size
    fwidth,fheight = font.getsize('中'*line_size)
    owidth,oheight = font.getoffset('中'*line_size)
    pic_size=(margin*2+fwidth+owidth,margin*2+(fheight+oheight)*line_count)
    
    # create new picture
    pic = Image.new('RGB', pic_size,bg_conf['rgb'])
    draw = ImageDraw.Draw(pic)
    i=0
    for index,text in enumerate(texts):
        for ii in range(line_counts[index]):
        # draw lines
            
            draw.text((margin,margin+(fheight+oheight)*i), text[ii*line_size:(ii+1)*line_size], font_conf['rgb'], font)
            i+=1
            # print(i)
    if pic_path:
        pic.save(pic_path)
#     # pic.show()
# text=["无图"]
# # """text=['接到一个需求，将给出的文字自动生成图片。',
# # '要求白底黑字，根据图片尺寸两边预留固定尺寸，文字自动居中。这里的一个难点就是计算文字的字号。',
# # '思路：根据宋体实验找了一下规律，每两个字号渲染尺寸会按双字节加一倍。',
# # '也就是计算出双字个数，通过宽度剪去双边预留尺寸，再除以双字节个数就是字号。']
# # """
# CreateMutiLinesPic(text, 20,'/home/abg/nonebot/Alice/QQbotFiles/bilibili/null.jpg')# my function