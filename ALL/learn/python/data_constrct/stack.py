#coding:UTF-8

class Stack:
    def __init__(self):
        self.item = []
    def is_empty(self):
        return self.item == []
    def push(self,obj):
        self.item.append(obj)
    def pop(self):
        return self.item.pop()


if __name__ == "__main__":
    stack = Stack()
    print(stack.is_empty())
    stack.push("a")
    print stack.pop()
    print stack.item
