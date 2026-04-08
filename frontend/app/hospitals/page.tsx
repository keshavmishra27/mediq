import { hospitals } from "@/lib/data";
import { Search, MapPin, Phone, Clock } from "lucide-react";
import Image from "next/image";

export default function HospitalsPage() {
  return (
    <div className="min-h-screen flex flex-col md:flex-row bg-white dark:bg-black">
      {/* Sidebar ListView */}
      <div className="w-full md:w-[450px] lg:w-[500px] border-r border-gray-200 dark:border-zinc-800 flex flex-col h-[calc(100vh-88px)] bg-gray-50 dark:bg-zinc-950">
        <div className="p-6 border-b border-gray-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 sticky top-0 z-10">
          <h1 className="text-2xl font-bold mb-4">Our Hospitals</h1>
          <div className="relative">
            <input
              type="text"
              placeholder="Search by city or facility name..."
              className="w-full px-4 py-3 pl-11 rounded-xl bg-gray-100 dark:bg-zinc-800 border-none outline-none focus:ring-2 focus:ring-primary transition-shadow"
            />
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {hospitals.map((hospital) => (
            <div
              key={hospital.id}
              className="bg-white dark:bg-zinc-900 rounded-xl p-5 shadow-sm border border-gray-100 dark:border-zinc-800 hover:border-primary cursor-pointer transition-colors"
            >
              <h3 className="font-bold text-lg mb-2 text-gray-900 dark:text-white">
                {hospital.name}
              </h3>
              <div className="space-y-2 text-sm text-gray-600 dark:text-gray-400 mb-4">
                <p className="flex items-center gap-2">
                  <MapPin className="w-4 h-4 text-primary" />
                  {hospital.lat.toFixed(2)}, {hospital.lng.toFixed(2)} (Coordinates)
                </p>
                <p className="flex items-center gap-2">
                  <Clock className="w-4 h-4 text-primary" />
                  Open 24/7
                </p>
                <p className="flex items-center gap-2">
                  <Phone className="w-4 h-4 text-primary" />
                  +91 {Math.floor(Math.random() * 9000000000) + 1000000000}
                </p>
              </div>
              <div className="flex flex-wrap gap-2">
                {hospital.services.map((service, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-1 bg-blue-50 dark:bg-blue-900/20 text-primary text-xs font-semibold rounded"
                  >
                    {service}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Map View Placeholder */}
      <div className="flex-1 relative h-[50vh] md:h-[calc(100vh-88px)] bg-gray-200 dark:bg-zinc-900">
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{ backgroundImage: "url('https://images.unsplash.com/photo-1524661135-423995f22d0b?q=80&w=2074&auto=format&fit=crop')" }}
        />
        <div className="absolute inset-0 bg-white/20 dark:bg-black/40 backdrop-blur-[2px]" />
        
        {/* Simulate Map Pins */}
        <div className="absolute inset-0 max-w-4xl mx-auto h-full flex items-center justify-center p-8">
            <div className="bg-white/90 dark:bg-black/90 p-6 rounded-2xl shadow-2xl backdrop-blur-md max-w-sm text-center">
              <div className="w-16 h-16 bg-primary/20 text-primary rounded-full flex items-center justify-center mx-auto mb-4 animate-bounce">
                <MapPin className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-bold mb-2">Interactive Map Unavailable</h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                This is a high-fidelity frontend prototype. A real API/Maps SDK integration would render interactive markers here.
              </p>
            </div>
        </div>
      </div>
    </div>
  );
}
