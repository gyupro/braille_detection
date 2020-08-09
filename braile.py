import korean_braille
import english_braille
import numbers_braille

def encode(b_num, lang):



    letters = []


    for row in b_num:

        # if d in korean_braille.b1:
        #     print(hex(d), korean_braille.b1[d])
        # elif d in korean_braille.b2:
        #     print(hex(d), korean_braille.b2[d])
        # elif d in korean_braille.b3:
        #     print(hex(d), korean_braille.b3[d])
        # else:
        #     print(hex(d), '??')

        if lang=='ko':

            korean = korean_braille.encode(row)
            letters.append(korean)
            print(korean)
        elif lang=='en':
            english = english_braille.encode(row)
            letters.append(english)
            print(english)
        elif lang=='numbers':
            numbers = numbers_braille.encode(row)
            letters.append(numbers)
            print(numbers)

    return letters
    ##################
