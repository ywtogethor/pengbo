#coding:UTF-8

class Queue:
    def __init__(self):
        self.item = []
    def inq(self,item):
        self.item.insert(0,item)
    def outq(self):
        return self.item.pop()


if __name__ == "__main__":
    q = Queue()
    q.inq("a")
    q.inq("b")
    print q.item
    print q.outq()
    print q.item
