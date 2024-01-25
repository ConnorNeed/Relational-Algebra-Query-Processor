from relation import Table
from Interface import get_user_info
TABLE_NAMES = []
TABLES = []

def start ():
    while True:
        str = get_user_info()
        if str[:str.find(' ')].strip().lower() in ["select","project", "ijoin", "ljoin", "rjoin","ojoin","union","intersect","minus"]:
            try:
                caller(str.replace("\n",""))[0].display()
            except Exception as e:
                print(e)
            continue
        try:
            createTable(str).display()
        except Exception as e:
            print(e)
        

def caller(str):
    inputTables = []
    if(str.find("(") == -1):
        if (str.strip() in TABLE_NAMES):
            return [TABLES[TABLE_NAMES.index(str.strip())]]
        raise Exception(f"Can't find table {str.strip()}")
    lIndex = str.find("(")
    opens = 1
    for i in range(str.find("(")+1,len(str)):
        c = str[i]
        if c == '(':
            opens += 1
            if lIndex == -1:
                lIndex = i
            continue
        if c ==')':
            opens -= 1
            if opens == 0:
              inputTables +=  caller(str[lIndex+1:i])
              lIndex = -1
        if opens < 0:
            raise Exception("Parse Error: Invalid bracet formation")

    str = str[:str.find("(")]
    keyword = str[:str.find(" ")]

    if(keyword.lower()=="select"):
        return select(str[str.find(" ")+1:], inputTables)
    if(keyword.lower()=="project"):
        return project(str[str.find(" ")+1:], inputTables)
    if(keyword.lower() == "ijoin"):
        return iJoin(str[str.find(" ")+1:], inputTables)
    if(keyword.lower() == "ljoin"):
        return lJoin(str[str.find(" ")+1:], inputTables)
    if(keyword.lower() == "rjoin"):
        return rJoin(str[str.find(" ")+1:], inputTables)
    if(keyword.lower() == "ojoin"):
        return oJoin(str[str.find(" ")+1:], inputTables)
    if(keyword.lower() == "union"):
        return [inputTables[0].union(inputTables[1])]
    if(keyword.lower() == "intersect"):
        return [inputTables[0].intersect(inputTables[1])]
    if(keyword.lower() == "minus"):
        return [inputTables[0].setMinus(inputTables[1])]

    
def select(str, inputArr):
    if(len(inputArr) != 1):
        raise Exception(f"Invalid Number of arguments for select ({len(inputArr)} != 1)")
    delimiters = ['>','<','=','!', "&", '|'] 
    values = []
    value = ''
    evalStatement = 'values[0] '
    flag = False
    for i in range(len(str)):
        c = str[i]
        if c in delimiters:
            if(not flag):
                flag = True
                values.append(value.strip())
                value = ''
            evalStatement += c
            continue
        if flag:
            evalStatement += f' values[{len(values)}] '
        flag = False
        if c != '"' and c != ' ':
            value += c
    values.append(value)    
    evalStatement = evalStatement.strip()
    return [inputArr[0].get_rows(values,evalStatement.replace("&&","and").replace("||", "or").replace(" = "," == "))]

def project(str, inputArr):
    if(len(inputArr) > 1):
        raise Exception("Invalid Number of arguments for project")
    csvList = str[str.find('"')+1:str.rfind('"')].replace(" ", "").split(",")
    return [inputArr[0].get_columns(csvList)]

def iJoin(str, inputArr):
    if(len(inputArr) != 2):
        raise Exception("Invalid Number of arguments for iJoin")
    cross = inputArr[0].dup1(inputArr[1].len()).join(inputArr[1].dup2(inputArr[0].len()))
    return select(str, [cross])

def lJoin(str, inputArr):
    if(len(inputArr) != 2):
        raise Exception("Invalid Number of arguments for lJoin")
    [iJoinTable] = iJoin(str, inputArr)
    leftOnly = inputArr[0].setMinus(iJoinTable.get_columns(inputArr[0].column_names))
    nullTable = Table(rows=leftOnly.rows, columns=inputArr[1].columns, column_names=inputArr[1].column_names, table_name="null")
    return [iJoinTable.union(leftOnly.join(nullTable))]

def rJoin(str, inputArr):
    if(len(inputArr) != 2):
        raise Exception("Invalid Number of arguments for rJoin")
    [iJoinTable] = iJoin(str, inputArr)
    rightOnly = inputArr[1].setMinus(iJoinTable.get_columns(inputArr[1].column_names))
    nullTable = Table(rows=rightOnly.rows, columns=inputArr[0].columns, column_names=inputArr[0].column_names, table_name="null")
    return [iJoinTable.union(nullTable.join(rightOnly))]

def oJoin(str, inputArr):
    if(len(inputArr) != 2):
        raise Exception("Invalid Number of arguments for oJoin")
    return [lJoin(str, inputArr)[0].union(rJoin(str, inputArr)[0])]


def createTable(str):
    index = str.find(' ')
    if index == -1:
        raise Exception(f"Spacing error in relation")
    name = str[:index].strip()
    str = str[index:].strip()
    column_names = getBetween(str, "(", ")").replace(" ", "").split(",")
    str = str[str.find(')')+1:]
    rows = getBetween(str, "\n", "\n}").replace(" ", "").split("\n")
    table = Table(0, len(column_names), column_names, name)
    for row in rows:
        cells = row.split(",")
        for i in range(len(cells)):
            cells[i] = cells[i].strip()
        table.add_row(cells)
    TABLES.append(table)
    TABLE_NAMES.append(name)
    return table

def getBetween(str, a, b):
    indexA = str.find(a)
    indexB = str[indexA+1:].find(b)
    if indexA == -1 or indexB == -1:
        raise Exception(f"Could not find {b} after {a} in {str}")
    return str[indexA+1:indexB+indexA+1]

start()