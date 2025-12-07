from tkinter import N
from httpx import get
import psycopg2
from fastapi import HTTPException
from psycopg2.extras import RealDictCursor

"""
This file is responsible for making database queries, which your fastapi endpoints/routes can use.
The reason we split them up is to avoid clutter in the endpoints, so that the endpoints might focus on other tasks 

- Try to return results with cursor.fetchall() or cursor.fetchone() when possible
- Make sure you always give the user response if something went right or wrong, sometimes 
you might need to use the RETURNING keyword to garantuee that something went right / wrong
e.g when making DELETE or UPDATE queries
- No need to use a class here
- Try to raise exceptions to make them more reusable and work a lot with returns
- You will need to decide which parameters each function should receive. All functions 
start with a connnection parameter.
- Below, a few inspirational functions exist - feel free to completely ignore how they are structured
- E.g, if you decide to use psycopg3, you'd be able to directly use pydantic models with the cursor, these examples are however using psycopg2 and RealDictCursor
"""


### THIS IS JUST AN EXAMPLE OF A FUNCTION FOR INSPIRATION FOR A LIST-OPERATION (FETCHING MANY ENTRIES)

# USERS
def get_users(conn):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT 
                        id, full_name, email, phone_number, profile_picture, role, created_at
                        FROM users;""")
            users = cursor.fetchall()
    return users


def get_user(conn, user_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT 
                        id, full_name, email, phone_number, profile_picture, role, created_at
                        FROM users 
                        WHERE id = %s;""", (user_id,))
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
    return user


def add_user(conn, user):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO users (full_name, email, profile_picture, phone_number, password, role) 
                VALUES (%s, %s, %s, %s, %s, %s) 
                RETURNING id;
            """,
                (
                    user.full_name,
                    user.email,
                    user.profile_picture,
                    user.phone_number,
                    user.password,
                    user.role,
                ),
            )
            user = cursor.fetchone()
    return get_user(conn, user["id"])


def edit_user(conn, user_id, user):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            updates = []
            values = []
            
            if user.full_name is not None:
                updates.append("full_name = %s")
                values.append(user.full_name)
            if user.email is not None:
                updates.append("email = %s")
                values.append(user.email)
            if user.phone_number is not None:
                updates.append("phone_number = %s")
                values.append(user.phone_number)
            if user.profile_picture is not None:
                updates.append("profile_picture = %s")
                values.append(user.profile_picture)
                
            if not updates:
                return None  # No updates to perform
        
            values.append(user_id)
            
            cursor.execute(f"""
                UPDATE users 
                SET {', '.join(updates)}
                WHERE id = %s
                RETURNING id
            """, values)
            return cursor.fetchone()


def delete_user(conn, user_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""DELETE FROM users WHERE id = %s RETURNING id""", (user_id,))
            return cursor.fetchone()


# PROPERTIES
def get_properties(conn):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(""" 
    SELECT 
        p.id, p.title, p.description, p.property_type, p.start_price, p.status,
        f.rooms, f.bathrooms, f.size_sqm, f.floor, f.year_built, 
        f.monthly_rent, f.total_floors, f.has_garden, f.has_parking, 
        f.has_pool, f.has_balcony, f.energy_class,

        loc.city, loc.address, loc.zip_code, loc.country, 
        loc.latitude, loc.longitude, loc.map_url,
        l.start_date, l.end_date,

        u.full_name AS user_name,
        u.email AS user_email,
        u.phone_number AS user_phone,
        u.profile_picture AS user_picture,

        b.years_of_experience,
        b.bio AS broker_bio,
        b_user.full_name AS broker_name,
        b_user.email AS broker_email,
        b_user.phone_number AS broker_phone,
        b_user.profile_picture AS broker_picture,
        
        a_user.email AS agency_email,
        a_user.full_name AS agency_name,
        a_user.phone_number AS agency_phone,
        a_user.profile_picture AS agency_picture
        
    FROM properties p
    JOIN features f ON p.id = f.property_id
    JOIN location loc ON p.id = loc.property_id
    JOIN listing l ON p.id = l.property_id
    LEFT JOIN users u ON l.user_id = u.id
    LEFT JOIN brokers b ON l.broker_id = b.user_id
    LEFT JOIN users b_user ON b.user_id = b_user.id
    LEFT JOIN agencies a ON b.agency_id = a.id
    LEFT JOIN users a_user ON a.user_id = a_user.id
    WHERE p.status = 'Active'
""")
            properties = cursor.fetchall()
    return properties


