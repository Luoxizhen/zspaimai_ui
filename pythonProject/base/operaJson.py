import json
# def readJson():
#     return json.load(open('login.json','r'))['item']
# for item in readJson():
#     print(item)


def readJson():
    return json.load(open('../data/login.json', 'r'))['item']
print (readJson())
for item in readJson():
    print(item)