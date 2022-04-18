import random
import datetime

startTime = datetime.datetime.now()
maxTime = startTime + datetime.timedelta(minutes=5)

geneSet = [i for i in range(10)]

class node:
    def __init__(self, char, leader):
        self._char = char
        self._leader = leader

def get_char(string):
    setChar = set()
    setLeader = set()

    index = 0
    for ch in string:
        if ch.isalpha() & ch.isupper():
            setChar.add(ch)
            if index > 0:
                if not string[index - 1].isalpha():
                    setLeader.add(ch)
            else:
                if ch.isalpha():
                    setLeader.add(ch)
        index += 1

    listReturn = list(setChar)
    listReturn.sort()

    if len(listReturn) < 10:
        for i in range(10 - len(listReturn)):
            listReturn.append('_')

    return listReturn, list(setLeader)

# for class node
def get_node_list(listChar, listLeader):
	listReturn = []
	for ch in listChar:
		listReturn.append(node(ch, True if ch in listLeader else False))

	return listReturn

def print_node_list(nodeList):
    for value in nodeList:
        print(f"{value._char} => {value._leader}")

def print_problem_list(problem):
    for value in problem:
        print(f"{value[0]} => {value[1]._char} => {value[1]._leader}")

# for calculating
def split_to_string_list(string):
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

def count_for_len_val(stringList):
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

def calc_in_parentheses(problem, stringList, n):
    result = 0
    temp = 0
    before = 0
    for k in range(n, len(stringList)):
        calc = 1
        for i in range(len(stringList[k]) - 1, -1, -1):
            for j in range(len(problem)):
                if problem[j][1]._char == stringList[k][i]:
                    temp += calc * problem[j][0]
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

def calc_for_fitness(problem, stringList):
    val = list(bytearray(count_for_len_val(stringList)))

    index = 0
    valInPar = 0
    flag = False
    for k in range(len(stringList)):
        calc = 1
        if '(' in stringList[k]:
            flag = True
            if '-' in stringList[k]:
                val[index] = -calc_in_parentheses(problem, stringList, k)
            else:
                val[index] = calc_in_parentheses(problem, stringList, k)
                if '*' in stringList[k]:
                    val[index-1] *= val[index]
                    val[index] = 0
                    index -= 1
        if not flag:
            for i in range(len(stringList[k]) - 1, -1, -1):
                for j in range(len(problem)):
                    if problem[j][1]._char == stringList[k][i]:
                        val[index] += calc * problem[j][0]
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

    return calcVal, val[len(val) - 2]

def unzip(list_zip):
    return [list(value) for value in list_zip]

# Genetic Algorithm
def gen_ancestor(nodeList):
	geneList = geneSet.copy()
	genes = []
	index = 0
	while len(genes) < 10:
		val = random.sample(geneList,1)[0]
		if nodeList[index]._leader:
			if val == 0:
				continue
		genes.append(val)
		geneList.remove(val)
		index += 1

	return unzip(list(zip(genes, nodeList)))

def get_fitness(problem, stringList):
	leftVal, rightVal = calc_for_fitness(problem, stringList)
	return abs(rightVal - leftVal)

def can_mutate(ancestor, n, m):
    if ancestor[n][1]._leader:
        if ancestor[m][0] == 0:
            return False

    if ancestor[m][1]._leader:
        if ancestor[n][0] == 0:
            return False

    return True

def get_child(ancestor):
    child = ancestor.copy()
    while True:
        n, m = random.sample(geneSet, 2)

        if can_mutate(child, n, m):
            child[n][0], child[m][0] = child[m][0], child[n][0]
            break
    return child

def solving(string):
    stringList = split_to_string_list(string)
    listChar, listLeader = get_char(string)

    if len(listChar) > 10:
        return False

    nodeList = get_node_list(listChar, listLeader)
    ancestor = gen_ancestor(nodeList)
    best_fitness = get_fitness(ancestor, stringList)
    generaion = 0

    if best_fitness == 0:
        print(f'Generations: {generaion}')
        return ancestor

    while True:
        if datetime.datetime.now() > maxTime:
            print(f'Generations: {generaion}')
            return False

        child = get_child(ancestor)
        child_fitness = get_fitness(child, stringList)
        generaion += 1

        if child_fitness == 0:
            print(f'Generations: {generaion}')
            return child

        if child_fitness < best_fitness:
            ancestor = child
            best_fitness = child_fitness

def read_file(file_name):
    with open(file_name, 'r') as f:
        problem = f.readline()
    return problem

def to_string(solved):
    string = ''
    for value in solved:
        if value[1]._char.isalpha() & value[1]._char.isupper():
            string += str(value[0])
    return string

def write_file(file_name, solved):
    with open(file_name, 'w') as f:
        if not solved:
            f.write('The problem has no solution or exceeds the runtime!')
        else:
            f.write(to_string(solved))

# string = "SO+MANY+MORE+MEN+SEEM+TO+SAY+THAT+THEY+MAY+SOON+TRY+TO+STAY+AT+HOME+SO+AS+TO+SEE+OR+HEAR+THE+SAME+ONE+MAN+TRY+TO+MEET+THE+TEAM+ON+THE+MOON+AS+HE+HAS+AT+THE+OTHER+TEN=TESTS"
# string = "SEND+(MORE+MONEY)*OR+DIE=NUOYI"
# string = "SEND+MORE=MONEY"
# string = "SEND+(MORE+MONEY)-OR+DIE=NUOYI"
# string = "SEND*TA=MONEY"
# string = "A+(B-C)*D*(H+M-F)*HY=RE"
# string = "TWO+TWO=FOUR"
# string = "SEND+MORE*A+MORE=MONEY"
# string = "NHATCUONG+(HOTBOY+HATHAY+HOCTOT)*HAHA-THONG*GYANG=GACUBTUUHH"

string = read_file('input.txt')

print(string)
result = solving(string)
write_file('output.txt', result)

if not result:
    print(result)
else:
    print("====RESULT====")
    print_problem_list(result)
    print('====OUTPUT====')
    print(to_string(result))