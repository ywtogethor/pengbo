#coding:UTF-8

#a = [14,6,9,34,2,6,0,45,12,3]

#while 2>1:
#    for letter in range(len(a)):
#        if letter < len(a)-1 and a[letter] > a[letter+1] :
#            a[letter],a[letter+1] =  a[letter+1],a[letter]
#    print a

class kaka:
    def kk(self,data):
        for letter in range(len(data)):
            if letter < len(data)-1 and data[letter] > data[letter+1] :
                data[letter],data[letter+1] =  data[letter+1],data[letter]
        return data
    
           
if __name__ == "__main__":
    a = [43,6,78,34,88,7,99,45,100,3]
    pass_num = 1
    aa = kaka()
    while pass_num < (len(a)):
        a = aa.kk(a)
        pass_num = pass_num + 1
    print a

