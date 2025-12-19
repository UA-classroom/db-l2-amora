
import React, { useState, useEffect, useCallback } from 'react';
import { Property } from './types';
import { mockProperties } from './mockData';
import PropertyList from './components/PropertyList';
import PropertyDetail from './components/PropertyDetail';
import Header from './components/Header';
import { Spinner } from './components/Spinner';

const App: React.FC = () => {
  const [properties, setProperties] = useState<Property[]>([]);
  const [selectedProperty, setSelectedProperty] = useState<Property | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProperties = useCallback(() => {
    setIsLoading(true);
    setError(null);
    // Simulate API call
    setTimeout(() => {
      try {
        setProperties(mockProperties);
        setIsLoading(false);
      } catch (err) {
        setError('Failed to fetch properties.');
        setIsLoading(false);
      }
    }, 1000);
  }, []);

  useEffect(() => {
    fetchProperties();
  }, [fetchProperties]);

  const handleSelectProperty = (property: Property) => {
    setSelectedProperty(property);
    window.scrollTo(0, 0);
  };

  const handleBackToList = () => {
    setSelectedProperty(null);
  };

  const renderContent = () => {
    if (isLoading) {
      return (
        <div className="flex justify-center items-center h-[calc(100vh-200px)]">
          <Spinner />
        </div>
      );
    }

    if (error) {
      return <div className="text-center text-red-500 mt-10">{error}</div>;
    }

    if (selectedProperty) {
      return <PropertyDetail property={selectedProperty} onBack={handleBackToList} />;
    }

    return <PropertyList properties={properties} onSelectProperty={handleSelectProperty} />;
  };

  return (
    <div className="min-h-screen bg-slate-100 dark:bg-slate-900 text-slate-800 dark:text-slate-200 font-sans">
      <Header />
      <main className="container mx-auto px-4 py-8">
        {renderContent()}
      </main>
      <footer className="text-center py-6 border-t border-slate-200 dark:border-slate-800 text-slate-500">
        <p>&copy; {new Date().getFullYear()} Zenith Estate. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default App;
