"use client";

import { Search, MapPin } from "lucide-react";

export default function MapSection() {
  return (
    <section className="relative h-[500px] w-full bg-gray-100 dark:bg-zinc-900 border-t border-gray-200 dark:border-zinc-800">
      {/* Static Map Image / Placeholder */}
      <div 
        className="absolute inset-0 bg-cover bg-center opacity-80"
        style={{ backgroundImage: "url('https://images.unsplash.com/photo-1524661135-423995f22d0b?q=80&w=2074&auto=format&fit=crop')" }}
      />
      
      {/* Overlay Filter for aesthetics */}
      <div className="absolute inset-0 bg-blue-900/10 dark:bg-blue-950/40 mix-blend-multiply pointer-events-none" />

      {/* Floating Search Interface */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[90%] max-w-lg bg-white dark:bg-zinc-900 rounded-2xl shadow-2xl p-6 md:p-8 backdrop-blur-md">
        <div className="text-center mb-6">
          <div className="w-12 h-12 bg-primary/10 text-primary rounded-full flex items-center justify-center mx-auto mb-3">
            <MapPin className="w-6 h-6" />
          </div>
          <h3 className="text-2xl font-bold">Locate Nearest Hospital</h3>
          <p className="text-gray-500 dark:text-gray-400 text-sm mt-2">
            Find MediCare Plus facilities in your vicinity for quick assistance.
          </p>
        </div>

        <div className="relative">
          <input
            type="text"
            placeholder="Enter your city or zip code..."
            className="w-full px-5 py-4 pl-12 rounded-xl bg-gray-50 dark:bg-zinc-800 border border-gray-200 dark:border-zinc-700 outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all text-sm"
          />
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
        </div>
        
        <button className="w-full mt-4 py-4 bg-primary text-white font-medium rounded-xl hover:bg-primary-dark transition-colors shadow-lg shadow-primary/25">
          Search Locations
        </button>
      </div>
    </section>
  );
}
