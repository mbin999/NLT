import json

def resolveJson(path):
    myFile = open(path, "rb")

    myObject = myFile.read()
    u = myObject.decode('utf-8-sig','ignore')
    myObject = u.encode('utf-8')
    myFile.encoding
    myFile.close()
    fileJson = json.loads(myObject, 'utf-8')
    #fileJson = json.load(file)
    field = fileJson["field"]
    futures = fileJson["futures"]
    type = fileJson["type"]
    name = fileJson["name"]
    time = fileJson["time"]

    return (field, futures, type, name, time)

def output():
    result = resolveJson(path)
    print(result)
    for x in result:
        for y in x:
            print(y)


path = r"C:\Users\dell\Desktop\kt\test.json"
output()





















