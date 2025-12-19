
import React from 'react';

const FilterSidebar: React.FC = () => {
  return (
    <div className="bg-white dark:bg-slate-800 p-6 rounded-xl shadow-lg h-full">
      <h3 className="text-xl font-bold mb-6 text-slate-800 dark:text-white">Filter Properties</h3>
      <form>
        <div className="mb-6">
          <label htmlFor="listing-type" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Listing Type</label>
          <select id="listing-type" name="listing-type" className="w-full bg-slate-100 dark:bg-slate-700 border-slate-200 dark:border-slate-600 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500">
            <option>For Sale</option>
            <option>For Rent</option>
          </select>
        </div>
        <div className="mb-6">
          <label htmlFor="property-type" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Property Type</label>
          <select id="property-type" name="property-type" className="w-full bg-slate-100 dark:bg-slate-700 border-slate-200 dark:border-slate-600 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500">
            <option>Any</option>
            <option>Apartment</option>
            <option>House</option>
            <option>Villa</option>
            <option>Loft</option>
          </select>
        </div>
        <div className="mb-6">
          <label htmlFor="price-range" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Price Range</label>
          <input type="range" id="price-range" name="price-range" min="50000" max="2000000" step="10000" className="w-full h-2 bg-slate-200 dark:bg-slate-600 rounded-lg appearance-none cursor-pointer" />
           <div className="flex justify-between text-xs text-slate-500 dark:text-slate-400 mt-1">
            <span>$50k</span>
            <span>$2M+</span>
          </div>
        </div>
         <div className="mb-6">
          <label htmlFor="beds" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Bedrooms</label>
          <select id="beds" name="beds" className="w-full bg-slate-100 dark:bg-slate-700 border-slate-200 dark:border-slate-600 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500">
            <option>1+</option>
            <option>2+</option>
            <option>3+</option>
            <option>4+</option>
          </select>
        </div>
        <div className="mb-6">
          <label htmlFor="baths" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Bathrooms</label>
          <select id="baths" name="baths" className="w-full bg-slate-100 dark:bg-slate-700 border-slate-200 dark:border-slate-600 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500">
            <option>1+</option>
            <option>2+</option>
            <option>3+</option>
          </select>
        </div>
        <div>
          <button type="submit" className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-4 rounded-lg transition duration-300">
            Apply Filters
          </button>
        </div>
      </form>
    </div>
  );
};

export default FilterSidebar;
