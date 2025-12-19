
import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="bg-white dark:bg-slate-900/70 shadow-md backdrop-blur-lg sticky top-0 z-50">
      <nav className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0">
                <svg className="w-8 h-8 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
            </div>
            <div className="ml-4">
              <h1 className="text-xl font-bold text-slate-800 dark:text-white">Zenith Estate</h1>
            </div>
          </div>
          <div className="flex items-center">
             <button className="hidden md:block bg-transparent text-slate-600 dark:text-slate-300 hover:text-indigo-500 dark:hover:text-indigo-400 font-medium py-2 px-4 rounded-md transition duration-150 ease-in-out">
                List a Property
              </button>
              <button className="ml-4 bg-indigo-500 hover:bg-indigo-600 text-white font-medium py-2 px-4 rounded-md shadow-sm transition duration-150 ease-in-out">
                Sign In
              </button>
          </div>
        </div>
      </nav>
    </header>
  );
};

export default Header;
