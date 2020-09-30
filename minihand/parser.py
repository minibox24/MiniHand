def Parser(text):
    parsing = [{}, ""]

    stringMode = False
    escapeMode = False

    for t in text:
        realT = t
        if t == "\\":
            escapeMode = True
            t = ""

        if t == '"':
            t = ""
            if stringMode:
                stringMode = False
            else:
                stringMode = True
            
            if escapeMode:
                stringMode = True
                t = '"'

        if t == " " and not stringMode:
            if True:
                parsing.append('')
                t = ""

        idx = len(parsing) - 1 
        parsing[idx] += t

        if realT != "\\" and escapeMode:
            escapeMode = False

    optionMode = False
    optionName = ""
    dellst = []

    for i in parsing:
        if type(i) is dict:
            continue

        if i == "":
            dellst.append(i)

        if i.startswith('--'):
            optionName = i[2:]
            optionMode = True
            dellst.append(i)

        if optionMode and not i.startswith('--'):
            parsing[0][optionName] = i
            dellst.append(i)
            optionMode = False
            optionName = ""

    for d in dellst:
        parsing.remove(d)

    if len(parsing) == 1:
        parsing.append('')

    return parsing

if __name__ == "__main__":
    text = '안녕 "안 녕" "=> \" <=" --hi hello'
    parsing = Parser(text)
    print(f"대상 문자열: \033[96m{text}\033[0m")
    print(f"파싱된 문자열 리스트: \033[96m{parsing}\033[0m")
    
