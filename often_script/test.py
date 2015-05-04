#coding:UTF-8
import requests
import re
import json

class kaka:
    def request(self,url):
        response = requests.request("get",url,allow_redirects=False)
        head = response.headers
        return head    

if __name__ == "__main__":
    kk = kaka()
    url = "http://detail.tmall.hk/hk/item.htm?id=38907127875" 
    head = kk.request(url)
    while "location" in head:
        re_location = re.search("location': '([^,]+)',",str(head))
        url = re_location.group(1)
        print url
        print "===================="
        head = kk.request(url)
    


