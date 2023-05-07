import urllib.request
import urllib.parse
from lxml import etree
httpproxy_handler = urllib.request.ProxyHandler({"http" : "127.0.0.1:7890","https":"127.0.0.1:7890"})
opener = urllib.request.build_opener(httpproxy_handler,urllib.request.HTTPHandler)
urllib.request.install_opener(opener)
def bquery(content):
    # 请求地址
    url = 'https://baike.baidu.com/item/' + urllib.parse.quote(content)
    # 请求头部
    headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36' 
    }
    # 利用请求地址和请求头部构造请求对象
    req = urllib.request.Request(url=url, headers=headers, method='GET')
    # 发送请求，获得响应
    response = urllib.request.urlopen(req)
    # 读取响应，获得文本
    text = response.read().decode('utf-8')
    # 构造 _Element 对象
    html = etree.HTML(text)
    # 使用 xpath 匹配数据，得到匹配字符串列表
    sen_list = html.xpath('//div[contains(@class,"lemma-summary") or contains(@class,"lemmaWgt-lemmaSummary")]//text()') 
    # 过滤数据，去掉空白
    sen_list_after_filter = [item.strip('\n') for item in sen_list]
    # 将字符串列表连成字符串并返回
    return ''.join(sen_list_after_filter)

def wquery(content):
    # 请求地址
    url = 'https://zh.wikipedia.org/wiki/' +  urllib.parse.quote(content)
    # 请求头部
    headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36' 
    }
    # 利用请求地址和请求头部构造请求对象
    req = urllib.request.Request(url=url, headers=headers, method='GET')
    # 发送请求，获得响应
    response = urllib.request.urlopen(req)
    # 读取响应，获得文本
    text = response.read().decode('utf-8')
    # 构造 _Element 对象
    html = etree.HTML(text)
    # 使用 xpath 匹配数据，得到 <div class="mw-parser-output"> 下所有的子节点对象
    obj_list = html.xpath('//div[@class="mw-parser-output"]/*')
    # 在所有的子节点对象中获取有用的 <p> 节点对象
    for i in range(0,len(obj_list)):
        if 'p' == obj_list[i].tag:
            start = i
            break
    for i in range(start,len(obj_list)):
        if 'p' != obj_list[i].tag:
            end = i
            break
    p_list = obj_list[start:end]
    # 使用 xpath 匹配数据，得到 <p> 下所有的文本节点对象
    sen_list_list = [obj.xpath('.//text()') for obj in p_list]
    # 将文本节点对象转化为字符串列表
    sen_list = [sen.encode('utf-8').decode() for sen_list in sen_list_list for sen in sen_list]
    # 过滤数据，去掉空白
    sen_list_after_filter = [item.strip('\n') for item in sen_list]
    # 将字符串列表连成字符串并返回
    return ''.join(sen_list_after_filter)


if __name__ == '__main__':
    while (True):
        content = input('查询词语：')
        result = query(content)
        if len(result):
            print("查询结果：%s" % result,len(result))
