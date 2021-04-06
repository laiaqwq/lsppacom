import requests
import re
import socket
import time
import traceback

munber = 1
tab = 1000
sleepTime = 1

inUrl = []
proxies = {"http": "http://127.0.0.1:10810", "https": "http://127.0.0.1:10810"}
s = requests.session()
s.keep_alive = False
requests.adapters.DEFAULT_RETRIES = 5
socket.setdefaulttimeout(5)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'
}

for t in range(1, tab):
    print("开始下载第"+str(t)+"页")
    try:
        response = requests.get('https://konachan.com/post?page=' + str(t), headers=headers, proxies=proxies)
        outHtml = response.text
        # print(outHtml)
        tuUrl = re.findall('<a class="thumb" href=".*?">', outHtml)
        print(tuUrl)

        print("图片数量"+str(len(tuUrl)))

        # 获取地址

        for i in tuUrl:
            print("列表切片"+i)
            inUrl.append(i[23:91])  # 24 92

        # 地址切片

        for p in inUrl:
            try:
                response = requests.get('https://konachan.com/' + str(p), headers=headers, proxies= proxies)
                outHtml = response.text
                pngurl = re.findall('<a class="original-file-.*?" href=".*?" id="png">.*?</a>', outHtml)
                print(pngurl)
                if pngurl:
                    pngDownurl = re.findall('href=".*?" id="png">',str(pngurl))
                    print(pngDownurl)
                    pngDown = str(pngDownurl)[8:-13]
                    print(pngDownurl)
                    # png地址截取
                    print("开始下载原图"+str(munber))
                else:
                    pngurl = re.findall('<a class="original-file-.*?" href=".*?" id=".*?">Download larger version .*?/a>', outHtml)
                    print(pngurl)
                    pngurl = re.findall('href=".*?" id="highres">', str(pngurl))
                    print(pngurl)
                    pngDown = str(pngurl)[8:-17]
                    print(pngDown)
                    # png地址截取
                    print("开始下载大图")
                png = requests.get(pngDown, headers=headers, proxies=proxies)
                fileName = str(munber) + pngDown[-4:]
                print(fileName)

                with open(fileName, 'ab') as f:
                    f.write(png.content)
                    f.close()
                print("第" + str(munber) + "张下载完成")
                munber += 1
                time.sleep(sleepTime)
                    # 下载图片
            except:
                print("can't download or save of " + str(munber))
                traceback.print_exc()


        print(inUrl)
        time.sleep(sleepTime)
        inUrl = []
        print(t)
    except:
        print("cant")
        print(traceback.print_exc())