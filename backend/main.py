import random, string
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

trx = [
    {"id": 1, "code": "trx001", "data": "this is dummy data1", "total": 1000, "isPaid": False},
    {"id": 2, "code": "abcde1", "data": "this is dummy data2", "total": 1000, "isPaid": True}
]

class TransactionModel(BaseModel):
    data: str
    total: int

@app.get("/")
def index():
    return {
        "msg": "simple payment gateway simulator",
        "success": True
    }

@app.get("/transaction")
def transaction_list():
    return {
        "msg": "transaction list",
        "data": trx,
        "success": True
    }

@app.post("/transaction")
def transaction_create(item: TransactionModel):
    code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
    id = len(trx)
    trx.append({
        "id": id + 1,
        "code": str(code),
        "data": item.data,
        "total": item.total,
        "isPaid": False
    })

    return {
        "msg": "create transaction success",
        "data": trx[id],
        "success": True
    }


@app.post("/payment/{id}/{code}")
def transaction_create(id: int, code: str):
    try:
        data = trx[id-1]
        data["isPaid"] = True
        return {
            "msg": "payment success",
            "data": trx[id -1],
            "success": True
        }
    except Exception as e:
        return {
            "msg": "payment failed",
            "data": [],
            "success": False
        }

@app.get("/transaction/{trx_id}")
def transaction_retrive(trx_id: int):
    try:
        return {
            "msg": "transaction detail",
            "data": trx[trx_id - 1],
            "success": True
        }
    except IndexError:
        return {
            "msg": "transaction data not found",
            "data": [],
            "success": False
        }

