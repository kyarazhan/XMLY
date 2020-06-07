import requests
import pprint
import parsel
import re

# 浏览器伪装
headers = {
        'user-agent': '"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"'
}

#定义一个下载方法
def download_media(id_,name):
   #代码块 函数 方法
    #根据网址请求服务器
    response = requests.get('https://www.ximalaya.com/revision/play/v1/audio?id=' + str(id_)+ '&ptype=1',headers=headers)
    #字典类型
    data =response.json()
    #漂亮的打印
#    pprint.pprint(data)
    #键值对
    src = data['data']['src']
    print(src)

   #根据网址 请求服务器 拿到数据
    response = requests.get(src)
#    print(response)

    with open(name+'.mp3','wb') as f:
        f.write(response.content)

#清除存储命名中的文件非法字符
def validateTitle(title):
    # '/ \ : * ? " < > |'
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    #多空格
    rstr_1 = r"  "
    rstr_2 = r"   "
    # 非法字符替换为空格
    new_title_1 = re.sub(rstr, " ", title)
    # 双空格替换为单空格
    new_title_2 = re.sub(rstr_2, " ", new_title_1)
    # 三空格替换为单空格
    new_title = re.sub(rstr_1, " ", new_title_2)
    return new_title

"""
def serial(title):

    for serial_ in range(1,main_.serial_1):
        new_title = str(serial_)+title
        return new_title
"""

def main_():
    link = input("请输入地址栏链接:")
    page_ = int(input("请输入总共页数:"))+1
    for page in range(1, page_):
        response = requests.get(link+'p'+str(page)+'/', headers=headers)
#        print(response.text)
        sel = parsel.Selector(response.text)
        a_s = sel.css('.sound-list ul li a')
        for a in a_s[:30]:
            #获取文件名
            title = a.css('a::attr(title)').get()
            #调用清除存储命名中的文件非法字符的方法
            title = validateTitle(title)
            #获取文件后半链接
            url = a.css('a::attr(href)').get()

            id_ = url.split('/')[-1]
            print(title, id_)
            # 调用下载方法
            download_media(id_, title)

if __name__ == '__main__':
    print("喜马拉雅 免费产品 专用下载器！\n请输入下载链接,例如：https://www.ximalaya.com/yinyue/22886272/\n")
    main_()