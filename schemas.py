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
    property_type: str
class PropertyUpdate(BaseModel):
    property_type: str

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
    
class AgencyCreate(BaseModel):
    user_id: int
    organization_number: int
    history : str

class AgencyUpdate(BaseModel):
    user_id: int | None = None
    organization_number: int | None = None
    history : str | None = None

class BrokerCreate(BaseModel):
    user_id: int
    agency_id: int | None = None
    license_number: str 
    years_of_experience: int
    bio: str 
    
class BrokerUpdate(BaseModel):
    agency_id: int | None = None
    license_number: str | None = None
    years_of_experience: int | None = None
    bio: str | None = None

class ListingCreate(BaseModel):
    property_id: int
    property_owner_id: int | None = None
    broker_id: int | None = None
    title: str
    description: str
    start_price: int
    start_date: str | None = None
    end_date: str 
    listing_status: str
    listing_type: str

class UpdateStatus(BaseModel):
    listing_status: str
    
class CreateBid(BaseModel):
    user_id: int
    property_id: int
    bid_amount: int
    
class CreatOffer(BaseModel):
    user_id: int
    property_id: int
    offer_amount: int
    status: str
    message: str | None = None
    
class CreateFavorite(BaseModel):
    user_id : int
    property_id : int
    notes : str | None = None
    is_contacted : bool
    notify_price_change : bool
    notify_status_change : bool
    notify_new_message : bool

class CreatePriceHistory(BaseModel):
    property_id : int
    end_price : int

class RecordView(BaseModel):
    user_id : int
    property_id : int
    
class CreateComparisonList(BaseModel):
    user_id : int
    name : str
    
class AddToComparisonList(BaseModel):
    comparison_list_id : int
    property_id : int
    
class ComparisonListUpdate(BaseModel):
    name: str