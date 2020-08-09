
al = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u'
           ,'v','w','x','y','z']

cap = ['A','B','C','D','E','F','G','H','I','J','K','L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
       'V', 'W',' X',' Y','Z']


cap_n = 0x04
al2n= [0x10, 0x30, 0x11, 0x13, 0x12, 0x31, 0x33, 0x32, 0x21, 0x23, 0x50, 0x70, 0x51, 0x53, 0x52, 0x71, 0x73, 0x72, 0x61, 0x63, 0x54, 0x74, 0x27, 0x55, 0x57, 0x56]




b1 = {n:l for l, n in zip(al, al2n)}
b1cap = {n:l for l, n in zip(cap, al2n)}


def encode(numbers):
    letters = ""
    is_cap = False
    for num in numbers:
        # num = hex(num)
        if num == cap_n:
            is_cap= True; continue
        else:
            if is_cap:

                letters += b1cap[num]
            else:
                # print(b1)
                letters += b1[num]
            is_cap = False
            print(letters)
    return letters

if __name__ == '__main__':
    h = [50, 18, 112, 112, 82]
    # h = [hex(_h) for _h in h]
    # print(h)
    u = encode(h)
    print(u)
