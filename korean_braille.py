u1l = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
u1n = [i * 21 * 28 + 0xac00 for i in range(19)]
u2l = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
u2n = [i * 28 for i in range(21)]
u3l = [' ', '.ㄱ', '.ㄲ', '.ㄳ', '.ㄴ', '.ㄵ', '.ㄶ', '.ㄷ', '.ㄹ', '.ㄺ', '.ㄻ', '.ㄼ', '.ㄽ', '.ㄾ', '.ㄿ', '.ㅀ', '.ㅁ', '.ㅂ', '.ㅄ', '.ㅅ', '.ㅆ', '.ㅇ', '.ㅈ', '.ㅊ', '.ㅋ', '.ㅌ', '.ㅍ', '.ㅎ']
u3n = [i for i in range(28)]



u1 = {l:n for l, n in zip(u1l, u1n)}
u2 = {l:n for l, n in zip(u2l, u2n)}
u3 = {l:n for l, n in zip(u3l, u3n)}


b1l = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
b1n = [0x01, 0x11, 0x21, 0x02, 0x12, 0x03, 0x04, 0x05, 0x06, 0x31, 0x32, 0x13, 0x23]

b2l = ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ' ,'ㅡ', 'ㅣ', 'ㅐ', 'ㅔ', 'ㅖ', 'ㅘ', 'ㅚ', 'ㅝ', 'ㅢ', '$']
b2n = [0x34, 0x43, 0x61, 0x16, 0x54, 0x45, 0x51, 0x15, 0x25, 0x52, 0x72, 0x53, 0x41, 0x74, 0x57, 0x71, 0x27, 0x72]

b3l = ['.ㄱ', '.ㄴ', '.ㄷ', '.ㄹ', '.ㅁ', '.ㅂ', '.ㅅ', '.ㅇ', '.ㅈ', '.ㅊ', '.ㅋ', '.ㅌ', '.ㅍ', '.ㅎ', '.ㅆ']
b3n = [0x10, 0x22, 0x42, 0x20, 0x24, 0x30, 0x40, 0x66, 0x50, 0x60, 0x62, 0x64, 0x26, 0x46, 0x41]

b4l = [('ㄱ', 'ㅏ'), ('ㅅ', 'ㅏ')] # ('ㅇ', 'ㅓ', '.ㄱ'), ('ㅇ', 'ㅓ', '.ㄴ'), ('ㅇ', 'ㅓ', '.ㄹ'), ('ㅇ', 'ㅕ', '.ㄴ'), ('ㅇ', 'ㅕ', 'ㄹ'), ('ㅇ', 'ㅕ', '.ㅇ'), ('ㅇ', 'ㅗ', '.ㄱ'), ('ㅇ', 'ㅗ', '.ㄴ'), ('ㅇ', 'ㅗ', '.ㅇ'), ('ㅇ', 'ㅜ', '.ㄴ'), ('ㅇ', 'ㅜ', '.ㄹ'), ('ㅇ', 'ㅡ', '.ㄴ'), ('ㅇ', 'ㅡ', '.ㄹ'), ('ㅇ', 'ㅣ', '.ㄴ')]
b4n = [0x35, 0x70]

b1 = {n:l for l, n in zip(b1l, b1n)}
b2 = {n:l for l, n in zip(b2l, b2n)}
b3 = {n:l for l, n in zip(b3l, b3n)}
b4 = {n:l for l, n in zip(b4l, b4n)}


fortis = {
    'ㄱ':'ㄲ',
    'ㄷ':'ㄸ',
    'ㅂ':'ㅃ',
    'ㅅ':'ㅆ',
    'ㅈ':'ㅉ'}

db = {
    ('.ㄱ', '.ㅅ'):('.ㄳ'),
    ('.ㄱ', '.ㄱ'):('.ㄲ'),
    ('.ㄴ', '.ㅈ'):('.ㄵ'),
    ('.ㄴ', '.ㅎ'):('.ㄶ'),
    ('.ㄹ', '.ㄱ'):('.ㄺ'),
    ('.ㄹ', '.ㅁ'):('.ㄻ'),
    ('.ㄹ', '.ㅂ'):('.ㄼ'),
    ('.ㄹ', '.ㅅ'):('.ㄽ'),
    ('.ㄹ', '.ㅌ'):('.ㄾ'),
    ('.ㄹ', '.ㅍ'):('.ㄿ'),
    ('.ㄹ', '.ㅎ'):('.ㅀ'),
    ('.ㅂ', '.ㅅ'):('.ㅄ'),
    ('.ㅅ', '.ㅅ'):('.ㅆ')
}    


combi = {
    'ㅑ':'ㅒ',
    'ㅘ':'ㅙ',
    'ㅝ':'ㅞ',
    'ㅜ':'ㅟ'
}


def encode(numbers):
    #1단계, 숫자를 기호로 바꾸고 된소리 이중모음 이중자음 처리
    arr1 = []
    for num in numbers:
        prev = None
        if len(arr1) > 0:
            prev = arr1[-1]
        #초성
        if num in b1:
            letter = b1[num]
            #쌍자음 처리
            if letter == 'ㅅ' and prev in fortis:
                arr1[-1] = fortis[prev]
            else:
                arr1.append(letter)
        #중성
        elif num in b2:
            letter = b2[num]
            
            #이중모음
            if letter == '$':
                if prev is None:
                    print('첫 글자는 이중모음이 될 수 없습니다.')
                    continue
                elif prev not in combi:
                    print('이중모음 앞에는 반드시 ㅑ, ㅘ, ㅝ, ㅜ 중 하나가 와야 합니다.')
                    continue
                else:
                    arr1[-1] = combi[prev]
            else:
                arr1.append(letter)
        elif num in b3:
            letter = b3[num]
            
            if prev is None or prev not in b3l:
                arr1.append(letter)
            elif (prev, letter) in db:
                arr1[-1] = db[(prev, letter)]
            else:
                print('허용될 수 없는 이중 종성입니다.')
                continue
        elif num in b4:
            letters = b4[num]
            for letter in letters:
                arr1.append(letter)
        else:
            print('알 수 없는 문자입니다.')
    #2단계
    #모음앞에 자음이 없으면 ㅇ 삽입
    arr2 = []
    for letter in arr1:
        #모음이고
        if letter in u2l:
            #앞에 자음이 아니면
            if len(arr2) == 0 or arr2[-1] not in u1l:
                arr2.append('ㅇ')            
        arr2.append(letter)
    
    #3단계 유니코드로 바꾼다.
    result = ''
    merge = 0
    for letter in arr2:
        if letter in u1l:
            #이전 글자 작업
            if merge != 0:
                result += chr(merge)
            #자음 처리
            merge = u1[letter]
        elif letter in u2l:
            merge += u2[letter]
        elif letter in u3l:
            merge += u3[letter]
        else:
            print('허용되지 않는 문자입니다.')
            continue
    #마지막
    result += chr(merge)
    print(arr1)
    print(arr2)
    return result


if __name__ == '__main__':
    samples = ['ㄱ', 'ㅏ', 'ㅜ', '$', 'ㄷ', 'ㅅ', 'ㅏ', '.ㄹ', '.ㄱ', 'ㅌ', 'ㅡ']
    rb = {l:n for l, n in zip(b1l + b2l + b3l, b1n + b2n + b3n)}
    
    numbers = [rb[s] for s in samples]
    h = [hex(n) for n in numbers]
    print(h)
    u = encode(numbers)
    print(u)