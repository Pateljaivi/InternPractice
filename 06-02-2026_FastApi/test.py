from fastapi import FastAPI

app = FastAPI()

items = []

@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.post("/items")
async def create_item(item:str):
    items.append(item)
    return items

@app.get("/items/{item_id}")
async def read_item(item_id:int, q:str):
    item = items[item_id]
    return item

