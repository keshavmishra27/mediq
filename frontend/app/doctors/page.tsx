import DoctorCard from "@/components/DoctorCard";
import { doctors } from "@/lib/data";

export default function DoctorsPage() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-black py-12 md:py-20">
      <div className="container mx-auto px-4 md:px-6">
        <div className="max-w-3xl mb-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-4 text-gray-900 dark:text-white">Our Specialists</h1>
          <p className="text-lg text-gray-600 dark:text-gray-400">
            Find and book appointments with top-rated doctors across various specialties.
          </p>
        </div>

        {/* Filters/Search placeholder */}
        <div className="bg-white dark:bg-zinc-900 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-zinc-800 mb-8 flex flex-col md:flex-row gap-4">
          <input 
            type="text" 
            placeholder="Search doctors by name or specialty..." 
            className="flex-1 px-4 py-3 rounded-lg bg-gray-50 dark:bg-zinc-800 border-none outline-none focus:ring-2 focus:ring-primary transition-shadow"
          />
          <select className="px-4 py-3 rounded-lg bg-gray-50 dark:bg-zinc-800 border-none outline-none focus:ring-2 focus:ring-primary min-w-[200px]">
            <option>All Cities</option>
            <option>Delhi</option>
            <option>Mumbai</option>
            <option>Bangalore</option>
          </select>
          <button className="px-6 py-3 bg-primary text-white rounded-lg font-medium hover:bg-primary-dark transition-colors">
            Search
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {doctors.map((doctor) => (
            <DoctorCard key={doctor.id} doctor={doctor} />
          ))}
        </div>
      </div>
    </div>
  );
}
