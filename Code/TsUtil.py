import random

def ConvertToInt(liste):
    product = []
    for i in liste:
        product.append(int(i))
    return product

def RandomIndexes(List,amount):
    indexes = []

    while len(indexes) < amount:
        temp = len(List)
        index = random.randint(0,temp-1)
        if index in indexes:
            continue
        indexes.append(index)

    indexes.sort(reverse=True)
    #print(indexes)
    
    return indexes

def RandomChoices2L(List1,List2,amount):
    indexes = RandomIndexes(List1,amount)
    tempX = []
    tempY = []
    for i in indexes:
        tempX.append(List1.pop(i))
        tempY.append(List2.pop(i))
    return (tempX,tempY)

def KFold(number,dataset):
    CategoryW = []
    CategoryL = []
    for i in dataset:
        if i[1] == 0:
            CategoryL.append(i)
        elif i[1] == 1:
            CategoryL.append(i)
    sets = []
    for i in range(number):
        index1 = int(len(CategoryL)/number)
        index2 = int(len(CategoryW)/number)
        testList = CategoryL[index1*i:index1*(i+1)] + CategoryW[index2*i:index2*(i+1)]
        trainList = CategoryL[:index1*i] + CategoryL[index1*i:] + CategoryW[:index2*i] + CategoryW[index2*i:]
        sets.append([trainList,testList])

    return sets

def LoadCfg(FileName):
    print("Getting Config File")
    config = open("Config.cfg","r")
    rawInfo = config.readlines()
    config.close()
    Info = {}
    category = []

    for i in rawInfo:
        temp = i.replace(" ","")
        temp = temp.replace("\n","")
        if temp == "":
            continue
        if temp[0] == "-":
            ctg = temp.replace("-","")
            category.append(ctg)
            Info[ctg] = {}
        else:
            inf = temp.split("=")
            if inf[1].find('"') < 0:
                try:
                    if inf[1] == "True":
                        inf[1] = True
                    elif inf[1] == "False":
                        inf[1] = False
                    else:
                        inf[1] = float(inf[1])
                except Exception:
                    print("Failed: " + inf[1])
            else:
                inf[1] = inf[1].replace('"',"")
            Info[category[len(category)-1]][inf[0]] = inf[1]
        #print(category)

    return Info

def LoadFile(FileName,IncludeDraw=False):
    print("Processing File: " + FileName)

    testInfo = open(FileName,"r")
    data = testInfo.readlines()
    testInfo.close()

    TestX = []
    TestY = []

    for i in data:
        temp = i.replace("\n","")
        temp = temp.split(",")
        
        tempList = ConvertToInt(temp[0:len(temp)-1])
        result = int(temp[len(temp)-1])
        if not IncludeDraw and result == 2:
            #print("Including draw")
            continue
        TestX.append(tempList)
        TestY.append(result)
    return (TestX,TestY)

def GenerateKFoldSet(FileName1,FileName2):
    file1 = LoadFile(FileName1)
    file2 = LoadFile(FileName2)
    dataX = file1[0] + file2[0]
    dataY = file1[1] + file2[1]
    data = []
    for i in range(len(dataX)):
        data.append((dataX[i],dataY[i]))
    return KFold(10,data)
