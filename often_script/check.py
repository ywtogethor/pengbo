#coding:UTF-8

import requests

class kaka:
    def request(self,url):
        response = requests.request("get",url,allow_redirects=False)
        return response


if __name__ == "__main__":
    kk = kaka()
    resource = open("tmall_product.txt")
    content = resource.readline()
    content = content.strip()
    while content:
        url = "http://detail.tmall.hk/hk/item.htm?id="+content+"&tbpm=3"
        response = kk.request(url)
        if response.status_code == 200:
            file = open("200_code","a+")
            file.write("200"+"\n")
            file.close()
        if response.status_code == 302:
            file = open("302_code.txt","a+")
            file.write("产品ID："+content+"\n")
            file.write("状态码："+str(response.status_code)+"\n")
            file.write("响应头部："+str(response.headers)+"\n")
            file.write("========================================================================="+"\n")
            file.close()
        if response.status_code != 200 and response.status_code != 302:
            file = open("else_code.txt","a+")
            file.write("产品ID："+content+"\n")
            file.write("状态码："+str(response.status_code)+"\n")
            file.write("响应头部："+str(response.headers)+"\n")
            file.write("========================================================================"+"\n")
            file.close()
        content = resource.readline()
        content = content.strip()
    resource.close()

