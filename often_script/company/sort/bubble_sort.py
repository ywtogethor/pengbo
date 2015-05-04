#coding:UTF-8
def one_sort(data):
    for letter in range(len(data)):
        if letter <len(data)-1 and data[letter] > data[letter+1]:
            data[letter],data[letter+1] = data[letter+1],data[letter]
    return data       

if __name__ == "__main__":
    a = [78,45,23,99,1,34,12,77,45,66] 
    num = 1
    while num <= len(a):
        a = one_sort(a)
        num = num + 1
    print a
    
            
    
    
