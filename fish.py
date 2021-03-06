import sys
import time
import random

class RegisterValue:
    def __init__(self):
        self.value = 0
        self.isSet = False

def PrintCodeSpace(codeSpace, x, y, Stack, output, register):
    print()
    print("Stacks:")
    for i in range(len(Stack) - 1, -1, -1):
        print(Stack[i])
    print("Register: |", end='')
    
    for r in register:
        if r.isSet:
            print(r.value, end='')
            print("|", end='')
        else:
            print("#|", end='')
    print()

    for i in range(len(codeSpace)):
        for j in range(len(codeSpace[i])):
            print('\u001b[40m', end='')
            if i == y and j == x:
                print('\u001b[42m', end='')
            print(codeSpace[i][j], end='')
            print('\u001b[40m', end='')
        if(codeSpace[i][-1] != '\n'):
            print()
    print()
    print("Output:\n" + "".join(output))
    print()

program = open(sys.argv[1]).read().split('\n')
framesPerLoop = int(sys.argv[3])

PCDir = 1
PCx = 0
PCy = 0

Stack = []
Stack.append([])

if len(sys.argv) > 4:
    for i in range(len(sys.argv) - 1, 3, -1):
        Stack[-1].append(int(sys.argv[i]))

maxLine = 0
for line in program:
    if len(line) > maxLine:
        maxLine = len(line)
for l in range(len(program)):
    for i in range(maxLine - len(program[l])):
        program[l] = "".join((program[l], ' '))

output = []
register = [RegisterValue()]

PrintCodeSpace(program, PCx, PCy, Stack, output, register)

steps = 0

readingMode = False
manualInput = False

negativeData = dict()

