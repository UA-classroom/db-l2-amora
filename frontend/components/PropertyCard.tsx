
import React from 'react';
import { Property } from '../types';
import { BedIcon, BathIcon, SizeIcon, LocationIcon } from './Icons';

interface PropertyCardProps {
  property: Property;
  onSelectProperty: (property: Property) => void;
}

const PropertyCard: React.FC<PropertyCardProps> = ({ property, onSelectProperty }) => {
  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price);
  };

  return (
    <div 
      className="bg-white dark:bg-slate-800 rounded-xl shadow-lg hover:shadow-2xl transition-shadow duration-300 ease-in-out overflow-hidden cursor-pointer flex flex-col group"
      onClick={() => onSelectProperty(property)}
    >
      <div className="relative">
        <img 
          src={`https://picsum.photos/seed/${property.id}/400/300`} 
          alt={property.title}
          className="w-full h-56 object-cover group-hover:scale-105 transition-transform duration-300" 
        />
        <div className="absolute top-4 left-4 bg-indigo-500 text-white text-xs font-bold px-3 py-1 rounded-full">
          {property.listing_type}
        </div>
         <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-4">
           <h3 className="text-white text-lg font-bold truncate">{property.title}</h3>
         </div>
      </div>
      <div className="p-5 flex-grow flex flex-col">
        <div className="flex items-center text-slate-500 dark:text-slate-400 text-sm mb-3">
          <LocationIcon className="w-4 h-4 mr-2 text-slate-400" />
          <span>{property.address}, {property.city}</span>
        </div>

        <div className="grid grid-cols-3 gap-4 text-center my-4 border-y dark:border-slate-700 py-3">
            <div className="flex flex-col items-center">
                <BedIcon className="w-5 h-5 mb-1 text-indigo-400"/>
                <span className="text-sm font-medium text-slate-700 dark:text-slate-300">{property.rooms} Beds</span>
            </div>
            <div className="flex flex-col items-center">
                <BathIcon className="w-5 h-5 mb-1 text-indigo-400"/>
                <span className="text-sm font-medium text-slate-700 dark:text-slate-300">{property.bathrooms} Baths</span>
            </div>
            <div className="flex flex-col items-center">
                <SizeIcon className="w-5 h-5 mb-1 text-indigo-400"/>
                <span className="text-sm font-medium text-slate-700 dark:text-slate-300">{property.size_sqm} m²</span>
            </div>
        </div>
        
        <div className="mt-auto flex justify-between items-center">
          <p className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">
            {formatPrice(property.start_price)}
            {property.listing_type === 'For Rent' && <span className="text-sm font-normal text-slate-500 dark:text-slate-400">/month</span>}
          </p>
          <button className="text-sm font-semibold text-indigo-600 dark:text-indigo-400 hover:text-indigo-500 dark:hover:text-indigo-300">
            View Details &rarr;
          </button>
        </div>
      </div>
    </div>
  );
};

export default PropertyCard;
