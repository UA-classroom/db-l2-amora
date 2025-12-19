
import React from 'react';
import { Property } from '../types';
import { BedIcon, BathIcon, SizeIcon, CalendarIcon, EnergyIcon, GarageIcon, LocationIcon } from './Icons';

interface PropertyDetailProps {
  property: Property;
  onBack: () => void;
}

const DetailItem: React.FC<{ icon: React.ReactNode; label: string; value: string | number | boolean }> = ({ icon, label, value }) => (
    <div className="flex flex-col items-center justify-center p-4 bg-slate-100 dark:bg-slate-800/50 rounded-lg text-center">
        <div className="text-indigo-400 mb-2">{icon}</div>
        <p className="text-sm text-slate-500 dark:text-slate-400">{label}</p>
        <p className="font-bold text-slate-800 dark:text-slate-200">
            {typeof value === 'boolean' ? (value ? 'Yes' : 'No') : value}
        </p>
    </div>
);

const PropertyDetail: React.FC<PropertyDetailProps> = ({ property, onBack }) => {
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(price);
  };
  
  return (
    <div className="max-w-6xl mx-auto">
      <button 
        onClick={onBack} 
        className="mb-6 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        &larr; Back to Listings
      </button>

      <div className="bg-white dark:bg-slate-800 rounded-xl shadow-xl overflow-hidden">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-0">
            <div className="md:col-span-3">
                <img src={`https://picsum.photos/seed/${property.id}/800/600`} alt={property.title} className="w-full h-full object-cover" />
            </div>
            <div className="md:col-span-2 p-8 flex flex-col">
                <h1 className="text-3xl lg:text-4xl font-extrabold text-slate-900 dark:text-white mb-2">{property.title}</h1>
                <div className="flex items-center text-slate-500 dark:text-slate-400 text-md mb-4">
                    <LocationIcon className="w-5 h-5 mr-2" />
                    <span>{property.address}, {property.city}, {property.country}</span>
                </div>
                <p className="text-4xl font-bold text-indigo-600 dark:text-indigo-400 mb-6">
                  {formatPrice(property.start_price)}
                  {property.listing_type === 'For Rent' && <span className="text-lg font-normal text-slate-500 dark:text-slate-400">/month</span>}
                </p>
                
                <p className="text-slate-600 dark:text-slate-300 mb-6 flex-grow">{property.description}</p>
                
                <div className="mt-auto space-y-4">
                    <button className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-4 rounded-lg transition duration-300">
                        Place a Bid
                    </button>
                    <button className="w-full bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 dark:hover:bg-slate-600 text-slate-800 dark:text-white font-bold py-3 px-4 rounded-lg transition duration-300">
                        Make an Offer
                    </button>
                </div>
            </div>
        </div>

        <div className="p-8 border-t border-slate-200 dark:border-slate-700">
            <h2 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white">Property Features</h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                <DetailItem icon={<BedIcon className="w-8 h-8"/>} label="Rooms" value={property.rooms} />
                <DetailItem icon={<BathIcon className="w-8 h-8"/>} label="Bathrooms" value={property.bathrooms} />
                <DetailItem icon={<SizeIcon className="w-8 h-8"/>} label="Size" value={`${property.size_sqm} m²`} />
                <DetailItem icon={<CalendarIcon className="w-8 h-8"/>} label="Year Built" value={property.year_built} />
                <DetailItem icon={<EnergyIcon className="w-8 h-8"/>} label="Energy Class" value={property.energy_class} />
                <DetailItem icon={<GarageIcon className="w-8 h-8"/>} label="Parking" value={property.has_parking} />
            </div>
        </div>

        {property.broker_name && (
        <div className="p-8 bg-slate-50 dark:bg-slate-800/50 border-t border-slate-200 dark:border-slate-700">
             <h2 className="text-2xl font-bold mb-6 text-slate-800 dark:text-white">Contact Agent</h2>
             <div className="flex items-center">
                <img src={property.broker_picture || `https://picsum.photos/seed/broker${property.id}/100`} alt={property.broker_name} className="w-24 h-24 rounded-full mr-6 object-cover"/>
                <div>
                    <h3 className="text-xl font-bold text-slate-900 dark:text-white">{property.broker_name}</h3>
                    <p className="text-indigo-500 dark:text-indigo-400">{property.agency_name}</p>
                    <p className="text-slate-600 dark:text-slate-300 mt-2">{property.broker_bio}</p>
                    <div className="mt-3 space-x-4">
                        <a href={`mailto:${property.broker_email}`} className="text-indigo-600 hover:underline">{property.broker_email}</a>
                        <span className="text-slate-400">|</span>
                        <a href={`tel:${property.broker_phone}`} className="text-indigo-600 hover:underline">{property.broker_phone}</a>
                    </div>
                </div>
             </div>
        </div>
        )}
      </div>
    </div>
  );
};

export default PropertyDetail;
