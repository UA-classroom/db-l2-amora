import os
from re import U

import psycopg2
from db import (
    add_agency,
    add_broker,
    add_favorite_property,
    add_property,
    add_user,
    bid_on_property,
    delete_agency_by_id,
    delete_broker_by_id,
    delete_property,
    delete_user,
    edit_agency,
    edit_broker,
    edit_property,
    edit_user,
    get_agencies,
    get_agency,
    get_bids_for_property,
    get_broker,
    get_brokers,
    get_favorite_properties,
    get_listings,
    get_offers_for_property,
    get_properties,
    get_property_by_id,
    get_user,
    get_users,
    listing_property,
    make_offer,
    unlist_property,
    update_listing_status,
    unfavorite_property,
    get_price_history,
    record_price_history,
    get_notifications,
    
)
from db_setup import get_connection
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from schemas import (
    AgencyCreate,
    AgencyUpdate,
    BrokerCreate,
    BrokerUpdate,
    CreateBid,
    CreateFavorite,
    CreatOffer,
    ListingCreate,
    PropertyFullCreate,
    PropertyUpdate,
    UpdateStatus,
    UserCreate,
    UserUpdate,
    CreatePriceHistory,
    
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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found or nothing to update")
    return {"message": f"User with id {user_id} has been updated."}

@app.delete("/user/{user_id}")
def delete_user_by_id(user_id: int):
    conn = get_connection()
    deleted = delete_user(conn, user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="property not found or nothing to update")
    return {"message": f"Property with id {property_id} has been updated."}

@app.delete("/property/{property_id}")
def delete_property_by_id(property_id : int):
    conn = get_connection()
    deleted = delete_property(conn, property_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": f"Property with id {property_id} has been deleted."}

#implementing agencies

@app.get("/agencies/")
def agencies():
    conn = get_connection()
    agencies = get_agencies(conn)
    if not agencies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No agencies found")
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="agency is not added")
    return {"agency" : agency}

@app.put("/agency/{agency_id}")
def update_agency(agency_id : int, data : AgencyUpdate):
    conn = get_connection()
    updated = edit_agency(conn, agency_id, data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found or nothing to update")
    return {"message": f"Agency with id {agency_id} has been updated."}

@app.delete("/agency/{agency_id}")
def delete_agency(agency_id : int):
    conn = get_connection()
    deleted = delete_agency_by_id(conn, agency_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    return {"message": f"Agency with id {agency_id} has been deleted."}

# implementing brokers endpoints

@app.get("/brokers/")
def brokers():
    conn = get_connection()
    brokers = get_brokers(conn)
    if not brokers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No brokers found")
    return {"brokers" : brokers}

@app.get("/broker/{broker_id}")
def broker_by_id(broker_id : int):
    conn = get_connection()
    broker = get_broker(conn, broker_id)
    if not broker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Broker not found")
    return {"broker" : broker}

@app.post("/broker/")
def create_broker(broker: BrokerCreate):
    conn = get_connection()
    broker = add_broker(conn, broker)
    if not broker:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Broker not added")
    return {"broker" : broker}

@app.put("/broker/{broker_id}")
def update_broker(broker_id : int, broker : BrokerUpdate):
    conn = get_connection()
    updated = edit_broker(conn, broker_id, broker)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Broker not found or nothing to update")
    return {"message": f"Broker with id {broker_id} has been updated."}

@app.delete("/broker/{broker_id}")
def delete_broker(broker_id : int):
    conn = get_connection()
    deleted = delete_broker_by_id(conn, broker_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Broker not found")
    return {"message": f"Broker with id {broker_id} has been deleted."}

@app.get("/property/list/")
def property_listings():
    conn = get_connection()
    listings = get_listings(conn)
    return {"listings": listings}

@app.post("/property/listing/")
def list_property(listing: ListingCreate):
    conn = get_connection()
    result = listing_property(conn, listing)
    if not result:
        raise HTTPException(status_code=400, detail="Listing creation failed")
    return {"listing": result}

@app.delete("/property/unlisting/{listing_id}")
def unlisting_property(listing_id: int):
    conn = get_connection()
    deleted = unlist_property(conn, listing_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="property not found")
    return {"message": f"Listing with id {listing_id} has been removed."}

@app.put("/property/edit_listing/{listing_id}")
def edit_listing_property(listing_id: int, update: UpdateStatus):
    conn = get_connection()
    updated = update_listing_status(conn, listing_id, update)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="property not found or nothing to update")
    return {"message": f"Listing with id {listing_id} has been updated."}

@app.get("/property/bids/{property_id}")
def property_bids(property_id: int):
    conn = get_connection()
    bids = get_bids_for_property(conn, property_id)
    if not bids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No bids found for this property")
    return {"bids": bids}

@app.post("/property/bid/")
def put_a_bid(data: CreateBid):
    conn = get_connection()
    bid = bid_on_property(conn, data)
    if not bid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return {"bid": bid}

@app.get("/property/offers/{property_id}")
def property_offers(property_id: int):
    conn = get_connection()
    offers = get_offers_for_property(conn, property_id)
    if not offers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No offers found for this property")
    return {"offers": offers}

@app.post("/property/offer/")
def make_an_offer(data: CreatOffer):
    conn = get_connection()
    offer = make_offer(conn, data)
    if not offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return {"offer": offer}

@app.get("/favorites/{user_id}")
def favorites(user_id: int):
    conn = get_connection()
    favorites = get_favorite_properties(conn, user_id)
    return {"favorites": favorites}

@app.post("/favorite/")
def add_favorite(data : CreateFavorite):
    conn = get_connection()
    favorite = add_favorite_property(conn, data)
    if not favorite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not add favorite")
    return {"favorite" : favorite}

@app.delete("/favorite/{favorite_id}")
def delete_favorite(favorite_id : int):
    conn = get_connection()
    deleted = unfavorite_property(conn, favorite_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")
    return {"message": f"Favorite with id {favorite_id} has been deleted."}

@app.get("/properties/price_history/{property_id}")
def price_history(property_id: int):
    conn = get_connection()
    price_history = get_price_history(conn, property_id)
    return {"price_history": price_history}

@app.post("/properties/price_history/")
def add_price_history(data: CreatePriceHistory):
    conn = get_connection()
    price_record = record_price_history(conn, data)
    if not price_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not record price history")
    return {"message": f"Property id {price_record["property_id"]} price has been recorded."}

@app.get("/notifications/{user_id}")
def notifications(user_id: int):
    conn = get_connection()
    notifications = get_notifications(conn, user_id)
    return {"notifications": notifications}
