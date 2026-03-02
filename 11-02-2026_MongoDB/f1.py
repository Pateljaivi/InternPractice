import pymongo

if __name__ == '__main__':
    print("Welcome to pyMongo")
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    print(client)
    db = client['Star']
    collection = db['c1forStar']

    # a = client.list_database_names()
    # print(a)
    # dictionary = {'name':'Rohit','marks':90}
    # collection.insert_one(dictionary)

    # l1 = [
    #     {"name":"Virat","Location":"Delhi","Age":37},
    #     {"name": "Rohit", "Location": "Mumbai", "Age": 35},
    #     {"name": "Bumrah", "Location": "Panjab", "Age": 31},
    #     {"name": "Hardik", "Location": "Gujarat", "Age": 33}
    # ]
#unique id we can set also through '_id':8
    # collection.insert_many(l1)

    # one = collection.find_one({"name":'Hardik'})
    # print(one)

    # allDocs = collection.find({"name": "Rohit"},{'name':1,'_id':0})
    # for item in allDocs:
    #     print(item)

    # allDocs = list(collection.find({"name": "Rohit"},{"name":0}).limit(1))
    # print(len(allDocs))
    # for item in allDocs:
    #      print(item)


    #update oration
    prev = {"name": "Virat"}
    nextt = {"$set":{"Location":"MEGHALAYA"}}
    up = collection.update_many(prev, nextt)
    print(up.modified_count)