from tkinter import N

import psycopg2
from fastapi import HTTPException
from httpx import get
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
        p.id, p.title, p.description, p.property_type, p.listing_type, p.start_price, p.status,
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
                p.id, p.title, p.description, p.property_type, p.listing_type, p.start_price, p.status,
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
            LEFT JOIN users u ON p.user_id = u.id
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

def edit_property(conn, property_id, property):
    with conn:
        with conn.cursor(cursor_factory = RealDictCursor) as cursor:
            updates = []
            values = []
            if property.user_id is not None:
                updates.append("user_id = %s")
                values.append(property.user_id)
            if property.title is not None:
                updates.append("title = %s")
                values.append(property.title)    
            if property.description is not None:
                updates.append("description = %s")
                values.append(property.description)   
            if property.property_type is not None:
                updates.append("property_type = %s")
                values.append(property.property_type)   
            if property.listing_type is not None:
                updates.append("listing_type = %s")
                values.append(property.listing_type)   
            if property.start_price is not None:
                updates.append("start_price = %s")
                values.append(property.start_price)   
            if property.status is not None:
                updates.append("status = %s")
                values.append(property.status)
            if not updates:
                return None
            
            values.append(property_id)
            
            cursor.execute(f"""UPDATE properties 
                        SET {', '.join(updates)} 
                        WHERE id = %s 
                        RETURNING id """, 
                        (values))
            return cursor.fetchone()

def delete_property(conn, property_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""DELETE FROM properties WHERE id = %s RETURNING id""", (property_id,))
            return cursor.fetchone()

# Agencies
def get_agencies(conn):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT 
                        a.id AS agency_id,
                        a.user_id,
                        a.organization_number, 
                        a.history, 
                        u.full_name AS agency_name, 
                        u.email AS agency_email,
                        u.phone_number AS agency_phone_number,
                        u.profile_picture AS agency_profile_picture,
                        u.created_at
                        FROM agencies a
                        JOIN users u ON a.user_id = u.id;
                        """)
            agencies = cursor.fetchall()
    return agencies

def get_agency(conn, agency_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""SELECT 
                        a.id AS agency_id,
                        a.user_id,
                        a.organization_number, 
                        a.history, 
                        u.full_name AS agency_name, 
                        u.email AS agency_email,
                        u.phone_number AS agency_phone_number,
                        u.profile_picture AS agency_profile_picture,
                        u.created_at
                        FROM agencies a
                        JOIN users u ON a.user_id = u.id
                        WHERE a.id = %s;
                        """,(agency_id,))
            agency = cursor.fetchone()
            if not agency:
                raise HTTPException(status_code=404, detail="Agency not found")
    return agency

def add_agency(conn, agency):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""INSERT INTO agencies (user_id, organization_number, history) 
                        VALUES (%s, %s, %s)
                        RETURNING id; 
                        """,
                        (
                            agency.user_id,
                            agency.organization_number,
                            agency.history
                        ))
            agency = cursor.fetchone()
    return get_agency(conn,agency["id"])

def edit_agency(conn, agency_id, agency):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            updates = []
            values = []
            if agency.user_id is not None:
                updates.append("user_id = %s")
                values.append(agency.user_id)
            if agency.organization_number is not None:
                updates.append("organization_number = %s")
                values.append(agency.organization_number)
            if agency.history is not None:
                updates.append("history = %s")
                values.append(agency.history)
            if not updates:
                return None
            
            values.append(agency_id)
                
            cursor.execute(F"""UPDATE agencies
                        SET {', '.join(updates)}
                        WHERE id = %s
                        RETURNING id 
                        """,
                        (values))
            return cursor.fetchone()

def delete_agency_by_id(conn, agency_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""DELETE FROM agencies WHERE id = %s RETURNING id""", (agency_id,))
            return cursor.fetchone()

def get_brokers(conn):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT 
                b.user_id AS broker_id,
                b.agency_id,
                b.license_number,
                u.full_name AS broker_name,
                u.email AS broker_email,
                u.profile_picture,
                b.years_of_experience, b.bio, b.created_at
                FROM brokers b 
                JOIN users u ON b.user_id = u.id;
                """)
            brokers = cursor.fetchall()
    return brokers

