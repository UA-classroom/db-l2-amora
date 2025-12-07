# Add Pydantic schemas here that you'll use in your routes / endpoints
# Pydantic schemas are used to validate data that you receive, or to make sure that whatever data
# you send back to the client follows a certain structure
from calendar import c

from pydantic import BaseModel


class UserCreate(BaseModel):
    full_name: str
    email: str
    phone_number: str
    password: str
    role: str
    profile_picture: str | None = None

class UserUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    password: str | None = None
    role: str | None = None
    profile_picture: str | None = None
    
class PropertyCreate(BaseModel):
    user_id: int
    title: str
    description: str
    property_type: str
    listing_type: str
    start_price: int
    end_price: int | None = None
    status: str | None = 'Active'

class PropertyUpdate(BaseModel):
    user_id: int
    title: str | None = None
    description: str | None = None
    property_type: str | None = None
    listing_type: str | None = None
    start_price: int | None = None
    end_price: int | None = None
    status: str | None = None
    
class FeatureCreate(BaseModel):
    rooms: int
    bathrooms: int
    size_sqm: int
    floor: int
    year_built: int
    year_renovated: int | None = None
    monthly_rent: int
    total_floors: int
    has_garden: bool
    garden_size_sqm: int | None = None
    has_elevator: bool
    has_garage: bool
    has_parking: bool
    has_pool: bool
    has_balcony: bool
    energy_class: str
class LocationCreate(BaseModel):
    address: str
    city: str
    zip_code: str
    county: str
    state: str | None = None
    country: str
    latitude: float
    longitude: float
    map_url: str

class imagesCreate(BaseModel):
    image_url: str
    image_order: int

class vedioCreate(BaseModel):
    video_url: str
    video_order: int
    
class PropertyFullCreate(BaseModel):
    property: PropertyCreate
    features: FeatureCreate
    location: LocationCreate
    images: list[imagesCreate] = []
    videos: list[vedioCreate] = []