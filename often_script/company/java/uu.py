#coding:UTF-8

class kaka:
    a = 10
    b = 20
    def __init__(self,data):
        print data
    def method(self):
        print self.a+self.b

if __name__ == "__main__":
    kk = kaka("123")
    kk.method()
