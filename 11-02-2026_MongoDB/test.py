import pymongo
from pymongo.errors import ServerSelectionTimeoutError

try:
    client = pymongo.MongoClient("mongodb://localhost:27017/",serverSelectionTimeoutMS=2000)
    client.server_info()

    db = client["company_db"]
    employees = db["employees"]
    print("Connected to MongoDB successfully.\n")

#1.READ
    print("\n1.READ: Current Employees:")
    all_employees = employees.find()
    for person in all_employees:
        print(f"{person['name']}({person['role']}) | Skills: {person['skills']}")

   #2.UPDATE
    # employees.update_one(
    #    {"name":"Nidhi"},
    #    {
    #        "$push":{"skills":"JAVASCRIPT"},
    #        "$set" : {"role":"Lead python developer"}
    #    }
    # )
    # print("\n2.UPDATE: Added 'JAVASCRIPT' and promoted to lead.")
    #
    # updated_person = employees.find_one({"name":"Nidhi"})
    # print(f"\n3.VARIFY:New data for Nidhi: {updated_person['skills']}")

    employees.delete_one({"name":"Nidhi"})
    print("\n4.DELETE: Removed data for Nidhi.")

except ServerSelectionTimeoutError:
    print("Error:Connection failed.Is 'mongod' running in your terminal?")