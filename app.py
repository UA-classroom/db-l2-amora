import os
from re import U

import psycopg2
from db import (
    add_agency,
    add_property,
    add_user,
    delete_agency_by_id,
    delete_property,
    delete_user,
    edit_agency,
    edit_property,
    edit_user,
    get_agencies,
    get_agency,
    get_brokers,
    get_properties,
    get_property_by_id,
    get_user,
    get_users,
    get_broker,
    add_broker,
    edit_broker,
    delete_broker_by_id
)
from db_setup import get_connection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from schemas import (
    AgencyCreate,
    AgencyUpdate,
    PropertyFullCreate,
    PropertyUpdate,
    UserCreate,
    UserUpdate,
    BrokerCreate,
    BrokerUpdate
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

@app.put("/user/{user_id}")
def update_user_by_id(user_id : int, user : UserUpdate):
    conn = get_connection()
    updated = edit_user(conn, user_id, user)
    if not updated:
            raise HTTPException(status_code=404, detail="user not found or nothing to update")
    return {"message": f"User with id {user_id} has been updated."}

@app.delete("/user/{user_id}")
def delete_user_by_id(user_id: int):
    conn = get_connection()
    deleted = delete_user(conn, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User with id {user_id} has been deleted."}


# implementing property endpoints
@app.get("/properties/")
def properties():
    properties = get_properties(get_connection())
    return {"properties": properties}

@app.get("/property/{property_id}")
def property(property_id: int):
    property = get_property_by_id(get_connection(), property_id)
    return {"property": property}

@app.post("/property/")
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

@app.put("/property/{property_id}")
def update_property_by_id(property_id : int, property : PropertyUpdate):
    conn = get_connection()
    updated = edit_property(conn, property_id, property)
    if not updated:
        raise HTTPException(status_code=404, detail="property not found or nothing to update")
    return {"message": f"Property with id {property_id} has been updated."}

@app.delete("/property/{property_id}")
def delete_property_by_id(property_id : int):
    conn = get_connection()
    deleted = delete_property(conn, property_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"Property with id {property_id} has been deleted."}

#implementing agencies

@app.get("/agencies/")
def agencies():
    conn = get_connection()
    agencies = get_agencies(conn)
    if not agencies:
        raise HTTPException(status_code=404, detail="No agencies found")
    return {"agencies" : agencies}

@app.get("/agency/{agency_id}")
def agency_by_id(agency_id : int):
    conn = get_connection()
    agency = get_agency(conn, agency_id)
    return {"agency" : agency}

@app.post("/agency/")
def create_agency(data : AgencyCreate):
    conn = get_connection()
    agency = add_agency(conn, data)
    if not agency:
        raise HTTPException(status_code=404, detail="agency is not added")
    return {"agency" : agency}

@app.put("/agency/{agency_id}")
def update_agency(agency_id : int, data : AgencyUpdate):
    conn = get_connection()
    updated = edit_agency(conn, agency_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Agency not found or nothing to update")
    return {"message": f"Agency with id {agency_id} has been updated."}

@app.delete("/agency/{agency_id}")
def delete_agency(agency_id : int):
    conn = get_connection()
    deleted = delete_agency_by_id(conn, agency_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Agency not found")
    return {"message": f"Agency with id {agency_id} has been deleted."}

# implementing brokers endpoints

@app.get("/brokers/")
def brokers():
    conn = get_connection()
    brokers = get_brokers(conn)
    if not brokers:
        raise HTTPException(status_code=404, detail="No brokers found")
    return {"brokers" : brokers}

@app.get("/broker/{broker_id}")
def broker_by_id(broker_id : int):
    conn = get_connection()
    broker = get_broker(conn, broker_id)
    if not broker:
        raise HTTPException(status_code=404, detail="Broker not found")
    return {"broker" : broker}

@app.post("/broker/")
def create_broker(broker: BrokerCreate):
    conn = get_connection()
    broker = add_broker(conn, broker)
    if not broker:
        raise HTTPException(status_code=404, detail="Broker not added")
    return {"broker" : broker}

@app.put("/broker/{broker_id}")
def update_broker(broker_id : int, broker : BrokerUpdate):
    conn = get_connection()
    updated = edit_broker(conn, broker_id, broker)
    if not updated:
        raise HTTPException(status_code=404, detail="Broker not found or nothing to update")
    return {"message": f"Broker with id {broker_id} has been updated."}

@app.delete("/broker/{broker_id}")
def delete_broker(broker_id : int):
    conn = get_connection()
    deleted = delete_broker_by_id(conn, broker_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Broker not found")
    return {"message": f"Broker with id {broker_id} has been deleted."}

@app.post("/")
