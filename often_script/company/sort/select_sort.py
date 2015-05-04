#coding:UTF-8

def max_value(max,data):
     for letter in range(len(data)):
         if data[letter] > max:
             max = data[letter]
             index = letter
     return max

if __name__ == "__main__":
    a = [78,45,23,99,1,34,12,77,45,66]
    b = a[0]
    num = 1
    while num <= len(a):
        b = max_value(b,a)     
        num = num + 1
    print b
