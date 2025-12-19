
import React from 'react';

export const Spinner: React.FC = () => {
  return (
    <div className="flex items-center justify-center space-x-2">
      <div className="w-4 h-4 rounded-full animate-pulse bg-indigo-500"></div>
      <div className="w-4 h-4 rounded-full animate-pulse bg-indigo-500" style={{ animationDelay: '0.2s' }}></div>
      <div className="w-4 h-4 rounded-full animate-pulse bg-indigo-500" style={{ animationDelay: '0.4s' }}></div>
    </div>
  );
};