def get_broker(conn, broker_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT 
                b.user_id AS broker_id,
                b.agency_id,
                b.license_number,
                u.full_name AS broker_name,
                u.email AS broker_email,
                u.profile_picture,
                b.years_of_experience, b.bio,
                b.created_at
                FROM brokers b 
                JOIN users u ON b.user_id = u.id
                WHERE b.user_id = %s;
                """, (broker_id,))
            broker = cursor.fetchone()
            if not broker:
                raise HTTPException(status_code=404, detail="Broker not found")
    return broker

def add_broker(conn, broker):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO 
                brokers (user_id, agency_id, license_number, years_of_experience, bio) 
                VALUES (%s, %s, %s, %s, %s)
                RETURNING user_id;
                """,
                (
                    broker.user_id,
                    broker.agency_id,
                    broker.license_number,
                    broker.years_of_experience,
                    broker.bio
                ))
            broker = cursor.fetchone()
    return get_broker(conn, broker["user_id"])

def edit_broker(conn, broker_id, broker):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            updates = []
            values = []
            if broker.agency_id is not None:
                updates.append("agency_id = %s")
                values.append(broker.agency_id)
            if broker.license_number is not None:
                updates.append("license_number = %s")
                values.append(broker.license_number)
            if broker.years_of_experience is not None:
                updates.append("years_of_experience = %s")
                values.append(broker.years_of_experience)
            if broker.bio is not None:
                updates.append("bio = %s")
                values.append(broker.bio)
            if not updates:
                return None
            
            values.append(broker_id)
                
            cursor.execute(F"""UPDATE brokers
                        SET {', '.join(updates)}
                        WHERE user_id = %s
                        RETURNING user_id 
                        """,
                        (values))
            return cursor.fetchone()

def delete_broker_by_id(conn, broker_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""DELETE FROM brokers WHERE user_id = %s 
                        RETURNING user_id""", (broker_id,))
            return cursor.fetchone()

# Add more functions as needed for other database operations

def list_property(conn, property_id, user_id=None, broker_id=None):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO listing (property_id, user_id, broker_id) 
                VALUES (%s, %s, %s)
                RETURNING id, property_id, user_id, broker_id, start_date, end_date, listing_status;
                """,
                (property_id, user_id, broker_id)
            )
            listing = cursor.fetchone()
    return listing

def unlist_property(conn, listing_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """DELETE FROM listing 
                WHERE id = %s
                RETURNING id, property_id, user_id, broker_id, start_date, end_date, listing_status;
                """,
                (listing_id,)
            )
            listing = cursor.fetchone()
    return listing

def get_listings(conn):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT 
                id, property_id, user_id, broker_id, start_date, end_date, listing_status
                FROM listing;
                """
            )
            listings = cursor.fetchall()
    return listings

def update_listing_status(conn, listing_id, listing_status):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """UPDATE listing 
                SET listing_status = %s
                WHERE id = %s
                RETURNING id, property_id, user_id, broker_id, start_date, end_date, listing_status;
                """,
                (listing_status, listing_id)
            )
            listing = cursor.fetchone()
    return listing

def delete_listing(conn, listing_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """DELETE FROM listing 
                WHERE id = %s
                RETURNING id;
                """,
                (listing_id,)
            )
            listing = cursor.fetchone()
    return listing

def bid_on_property(conn, user_id, property_id, bid_amount):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO bids (user_id, property_id, bid_amount) 
                VALUES (%s, %s, %s)
                RETURNING id, user_id, property_id, bid_amount, created_at;
                """,
                (user_id, property_id, bid_amount)
            )
            bid = cursor.fetchone()
    return bid

def get_bids_for_property(conn, property_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT 
                id, user_id, property_id, bid_amount, created_at
                FROM bids
                WHERE property_id = %s;
                """,
                (property_id,)
            )
            bids = cursor.fetchall()
    return bids

def make_offer(conn, user_id, property_id, offer_amount, message, status):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO offers (user_id, property_id, offer_amount, message, status) 
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, user_id, property_id, offer_amount, message, status, created_at;
                """,
                (user_id, property_id, offer_amount, message, status)
            )
            offer = cursor.fetchone()
    return offer