while(True):
    for skip in range(framesPerLoop):
        if readingMode:
            if program[PCy][PCx] == "'" or program[PCy][PCx] == '"':
                readingMode = False
            else:
                Stack[-1].append(ord(program[PCy][PCx]))
        elif program[PCy][PCx] == '^':
            PCDir = 0
        elif program[PCy][PCx] == '>':
            PCDir = 1
        elif program[PCy][PCx] == 'v':
            PCDir = 2
        elif program[PCy][PCx] == '<':
            PCDir = 3
        elif program[PCy][PCx].isdigit():
            Stack[-1].append(int(program[PCy][PCx]))
        elif ord(program[PCy][PCx]) <= 102 and ord(program[PCy][PCx]) >= 97:
            Stack[-1].append(ord(program[PCy][PCx]) - 97 + 10)
        elif program[PCy][PCx] == ':':
            Stack[-1].append(Stack[-1][-1])
        elif program[PCy][PCx] == 'n':
            output.append(str(Stack[-1].pop()))
        elif program[PCy][PCx] == "'" or program[PCy][PCx] == '"':
            readingMode = True
        elif program[PCy][PCx] == '&':
            if register[-1].isSet:
                Stack[-1].append(register[-1].value)
                register[-1].isSet = False
            else:
                register[-1].value = Stack[-1].pop()
                register[-1].isSet = True
        elif program[PCy][PCx] == '$':
            tmp = Stack[-1][-2]
            Stack[-1][-2] = Stack[-1][-1]
            Stack[-1][-1] = tmp
        elif program[PCy][PCx] == '.':
            PCy = Stack[-1].pop()
            PCx = Stack[-1].pop()
        elif program[PCy][PCx] == '+':
            a = Stack[-1].pop()
            b = Stack[-1].pop()
            Stack[-1].append(b + a)
        elif program[PCy][PCx] == '*':
            a = Stack[-1].pop()
            b = Stack[-1].pop()
            Stack[-1].append(b * a)
        elif program[PCy][PCx] == '%':
            a = Stack[-1].pop()
            b = Stack[-1].pop()
            Stack[-1].append(b%a)
        elif program[PCy][PCx] == '-':
            a = Stack[-1].pop()
            b = Stack[-1].pop()
            Stack[-1].append(b-a)
        elif program[PCy][PCx] == 'o':
            output.append(chr(Stack[-1].pop()))
        elif program[PCy][PCx] == 'i':
            if manualInput:
                Stack[-1].append(ord(input()[0]))
            else:
                tmpstr = sys.stdin.read(1)
                if len(tmpstr) == 0:
                    Stack[-1].append(-1)
                else:
                    Stack[-1].append(ord(tmpstr))
        elif program[PCy][PCx] == 'p':
            y = Stack[-1].pop()
            x = Stack[-1].pop()
            v = Stack[-1].pop()
            if x < 0 or y < 0:
                negativeData[(x, y)] = v
            else:
                if x != int(x) or y != int(y):
                    print("FLOAT CAN NOT BE AN INDEX")
                    exit()
                program[int(y)] = program[int(y)][:int(x)] + str(chr(v)) + program[int(y)][int(x) + 1:]
        elif program[PCy][PCx] == '?':
            if Stack[-1].pop() == 0:
                if PCDir == 0:
                    if PCy == 0:
                        PCy = len(program) - 1
                    else:
                        PCy -= 1
                elif PCDir == 1:
                    if PCx == len(program[PCy]) - 1:
                        PCx = 0
                    else:
                        PCx += 1
                elif PCDir == 2:
                    if PCy == len(program) - 1:
                        PCy = 0
                    else:
                        PCy += 1
                else:
                    if PCx == 0:
                        PCx = len(program[PCy]) - 1
                    else:
                        PCx -= 1
        elif program[PCy][PCx] == '~':
            Stack[-1].pop()
        elif program[PCy][PCx] == '{':
            Stack[-1].append(Stack[-1].pop(0))
        elif program[PCy][PCx] == '}':
            Stack[-1].insert(0, Stack[-1].pop())
        elif program[PCy][PCx] == 'g':
            y = Stack[-1].pop()
            x = Stack[-1].pop()
            if x < 0 or y < 0:
                Stack[-1].append(ord(negativeData[(x, y)]))
            else:
                Stack[-1].append(ord(program[y][x]))
        elif program[PCy][PCx] == ';':
            PrintCodeSpace(program, PCx, PCy, Stack, output, register)
            print('FINISHED SUCCESFULLY')
            exit()
        elif program[PCy][PCx] == 'r':
            Stack[-1].reverse()
        elif program[PCy][PCx] == 'l':
            Stack[-1].append(len(Stack[-1]))
        elif program[PCy][PCx] == '!':
            if PCDir == 0:
                if PCy == 0:
                    PCy = len(program) - 1
                else:
                    PCy -= 1
            elif PCDir == 1:
                if PCx == len(program[PCy]) - 1:
                    PCx = 0
                else:
                    PCx += 1
            elif PCDir == 2:
                if PCy == len(program) - 1:
                    PCy = 0
                else:
                    PCy += 1
            else:
                if PCx == 0:
                    PCx = len(program[PCy]) - 1
                else:
                    PCx -= 1
        elif program[PCy][PCx] == '[':
            register.append(RegisterValue())
            d = Stack[-1].pop()
            tmpStack = []
            for n in range(d):
                tmpStack.append(Stack[-1].pop())
            tmpStack.reverse()
            Stack.append(tmpStack)
        elif program[PCy][PCx] == ']':
            register.pop()
            Stack[-1].reverse()
            while len(Stack[-1]) > 0:
                Stack[-2].append(Stack[-1].pop())
            Stack.pop()
        elif program[PCy][PCx] == '@':
            tmp = Stack[-1][-1]
            Stack[-1][-1] = Stack[-1][-2]
            Stack[-1][-2] = Stack[-1][-3]
            Stack[-1][-3] = tmp
        elif program[PCy][PCx] == ',':
            a = Stack[-1].pop()
            b = Stack[-1].pop()
            Stack[-1].append(b/a)
        elif program[PCy][PCx] == '\\':
            if PCDir == 0:
                PCDir = 3
            elif PCDir == 1:
                PCDir = 2
            elif PCDir == 2:
                PCDir = 1
            else:
                PCDir = 0
        elif program[PCy][PCx] == '/':
            if PCDir == 0:
                PCDir = 1
            elif PCDir == 1:
                PCDir = 0
            elif PCDir == 2:
                PCDir = 3
            else:
                PCDir = 2
        elif program[PCy][PCx] == '_':
            if PCDir == 0:
                PCDir = 2
            elif PCDir == 2:
                PCDir = 0
        elif program[PCy][PCx] == '|':
            if PCDir == 1:
                PCDir = 3
            elif PCDir == 3:
                PCDir = 1
        elif program[PCy][PCx] == 'x':
            PCDir = random.randint(0,3)
        elif program[PCy][PCx] == '=':
            x = Stack[-1].pop()
            y = Stack[-1].pop()
            if x == y:
                Stack[-1].append(1)
            else:
                Stack[-1].append(0)
        elif program[PCy][PCx] == ')':
            a = Stack[-1].pop()
            b = Stack[-1].pop()
            if b > a:
                Stack[-1].append(1)
            else:
                Stack[-1].append(0)
        elif program[PCy][PCx] == '(':
            a = Stack[-1].pop()
            b = Stack[-1].pop()
            if b < a:
                Stack[-1].append(1)
            else:
                Stack[-1].append(0)
        elif program[PCy][PCx] == 'k':
            output.clear()
        elif program[PCy][PCx] != ' ':
            print('UNIMPLEMENTED CHARACTER: ' + program[PCy][PCx])
            exit()

        if PCDir == 0:
            if PCy == 0:
                PCy = len(program) - 1
            else:
                PCy -= 1
        elif PCDir == 1:
            if PCx == len(program[PCy]) - 1:
                PCx = 0
            else:
                PCx += 1
        elif PCDir == 2:
            if PCy == len(program) - 1:
                PCy = 0
            else:
                PCy += 1
        else:
            if PCx == 0:
                PCx = len(program[PCy]) - 1
            else:
                PCx -= 1
        steps += 1

    PrintCodeSpace(program, PCx, PCy, Stack, output, register)
    print(negativeData)
    time.sleep(float(sys.argv[2]))
    print("Steps taken: " + str(steps))


print()