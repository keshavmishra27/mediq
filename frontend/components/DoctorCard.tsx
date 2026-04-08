"use client";

import { motion } from "framer-motion";
import { Star, MapPin, Clock, Award } from "lucide-react";
import Link from "next/link";
import Image from "next/image";

interface DoctorProps {
  doctor: {
    id: number;
    name: string;
    specialty: string;
    rating: number;
    city: string;
    experience: string;
    avatar?: string;
  };
}

export default function DoctorCard({ doctor }: DoctorProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      whileHover={{ y: -5 }}
      transition={{ duration: 0.3 }}
      className="bg-white dark:bg-zinc-900 rounded-2xl p-6 shadow-sm hover:shadow-xl dark:shadow-none border border-gray-100 dark:border-zinc-800 transition-all group"
    >
      <div className="flex items-start gap-4 mb-4">
        <div className="relative w-20 h-20 rounded-full overflow-hidden bg-gray-100 dark:bg-zinc-800 shrink-0 border-2 border-transparent group-hover:border-primary transition-colors">
          {doctor.avatar ? (
            <div className="w-full h-full bg-gradient-to-br from-blue-100 to-primary/20 flex items-center justify-center text-primary font-bold text-2xl">
              {doctor.name.split(" ")[1][0]}
            </div>
          ) : null}
        </div>
        <div className="flex-1">
          <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-1 group-hover:text-primary transition-colors">
            {doctor.name}
          </h3>
          <p className="text-primary font-medium text-sm mb-2">{doctor.specialty}</p>
          <div className="flex items-center gap-1 bg-green-50 dark:bg-green-900/30 text-green-600 dark:text-green-400 w-fit px-2 py-0.5 rounded text-xs font-semibold">
            <Star className="w-3 h-3 fill-current" />
            <span>{doctor.rating}</span>
          </div>
        </div>
      </div>

      <div className="space-y-2 mb-6 text-sm text-gray-600 dark:text-gray-400">
        <div className="flex items-center gap-2">
          <Award className="w-4 h-4 text-gray-400 dark:text-gray-500" />
          <span>{doctor.experience} Experience</span>
        </div>
        <div className="flex items-center gap-2">
          <MapPin className="w-4 h-4 text-gray-400 dark:text-gray-500" />
          <span>{doctor.city}</span>
        </div>
        <div className="flex items-center gap-2">
          <Clock className="w-4 h-4 text-gray-400 dark:text-gray-500" />
          <span>Available Today</span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 mt-auto">
        <Link
          href={`/doctors/${doctor.id}`}
          className="text-center py-2.5 rounded-lg border border-primary text-primary font-medium hover:bg-primary/5 transition-colors text-sm"
        >
          View Profile
        </Link>
        <Link
          href={`/book?doctor=${doctor.id}`}
          className="text-center py-2.5 rounded-lg bg-primary text-white font-medium hover:bg-primary-dark shadow-sm transition-colors text-sm"
        >
          Book Now
        </Link>
      </div>
    </motion.div>
  );
}