def get_offers_for_property(conn, property_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT 
                id, user_id, property_id, offer_amount, message, status, created_at
                FROM offers
                WHERE property_id = %s;
                """,
                (property_id,)
            )
            offers = cursor.fetchall()
    return offers

def favorite_property(conn, user_id, property_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO favorite_properties (user_id, property_id) 
                VALUES (%s, %s)
                RETURNING user_id, property_id;
                """,
                (user_id, property_id)
            )
            favorite = cursor.fetchone()
    return favorite

def get_favorite_properties(conn, user_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT 
                user_id, property_id
                FROM favorite_properties
                WHERE user_id = %s;
                """,
                (user_id,)
            )
            favorites = cursor.fetchall()
    return favorites

def unfavorite_property(conn, user_id, property_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """DELETE FROM favorite_properties 
                WHERE user_id = %s AND property_id = %s
                RETURNING user_id, property_id;
                """,
                (user_id, property_id)
            )
            favorite = cursor.fetchone()
    return favorite

def record_price_history(conn, property_id, end_price):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO price_history (property_id, end_price) 
                VALUES (%s, %s)
                RETURNING id, property_id, end_price, record_at;
                """,
                (property_id, end_price)
            )
            price_record = cursor.fetchone()
    return price_record

def get_price_history(conn, property_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT 
                id, property_id, end_price, record_at
                FROM price_history
                WHERE property_id = %s;
                """,
                (property_id,)
            )
            price_history = cursor.fetchall()
    return price_history

def add_notification(conn, user_id, property_id, favorite_id, message):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO notifications (user_id, property_id, favorite_id, message) 
                VALUES (%s, %s, %s, %s)
                RETURNING id, user_id, property_id, favorite_id, message, is_read, created_at;
                """,
                (user_id, property_id, favorite_id, message)
            )
            notification = cursor.fetchone()
    return notification

def get_notifications(conn, user_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT 
                id, user_id, property_id, favorite_id, message, is_read, created_at
                FROM notifications
                WHERE user_id = %s;
                """,
                (user_id,)
            )
            notifications = cursor.fetchall()
    return notifications

def mark_notification_as_read(conn, notification_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """UPDATE notifications 
                SET is_read = TRUE
                WHERE id = %s
                RETURNING id, user_id, property_id, favorite_id, message, is_read, created_at;
                """,
                (notification_id,)
            )
            notification = cursor.fetchone()
    return notification

def delete_notification(conn, notification_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """DELETE FROM notifications 
                WHERE id = %s
                RETURNING id;
                """,
                (notification_id,)
            )
            notification = cursor.fetchone()
    return notification

def get_property_views(conn, property_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT 
                user_id, property_id, view_count, last_viewed_at
                FROM property_views
                WHERE property_id = %s;
                """,
                (property_id,)
            )
            views = cursor.fetchall()
    return views

def record_property_view(conn, user_id, property_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO property_views (user_id, property_id, view_count, last_viewed_at) 
                VALUES (%s, %s, 1, CURRENT_TIMESTAMP)
                ON CONFLICT (user_id, property_id) 
                DO UPDATE SET 
                    view_count = property_views.view_count + 1,
                    last_viewed_at = CURRENT_TIMESTAMP
                RETURNING user_id, property_id, view_count, last_viewed_at;
                """,
                (user_id, property_id)
            )
            view_record = cursor.fetchone()
    return view_record

def compare_properties(conn, user_id, property_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """INSERT INTO comparison_lists (user_id, property_id) 
                VALUES (%s, %s)
                RETURNING user_id, property_id;
                """,
                (user_id, property_id)
            )
            comparison = cursor.fetchone()
    return comparison

def get_comparison_list(conn, user_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """SELECT 
                user_id, property_id
                FROM comparison_lists
                WHERE user_id = %s;
                """,
                (user_id,)
            )
            comparison_list = cursor.fetchall()
    return comparison_list

def remove_from_comparison(conn, user_id, property_id):
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """DELETE FROM comparison_lists 
                WHERE user_id = %s AND property_id = %s
                RETURNING user_id, property_id;
                """,
                (user_id, property_id)
            )
            comparison = cursor.fetchone()
    return comparison
