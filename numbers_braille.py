
numbers = ['1', '2','3', '4', '5','6','7','8','9','0']

numbers2n= [0x10,0x30,0x11,0x13,0x12,0x31,0x33,0x32,0x21,0x23]


number_n = 0x47

b1 = {n:l for l, n in zip(numbers, numbers2n)}

def encode(numbers):
    letters = ""
    is_num= False
    for num in numbers:
        if num == number_n:
            is_num= True; continue
        else:
            if is_num:
                letters += b1[num]
    return letters

if __name__ == '__main__':

# 490
    h = [71, 19, 33, 35]
    # print(h)
    u = encode(h)
    print(u)