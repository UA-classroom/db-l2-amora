import os

import psycopg2
from db import get_users, get_user_by_id, add_user, delete_user, edit_user, get_properties, get_property_by_id
from db_setup import get_connection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

"""
ADD ENDPOINTS FOR FASTAPI HERE
Make sure to do the following:
- Use the correct HTTP method (e.g get, post, put, delete)
- Use correct STATUS CODES, e.g 200, 400, 401 etc. when returning a result to the user
- Use pydantic models whenever you receive user data and need to validate the structure and data types (VG)
This means you need some error handling that determine what should be returned to the user
Read more: https://www.geeksforgeeks.org/10-most-common-http-status-codes/
- Use correct URL paths the resource, e.g some endpoints should be located at the exact same URL, 
but will have different HTTP-verbs.
"""


# INSPIRATION FOR A LIST-ENDPOINT - Not necessary to use pydantic models, but we could to ascertain that we return the correct values
# @app.get("/items/")
# def read_items():
#     con = get_connection()
#     items = get_items(con)
#     return {"items": items}


# INSPIRATION FOR A POST-ENDPOINT, uses a pydantic model to validate
# @app.post("/validation_items/")
# def create_item_validation(item: ItemCreate):
#     con = get_connection()
#     item_id = add_item_validation(con, item)
#     return {"item_id": item_id}


# IMPLEMENT THE ACTUAL ENDPOINTS! Feel free to remove


class House(BaseModel):
    name: str
    price: int
    description: str


@app.get("/users/")
def users():
    conn = get_connection()
    users = get_users(conn)
    return {"users": users}

@app.get("/user/{user_id}")
def user(user_id: int):
    conn = get_connection()
    user = get_user_by_id(conn, user_id)
    return {"user": user}

@app.post("/user/")
def create_user(user: dict):
    conn = get_connection()
    user_id = add_user(conn, user)
    return {"user_id": user_id}

@app.get("/properties/")
def properties():
    properties = get_properties(get_connection())
    return {"properties": properties}

@app.get("/property/{property_id}")
def property(property_id: int):
    property = get_property_by_id(get_connection(), property_id)
    return {"property": property}

# @app.get("/users/")
# def users():
#     users = get_users(get_connection())
#     return {"Users": users}

# @app.get("/agencies/")
# def agencies():
#     agencies = get_agencies(get_connection())
#     return {"Agencies": agencies}

# @app.get("/brokers/")
# def brokers():
#     brokers = get_brokers(get_connection())
#     return {"Brokers": brokers}
