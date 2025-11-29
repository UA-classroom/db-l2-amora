import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_NAME = os.getenv("DATABASE_NAME")
PASSWORD = os.getenv("PASSWORD")


def get_connection():
    """
    Function that returns a single connection
    In reality, we might use a connection pool, since
    this way we'll start a new connection each time
    someone hits one of our endpoints, which isn't great for performance
    """
    return psycopg2.connect(
        dbname="testdb",
        user="amr",  # change if needed
        password="682354",
        host="localhost",  # change if needed
        port="5432",  # change if needed
    )


def create_tables():
    """
    A function to create the necessary tables for the project.
    """
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE users (
        ID SERIAL PRIMARY KEY,
        full_name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL, 
        phone_number VARCHAR(20) NOT NULL,
        password VARCHAR(100) NOT NULL,
        role VARCHAR(100) NOT NULL,
        profile_picture VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE properties (
        ID SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        property_type VARCHAR(100) NOT NULL,
        listing_type VARCHAR(100) NOT NULL,
        start_price INT NOT NULL,
        end_price INT NOT NULL,
        price_per_sqr_meter INT NOT NULL,
        status VARCHAR(100) DEFAULT 'Active' NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute(""" CREATE TABLE features (
        property_id INT PRIMARY KEY REFERENCES properties(ID),
        rooms INT NOT NULL,
        bathrooms INT NOT NULL,
        size_sqm INT NOT NULL,
        floor INT NOT NULL,
        year_built INT NOT NULL,
        year_renovated INT,
        monthly_rent INT NOT NULL,
        total_floors INT NOT NULL,
        has_garden BOOLEAN NOT NULL,
        garden_size_sqm INT,
        has_elevator BOOLEAN NOT NULL,
        has_garage BOOLEAN NOT NULL,
        has_parking BOOLEAN NOT NULL,
        has_pool BOOLEAN NOT NULL,
        has_balcony BOOLEAN NOT NULL,
        energy_class VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE location (
        property_id INT PRIMARY KEY REFERENCES properties(ID),
        address VARCHAR(100) NOT NULL,
        city VARCHAR(100) NOT NULL,
        zip_code VARCHAR(100) NOT NULL,
        county VARCHAR(100) NOT NULL,
        state VARCHAR(100),
        country VARCHAR(100) NOT NULL,
        latitude DECIMAL NOT NULL,
        longitude DECIMAL NOT NULL,
        map_url VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE listing(
        id SERIAL PRIMARY KEY,
        property_id INT REFERENCES properties(ID),
        user_id INT REFERENCES users(ID),
        broker_id INT REFERENCES users(ID),
        start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        end_date TIMESTAMP,
        listing_status VARCHAR(100) DEFAULT 'Active' NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE property_images (
        id SERIAL PRIMARY KEY,
        property_id INT REFERENCES properties(ID),
        image_url VARCHAR(100) NOT NULL,
        image_order INT NOT NULL
        )""")

        cursor.execute("""CREATE TABLE property_videos (
        id SERIAL PRIMARY KEY,
        property_id INT REFERENCES properties(ID),
        video_url VARCHAR(100) NOT NULL,
        video_order INT NOT NULL
        )""")

        cursor.execute("""CREATE TABLE agencies (
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(ID),
        organization_number INT NOT NULL,
        history TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE brokers (
        user_id INT PRIMARY KEY REFERENCES users(ID),
        agency_id INT REFERENCES agencies(ID),
        years_of_experience INT NOT NULL,
        bio TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE property_brokers (
        property_id INT REFERENCES properties(ID),
        broker_id INT REFERENCES brokers(user_id),
        PRIMARY KEY (property_id, broker_id)
        )""")

        cursor.execute("""CREATE TABLE property_views(
        id SERIAL PRIMARY KEY,
        property_id INT REFERENCES properties(ID),
        user_id INT REFERENCES users(ID),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP        
        )""")

        cursor.execute("""CREATE TABLE interested_buyers(
        user_id INT REFERENCES users(ID),
        property_id INT REFERENCES properties(ID),
        is_contacted BOOLEAN NOT NULL,
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, property_id)
        )""")

        cursor.execute("""CREATE TABLE property_owners(
        user_id INT REFERENCES users(ID),
        property_id INT REFERENCES properties(ID),
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, property_id)
        )""")

        cursor.execute("""CREATE TABLE bids(
        id SERIAL PRIMARY KEY,
        property_id INT REFERENCES properties(ID),
        user_id INT REFERENCES users(ID),
        bid_amount INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE offers(
        id SERIAL PRIMARY KEY,
        property_id INT REFERENCES properties(ID),
        user_id INT REFERENCES users(ID),
        offer_amount INT NOT NULL,
        message VARCHAR(100),
        status VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE price_history(
        id SERIAL PRIMARY KEY,
        property_id INT REFERENCES properties(ID),
        end_price INT NOT NULL,
        record_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE favorites(
        id SERIAL PRIMARY KEY,
        property_id INT REFERENCES properties(ID),
        user_id INT REFERENCES users(ID),
        notes VARCHAR(100),
        is_contacted BOOLEAN NOT NULL,
        notify_price_change BOOLEAN NOT NULL,
        notify_status_change BOOLEAN NOT NULL,
        notify_new_message BOOLEAN NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE notifications(
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(ID),
        property_id INT REFERENCES properties(ID),
        favorite_id INT REFERENCES favorites(ID),
        title VARCHAR(50) NOT NULL,
        message VARCHAR(100) NOT NULL,
        is_read BOOLEAN NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE comparison_lists(
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(ID),
        name VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE comparison_list_items(
        comparison_list_id INT REFERENCES comparison_lists(ID),
        property_id INT REFERENCES properties(ID),
        PRIMARY KEY (comparison_list_id, property_id)
        )""")



        connection.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        connection.close()



if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
    print("Tables created successfully.")
