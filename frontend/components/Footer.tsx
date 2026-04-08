import Link from "next/link";
import { HeartPulse, X, MessageCircle, Camera, Users, Search, MapPin, Phone, Mail } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-gray-50 dark:bg-zinc-900 border-t border-gray-200 dark:border-zinc-800 pt-16 pb-8">
      <div className="container mx-auto px-4 md:px-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-12">
          {/* Brand Info */}
          <div className="space-y-4">
            <Link href="/" className="flex items-center gap-2">
              <HeartPulse className="w-8 h-8 text-primary" />
              <span className="text-xl font-bold tracking-tight">
                MediCare <span className="text-primary">Plus</span>
              </span>
            </Link>
            <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">
              Providing world-class healthcare services with compassion, expertise, and advanced technology. Your health is our priority.
            </p>
            <div className="flex gap-4 pt-2">
              <a href="#" className="p-2 bg-white dark:bg-zinc-800 rounded-full text-gray-500 hover:text-primary shadow-sm transition-colors"><X className="w-4 h-4" /></a>
              <a href="#" className="p-2 bg-white dark:bg-zinc-800 rounded-full text-gray-500 hover:text-primary shadow-sm transition-colors"><MessageCircle className="w-4 h-4" /></a>
              <a href="#" className="p-2 bg-white dark:bg-zinc-900 rounded-full text-gray-500 hover:text-primary shadow-sm transition-colors"><Camera className="w-4 h-4" /></a>
              <a href="#" className="p-2 bg-white dark:bg-zinc-900 rounded-full text-gray-500 hover:text-primary shadow-sm transition-colors"><Users className="w-4 h-4" /></a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-semibold text-lg mb-6">Quick Links</h3>
            <ul className="space-y-3">
              {['About Us', 'Find a Doctor', 'Our Hospitals', 'Book Appointment', 'Specialties', 'Contact Us'].map((link) => (
                <li key={link}>
                  <Link href="#" className="text-gray-600 dark:text-gray-400 hover:text-primary text-sm flex items-center gap-2 group">
                    <span className="w-1.5 h-1.5 rounded-full bg-gray-300 dark:bg-zinc-700 group-hover:bg-primary transition-colors" />
                    {link}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Services */}
          <div>
            <h3 className="font-semibold text-lg mb-6">Our Services</h3>
            <ul className="space-y-3">
              {['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', '24/7 Emergency', 'Lab Tests'].map((link) => (
                <li key={link}>
                  <Link href="#" className="text-gray-600 dark:text-gray-400 hover:text-primary text-sm flex items-center gap-2 group">
                    <span className="w-1.5 h-1.5 rounded-full bg-gray-300 dark:bg-zinc-700 group-hover:bg-primary transition-colors" />
                    {link}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="font-semibold text-lg mb-6">Contact Info</h3>
            <ul className="space-y-4">
              <li className="flex gap-3 text-sm text-gray-600 dark:text-gray-400">
                <MapPin className="w-5 h-5 text-primary shrink-0" />
                <span>123 Health Avenue, Medical District, ND 110001, India</span>
              </li>
              <li className="flex gap-3 text-sm text-gray-600 dark:text-gray-400">
                <Phone className="w-5 h-5 text-primary shrink-0" />
                <span>1800-123-4567<br/>+91 98765 43210</span>
              </li>
              <li className="flex gap-3 text-sm text-gray-600 dark:text-gray-400">
                <Mail className="w-5 h-5 text-primary shrink-0" />
                <span>support@medicareplus.com</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-200 dark:border-zinc-800 pt-8 mt-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-gray-500 dark:text-gray-500">
            &copy; {new Date().getFullYear()} MediCare Plus. All rights reserved.
          </p>
          <div className="flex gap-6 text-sm text-gray-500 dark:text-gray-500">
            <Link href="#" className="hover:text-primary">Privacy Policy</Link>
            <Link href="#" className="hover:text-primary">Terms of Service</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
