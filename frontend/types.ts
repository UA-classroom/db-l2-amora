
export interface Property {
  id: number;
  title: string;
  description: string;
  property_type: string;
  listing_type: string;
  start_price: number;
  status: string;
  rooms: number;
  bathrooms: number;
  size_sqm: number;
  floor: number;
  year_built: number;
  monthly_rent: number;
  total_floors: number;
  has_garden: boolean;
  has_parking: boolean;
  has_pool: boolean;
  has_balcony: boolean;
  energy_class: string;
  city: string;
  address: string;
  zip_code: string;
  country: string;
  latitude: number;
  longitude: number;
  map_url: string | null;
  start_date: string;
  end_date: string;
  user_name: string;
  user_email: string;
  user_phone: string;
  user_picture: string | null;
  years_of_experience: number | null;
  broker_bio: string | null;
  broker_name: string | null;
  broker_email: string | null;
  broker_phone: string | null;
  broker_picture: string | null;
  agency_email: string | null;
  agency_name: string | null;
  agency_phone: string | null;
  agency_picture: string | null;
  listing_status: string;
}

export interface Bid {
    id: number;
    user_id: number;
    property_id: number;
    bid_amount: number;
    created_at: string;
}

export interface Offer {
    id: number;
    user_id: number;
    property_id: number;
    offer_amount: number;
    message: string | null;
    status: string;
    created_at: string;
}
