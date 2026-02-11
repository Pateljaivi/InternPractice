import pymongo
from pymongo.errors import ServerSelectionTimeoutError

def setup_mongodb():
    client = pymongo.MongoClient("mongodb://localhost:27017/",serverSelectionTimeoutMS=2000)

    try:
        client.server_info()
        print("Conection Successful:MongoDB server is running.")

        db = client["company_db"]
        employees = db["employees"]

        new_employee = {
            "name" : "Jaivi",
            "role" : "Python Developer",
            "skills" : ["python","mongodb","FastAPI"],
            "experience":1
        }

        if employees.count_documents({"name":"Jaivi"}) == 0:
            result = employees.insert_one(new_employee)
            print(f"Success! Created collection and inserted ID:{result.inserted_id}")
        else:
            print("Record for 'Jaivi' already exists.Skipping insertion.")

        collections = db.list_collection_names()
        print(f"Current Collections in 'company_db':{collections}")

        user_data = employees.find_one({"name":"Jaivi"})
        print(f"Varified Data in DB:{user_data}")

    except ServerSelectionTimeoutError:
        print("Error:Could not connect to MongoDB...")
        print("Make sure you have MongoDB running on localhost!!!")

if __name__ == '__main__':
    setup_mongodb()