
import React from 'react';
import { Property } from '../types';
import PropertyCard from './PropertyCard';
import FilterSidebar from './FilterSidebar';

interface PropertyListProps {
  properties: Property[];
  onSelectProperty: (property: Property) => void;
}

const PropertyList: React.FC<PropertyListProps> = ({ properties, onSelectProperty }) => {
  return (
    <div className="flex flex-col md:flex-row gap-8">
      <aside className="w-full md:w-1/4 lg:w-1/5">
        <FilterSidebar />
      </aside>
      <div className="w-full md:w-3/4 lg:w-4/5">
         <h2 className="text-3xl font-bold text-slate-800 dark:text-white mb-6">Featured Properties</h2>
        {properties.length > 0 ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
            {properties.map((property) => (
              <PropertyCard key={property.id} property={property} onSelectProperty={onSelectProperty} />
            ))}
          </div>
        ) : (
          <p className="text-center text-slate-500">No properties found.</p>
        )}
      </div>
    </div>
  );
};

export default PropertyList;
