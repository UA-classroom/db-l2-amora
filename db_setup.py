import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

def get_connection():
    """
    Function that returns a single connection
    In reality, we might use a connection pool, since
    this way we'll start a new connection each time
    someone hits one of our endpoints, which isn't great for performance
    """
    return psycopg2.connect(
        dbname=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST", "localhost"),
        port=os.getenv("DATABASE_PORT", "5432"),
    )


def create_tables():
    """
    A function to create the necessary tables for the project. 
    """
    cursor = None
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL, 
        phone_number VARCHAR(20) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL,
        role VARCHAR(100) NOT NULL,
        profile_picture VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS properties (
        id SERIAL PRIMARY KEY,
        property_type VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS features (
        property_id INT PRIMARY KEY REFERENCES properties(id) ON DELETE CASCADE,
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

        cursor.execute("""CREATE TABLE IF NOT EXISTS location (
        property_id INT PRIMARY KEY REFERENCES properties(id) ON DELETE CASCADE,
        address VARCHAR(100) NOT NULL,
        city VARCHAR(100) NOT NULL,
        zip_code VARCHAR(100) NOT NULL,
        county VARCHAR(100) NOT NULL,
        state VARCHAR(100),
        country VARCHAR(100) NOT NULL,
        latitude DECIMAL (10, 8) NOT NULL,
        longitude DECIMAL (10, 8) NOT NULL,
        map_url VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS property_images (
        id SERIAL PRIMARY KEY,
        property_id INT REFERENCES properties(id) ON DELETE CASCADE,
        image_url VARCHAR(100) NOT NULL,
        image_order INT NOT NULL
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS property_videos (
        id SERIAL PRIMARY KEY,
        property_id INT REFERENCES properties(id) ON DELETE CASCADE,
        video_url VARCHAR(100) NOT NULL,
        video_order INT NOT NULL
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS agencies (
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(id) ON DELETE RESTRICT,
        organization_number VARCHAR(100) UNIQUE NOT NULL,
        history TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS brokers (
        user_id INT PRIMARY KEY REFERENCES users(id) ON DELETE RESTRICT,
        agency_id INT REFERENCES agencies(id),
        license_number VARCHAR(100) NOT NULL,
        years_of_experience INT NOT NULL,
        bio TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS property_owner(
        user_id INT REFERENCES users(id) ON DELETE RESTRICT,
        property_id INT REFERENCES properties(id) ON DELETE CASCADE,
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, property_id)
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS listing_property (
        id SERIAL PRIMARY KEY,
        property_id INT REFERENCES properties(id) ON DELETE CASCADE,
        property_owner_id INT REFERENCES users(id),
        broker_id INT REFERENCES brokers(user_id),
        title VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        end_date TIMESTAMP,
        listing_status VARCHAR(100) DEFAULT 'Active' NOT NULL,
        listing_type VARCHAR(100) NOT NULL,
        start_price INT NOT NULL,
        end_price INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CHECK (
        (property_owner_id IS NOT NULL AND broker_id IS NULL)
        OR
        (property_owner_id IS NULL AND broker_id IS NOT NULL)
        )
        );
        """)
        
        cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS one_active_listing_per_broker_property
        ON listing_property(property_id, broker_id)
        WHERE broker_id IS NOT NULL
        AND listing_status = 'Active';
        """)
        
        cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS one_active_listing_per_owner
        ON listing_property(property_owner_id)
        WHERE property_owner_id IS NOT NULL
        AND listing_status = 'Active';
        """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS property_brokers (
        property_id INT REFERENCES properties(id) ON DELETE CASCADE,
        broker_id INT REFERENCES brokers(user_id) ON DELETE CASCADE,
        PRIMARY KEY (property_id, broker_id)
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS property_views(
        id SERIAL PRIMARY KEY,
        property_id INT REFERENCES properties(id) ON DELETE CASCADE,
        user_id INT REFERENCES users(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP        
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS interested_buyers(
        user_id INT REFERENCES users(id) ON DELETE RESTRICT,
        property_id INT REFERENCES properties(id) ON DELETE CASCADE,
        is_contacted BOOLEAN NOT NULL,
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, property_id)
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS bids(
        id SERIAL PRIMARY KEY,
        property_id INT REFERENCES properties(id) ON DELETE CASCADE,
        user_id INT REFERENCES users(id) ON DELETE SET NULL,
        bid_amount INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS offers(
        id SERIAL PRIMARY KEY,
        property_id INT REFERENCES properties(id) ON DELETE CASCADE,
        user_id INT REFERENCES users(id) ON DELETE SET NULL,
        offer_amount INT NOT NULL,
        message VARCHAR(100),
        status VARCHAR(100) NOT NULL DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS price_history(
        id SERIAL PRIMARY KEY,
        property_id INT REFERENCES properties(id) ON DELETE CASCADE,
        end_price INT NOT NULL,
        record_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS favorites(
        id SERIAL PRIMARY KEY,
        property_id INT REFERENCES properties(id) ON DELETE CASCADE,
        user_id INT REFERENCES users(id) ON DELETE CASCADE,
        notes VARCHAR(100),
        is_contacted BOOLEAN NOT NULL,
        notify_price_change BOOLEAN NOT NULL,
        notify_status_change BOOLEAN NOT NULL,
        notify_new_message BOOLEAN NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_favorites_user_id 
        ON favorites(user_id);
        """)

        cursor.execute("""CREATE TABLE IF NOT EXISTS notifications(
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(id) ON DELETE CASCADE,
        property_id INT REFERENCES properties(id) ON DELETE CASCADE,
        favorite_id INT REFERENCES favorites(id) ON DELETE CASCADE,
        title VARCHAR(50) NOT NULL,
        message VARCHAR(100) NOT NULL,
        is_read BOOLEAN NOT NULL DEFAULT FALSE,
        type VARCHAR(50) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS comparison_lists(
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(id) ON DELETE CASCADE,
        name VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS comparison_list_items(
        comparison_list_id INT REFERENCES comparison_lists(id) ON DELETE CASCADE,
        property_id INT REFERENCES properties(id) ON DELETE CASCADE,
        PRIMARY KEY (comparison_list_id, property_id)
        )""")



        connection.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
    print("Tables created successfully.")
