inUse = list(bytearray(10))

class node:
    def __init__(self, char, value = -1):
        self._char = char
        self._value = value

def splitToStringSplit(string):
    equal = string.split('=')
    plus = equal[0].split('+')
    result = equal[1]

    stringList = []
    for value in plus:
        minus = value.split('-')
        for i in range(len(minus)):
            if i > 0:
                minus[i] = '-' + minus[i]
        for m in minus:
            mul = m.split('*')
            for j in range(len(mul)):
                if j > 0:
                    mul[j] = '*' + mul[j]
                if mul[j] != '':
                    stringList.append(mul[j])
    stringList.append(result)

    return stringList

def countForVal(stringList):
    count = 0
    count_loop = 0
    count_mul = 0
    flag = False
    for i in range(len(stringList)):
        if '(' in stringList[i]:
            if '*' in stringList[i]:
                count_mul += 1
            flag = True
            count_par = 1
            count_loop += 1
            for j in range(i+1, len(stringList)):
                count_par += 1
                if ')' in stringList[j]:
                    break
            count += count_par
        if '*' in stringList[i]:
            if not flag:
                count_mul += 1
        if ')' in stringList[i]:
            flag = False

    count += count_mul
            
    return len(stringList) - count + count_loop + 1

# cái này tạm chưa quan tâm nhé
def checkLenStringValid(stringList):
    n = len(stringList) - 1
    for value in stringList[:n]:
        if len(value) >= len(stringList[n]):
            return False
    return True

# cái này cũng đừng quan tâm
def checkValueValid(nodeList, stringList):
    if checkLenStringValid(stringList):
        ch = stringList[len(stringList) - 1][0]
        for value in nodeList:
            if value._char == ch:
                if value._value <= 0:
                    return False
                else:
                    return True
    return False

def calcInPar(nodeList, stringList, n, count):
    result = 0
    temp = 0
    before = 0
    for k in range(n, len(stringList)):
        calc = 1
        for i in range(len(stringList[k]) - 1, -1, -1):
            for j in range(count):
                if nodeList[j]._char == stringList[k][i]:
                    temp += calc * nodeList[j]._value
                    calc *= 10
                    break
        if '-' in stringList[k]:
            if not '(' in stringList[k]:
                temp = -temp
        if '*' in stringList[k]:
            if not '(' in stringList[k]:
                temp *= before
                result -= before
        result += temp
        before = temp
        temp = 0

        if ')' in stringList[k]:
            break

    return result

def isValid(nodeList, count, stringList):
    val = list(bytearray(countForVal(stringList)))

    index = 0
    valInPar = 0
    flag = False
    for k in range(len(stringList)):
        calc = 1
        if '(' in stringList[k]:
            flag = True
            if '-' in stringList[k]:
                val[index] = -calcInPar(nodeList, stringList, k, count)
            else:
                val[index] = calcInPar(nodeList, stringList, k, count)
                if '*' in stringList[k]:
                    val[index-1] *= val[index]
                    val[index] = 0
                    index -= 1
        if not flag:
            for i in range(len(stringList[k]) - 1, -1, -1):
                for j in range(count):
                    if nodeList[j]._char == stringList[k][i]:
                        val[index] += calc * nodeList[j]._value
                        calc *= 10
                        break
            if '-' in stringList[k]:
                val[index] = -val[index]
            if '*' in stringList[k]:
                val[index-1] *= val[index]
                val[index] = 0
                index -= 1
            index += 1
        if ')' in stringList[k]:
            flag = False
            index += 1

    calcVal = 0
    for i in range(len(val) - 2):
        calcVal += val[i]

    if calcVal == val[len(val) - 2]:
        print(val)
        return True
    return False

def permutation(count, nodeList, n, stringList):
    if n == count - 1:
        for i in range(10):
            if inUse[i] == 0:
                nodeList[n]._value = i
                if isValid(nodeList, count, stringList):
                    return True

        return False

    for i in range(10):
        if inUse[i] == 0:
            nodeList[n]._value = i
            inUse[i] = 1
            if permutation(count, nodeList, n + 1, stringList):
                return True
            inUse[i] = 0

    return False

def solvProblem(string):
    freq = list(bytearray(26))
    stringList = splitToStringSplit(string)

    for value in stringList:
        for ch in value:
            if (ch != '-') & (ch != '*') & (ch != '(') & (ch != ')'):
                freq[ord(ch) - ord('A')] += 1

    unique = 0
    for i in range(26):
        if freq[i] > 0:
            unique += 1

    if unique > 10:
        return False

    nodeList = []
    for i in range(26):
        if freq[i] > 0:
            nodeList.append(node(chr(i + ord('A'))))

    if permutation(unique, nodeList, 0, stringList):
        return nodeList

    return False

def print_sol(nodeList):
    for value in nodeList:
        print(f"{value._char} => {value._value}")

if __name__ == '__main__':
    #stringList = ["SO","MANY","MORE","MEN","SEEM","TO","THEY","MAY","SAY","THAT","SOON","TRY","TO","TESTS"]
    #stringList = ["SEND","MORE","MONEY"]
    
    #result = solvProblem(stringList)

    #if result:
    #    print_sol(result)
    #else:
    #    print(result)

    #string = 'SEND+(MORE+MONEY)*OR+DIE=NUOYI'
    
    # string = 'SEND*THE=MONEY'

   string = "A+(B-C)*D*(H+M-F)*HY=RE"

   print(splitToStringSplit(string))

   result = solvProblem(string)

   if result:
        print_sol(result)
   else:
        print(result)