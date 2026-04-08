"use client";

import { motion } from "framer-motion";
import { Video, Calendar, TestTube, Pill } from "lucide-react";
import { services } from "@/lib/data";

const iconMap: Record<string, React.ReactNode> = {
  Video: <Video className="w-8 h-8" />,
  Calendar: <Calendar className="w-8 h-8" />,
  TestTube: <TestTube className="w-8 h-8" />,
  Pill: <Pill className="w-8 h-8" />,
};

export default function ServicesGrid() {
  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    show: { opacity: 1, y: 0, transition: { type: "spring" as const, stiffness: 100 } },
  };

  return (
    <section className="py-20 bg-gray-50 dark:bg-black">
      <div className="container mx-auto px-4 md:px-6">
        <div className="text-center mb-16 max-w-2xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Our Premium Services</h2>
          <p className="text-gray-600 dark:text-gray-400">
            Comprehensive care tailored to your needs. From online consultations to doorstep pharmacy delivery, we have got you covered.
          </p>
        </div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, margin: "-100px" }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
        >
          {services.map((service) => (
            <motion.div
              key={service.id}
              variants={itemVariants}
              whileHover={{ y: -8 }}
              className="bg-white dark:bg-zinc-900 p-8 rounded-2xl shadow-sm hover:shadow-xl dark:shadow-none border border-gray-100 dark:border-zinc-800 transition-all text-center group cursor-pointer"
            >
              <div className="w-16 h-16 mx-auto bg-blue-50 dark:bg-primary/10 text-primary rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform group-hover:bg-primary group-hover:text-white">
                {iconMap[service.icon]}
              </div>
              <h3 className="text-xl font-bold mb-3">{service.title}</h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed">
                {service.description}
              </p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