def get_property_by_id(conn, property_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT
                p.id, p.title, p.description, p.property_type, p.start_price, p.status,
                f.rooms, f.bathrooms, f.size_sqm, f.floor, f.year_built, 
                f.monthly_rent, f.total_floors, f.has_garden, f.has_parking, 
                f.has_pool, f.has_balcony, f.energy_class,

                loc.city, loc.address, loc.zip_code, loc.country, 
                loc.latitude, loc.longitude, loc.map_url,
                l.start_date, l.end_date,

                u.full_name AS user_name,
                u.email AS user_email,
                u.phone_number AS user_phone,
                u.profile_picture AS user_picture,

                b.years_of_experience,
                b.bio AS broker_bio,
                b_user.full_name AS broker_name,
                b_user.email AS broker_email,
                b_user.phone_number AS broker_phone,
                b_user.profile_picture AS broker_picture,
                
                a_user.email AS agency_email,
                a_user.full_name AS agency_name,
                a_user.phone_number AS agency_phone,
                a_user.profile_picture AS agency_picture
                
            FROM properties p
            JOIN features f ON p.id = f.property_id
            JOIN location loc ON p.id = loc.property_id
            LEFT JOIN listing l ON p.id = l.property_id
            LEFT JOIN users u ON l.user_id = u.id
            LEFT JOIN brokers b ON l.broker_id = b.user_id
            LEFT JOIN users b_user ON b.user_id = b_user.id
            LEFT JOIN agencies a ON b.agency_id = a.id
            LEFT JOIN users a_user ON a.user_id = a_user.id
            WHERE p.id = %s and p.status = 'Active'
            """,
                (property_id,),
            )
            property = cursor.fetchone()
            if not property:
                raise HTTPException(status_code=404, detail="Property not found")
    return property


def add_property(conn, property, features, location, images, videos):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO properties (user_id, title, description, property_type, listing_type, start_price, status) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    property.user_id,
                    property.title,
                    property.description,
                    property.property_type,
                    property.listing_type,
                    property.start_price,
                    property.status
                ))
            property_id = cursor.fetchone()["id"]
            if not property_id:
                raise HTTPException(status_code=404, detail="Property is not created")
            
            cursor.execute(
                """
                INSERT INTO FEATURES (property_id, rooms, bathrooms, size_sqm, floor, year_built, year_renovated,
                monthly_rent, total_floors, has_garden, garden_size_sqm, has_elevator, has_garage, has_parking, has_pool, has_balcony, energy_class) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    property_id,
                    features.rooms,
                    features.bathrooms,
                    features.size_sqm,
                    features.floor,
                    features.year_built,
                    features.year_renovated,
                    features.monthly_rent,
                    features.total_floors,
                    features.has_garden,
                    features.garden_size_sqm,
                    features.has_elevator,
                    features.has_garage,
                    features.has_parking,
                    features.has_pool,
                    features.has_balcony,
                    features.energy_class
                ))
            
            cursor.execute( """
                INSERT INTO location (property_id, address, city, zip_code, county, state, country, latitude, longitude, map_url) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    property_id,
                    location.address,
                    location.city,
                    location.zip_code,
                    location.county,
                    location.state,
                    location.country,
                    location.latitude,
                    location.longitude,
                    location.map_url
                ))
            
            for image in images:
                cursor.execute(
                    """
                    INSERT INTO property_images (property_id, image_url, image_order) 
                    VALUES (%s, %s, %s)
                    """,
                    (
                        property_id,
                        image.image_url,
                        image.image_order
                    ))
            
            for video in videos:
                cursor.execute(
                    """
                    INSERT INTO property_videos (property_id, video_url, video_order) 
                    VALUES (%s, %s, %s)
                    """,
                    (
                        property_id,
                        video.video_url,
                        video.video_order,
                    ))
            
    return get_property_by_id(conn, property_id)


# def edit_property(conn, property_id, property):
#     with conn:
#         with conn.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute(
#                 """
#                 UPDATE listing 
#                 SET title = %s, description = %s, property_type = %s, listing_type = %s, start_price = %s, status = %s 
#                 WHERE id = %s;
#             """,
#                 (
#                     property.title,
#                     property.description,
#                     property.property_type,
#                     property.listing_type,
#                     property.start_price,
#                     property.status,
#                     property_id,
#                 ),
#             )
#             property_id = cursor.fetchone()["id"]
#             if not property_id:
#                 raise HTTPException(status_code=404, detail="Property not found")
#     return property_id


# def delete_property(conn, property_id):
#     with conn:
#         with conn.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute("DELETE FROM listing WHERE id = %s;", (property_id,))
#             if not property_id:
#                 raise HTTPException(status_code=404, detail="Property not found")
#     return True


# # FEATURES


# def get_agencies(conn):
#     with conn:
#         with conn.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute("SELECT * FROM agencies;")
#             agencies = cursor.fetchall()
#     return agencies


# def get_brokers(conn):
#     with conn:
#         with conn.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute(
#                 "SELECT b.*, u.full_name, u.email, u.profile_picture FROM brokers b JOIN users u ON b.user_id = u.id"
#             )
#             brokers = cursor.fetchall()
    # return brokers


### THIS IS JUST INSPIRATION FOR A DETAIL OPERATION (FETCHING ONE ENTRY)
# def get_item(conn, item_id):
#     with conn:
#         with conn.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute("""SELECT * FROM items WHERE id = %s""", (item_id,))
#             item = cursor.fetchone()
#             return item


### THIS IS JUST INSPIRATION FOR A CREATE-OPERATION
# def add_item(conn, title, description):
#     with conn:
#         with conn.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute(
#                 "INSERT INTO items (title, description) VALUES (%s, %s) RETURNING id;",
#                 (title, description),
#             )
#             item_id = cursor.fetchone()["id"]
#     return item_id
