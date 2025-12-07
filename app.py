import os
from re import U

import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from db import (
    add_property,
    add_user,
    delete_user,
    edit_user,
    get_properties,
    get_property_by_id,
    get_user,
    get_users,
)
from db_setup import get_connection
from schemas import (
    FeatureCreate,
    PropertyCreate,
    PropertyFullCreate,
    PropertyUpdate,
    UserCreate,
    UserUpdate,
)

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

# implementing user endpoints
@app.get("/users/")
def users():
    conn = get_connection()
    users = get_users(conn)
    return {"users": users}

@app.get("/user/{user_id}")
def user(user_id: int):
    conn = get_connection()
    user = get_user(conn, user_id)
    return {"user": user}

@app.post("/user/")
def create_user(user: UserCreate):
    conn = get_connection()
    user = add_user(conn, user)
    return {"user": user}

@app.delete("/user/{user_id}")
def delete_user_by_id(user_id: int):
    conn = get_connection()
    deleted = delete_user(conn, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User with id {user_id} has been deleted."}

@app.put("/user/{user_id}")
def update_user_by_id(user_id : int, user : UserUpdate):
    conn = get_connection()
    updated = edit_user(conn, user_id, user)
    if not updated:
            raise HTTPException(status_code=404, detail="user not found or nothing to update")
    return {"message": f"User with id {user_id} has been updated."}


# implementing property endpoints
@app.get("/properties/")
def properties():
    properties = get_properties(get_connection())
    return {"properties": properties}

@app.get("/property/{property_id}")
def property(property_id: int):
    property = get_property_by_id(get_connection(), property_id)
    return {"property": property}

@app.post("/property")
def create_property(data: PropertyFullCreate):
    conn = get_connection()
    user = get_user(conn, data.property.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        property_data = add_property(conn, data.property, data.features, data.location, data.images, data.videos)
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    return {"property": property_data}
