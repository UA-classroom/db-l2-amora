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
                        full_name, email, phone_number, profile_picture, role, created_at
                        FROM users;""")
            users = cursor.fetchall()
    return users


def get_user_by_id(conn, user_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT 
                        full_name, email, phone_number, profile_picture, role, created_at
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
                INSERT INTO users (full_name, email, profile_picture, phone_number, password, role,) 
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
            user_id = cursor.fetchone()["id"]
    return user_id


def edit_user(conn, user_id, user):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                UPDATE users 
                SET full_name = %s, email = %s, profile_picture = %s, phone_number = %s, password = %s, role = %s 
                WHERE id = %s;
            """,
                (
                    user.full_name,
                    user.email,
                    user.profile_picture,
                    user.phone_number,
                    user.password,
                    user.role,
                    user_id,
                ),
            )
            user_id = cursor.fetchone()["id"]
            if not user_id:
                raise HTTPException(status_code=404, detail="User not found")
    return user_id


def delete_user(conn, user_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            if not user_id:
                raise HTTPException(status_code=404, detail="User not found")
    return True


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
    LEFT JOIN listing l ON p.id = l.property_id
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


# def add_property(conn, property):
#     with conn:
#         with conn.cursor(cursor_factory=RealDictCursor) as cursor:
#             cursor.execute(
#                 """
#                 INSERT INTO properties (user_id, title, description, property_type, listing_type, start_price, status) 
#                 VALUES (%s, %s, %s, %s, %s, %s) 
#                 RETURNING id;
#             """,
#                 (
#                     property.user_id,
#                     property.title,
#                     property.description,
#                     property.property_type,
#                     property.listing_type,
#                     property.start_price,
#                     property.status,
#                 ),
#                 """
#                 INSERT INTO features (property_id, feature_id) 
#                 VALUES (%s, %s);
#             """,
#                 (
#                     property_id,
#                     feature_id,
#                 ),
#                 """
#                 INSERT INTO location (property_id, country, city, address) 
#                 VALUES (%s, %s, %s, %s);
#             """,
#                 (
#                     property_id,
#                     country,
#                     city,
#                     address,
#                 ),
#                 """
#                 INSERT INTO images (property_id, image_url) 
#                 VALUES (%s, %s);
#             """,
#                 (
#                     property_id,
#                     image_url,
#                 ),
#                 """
#                 INSERT INTO videos (property_id, video_url) 
#                 VALUES (%s, %s);
#             """,
#                 (
#                     property_id,
#                     video_url,
#                 ),
#             )
#             property_id = cursor.fetchone()["id"]
#     return property_id


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
