"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle, ChevronRight, ChevronLeft, Calendar, User, FileText, Check } from "lucide-react";

export default function BookingForm() {
  const [step, setStep] = useState(1);
  const totalSteps = 4;

  const nextStep = () => setStep((p) => Math.min(p + 1, totalSteps));
  const prevStep = () => setStep((p) => Math.max(p - 1, 1));

  const steps = [
    { num: 1, title: "Patient Details", icon: User },
    { num: 2, title: "Consultation Type", icon: FileText },
    { num: 3, title: "Date & Time", icon: Calendar },
    { num: 4, title: "Confirmation", icon: CheckCircle },
  ];

  return (
    <div className="w-full max-w-3xl mx-auto bg-white dark:bg-zinc-900 rounded-3xl shadow-xl border border-gray-100 dark:border-zinc-800 overflow-hidden">
      {/* Progress Header */}
      <div className="bg-gray-50 dark:bg-zinc-800/50 p-6 md:p-8 border-b border-gray-100 dark:border-zinc-800">
        <h2 className="text-2xl font-bold mb-6 text-center">Book Your Appointment</h2>
        <div className="relative flex justify-between items-center">
          <div className="absolute left-0 top-1/2 -translate-y-1/2 w-full h-1 bg-gray-200 dark:bg-zinc-700 rounded-full" />
          <div
            className="absolute left-0 top-1/2 -translate-y-1/2 h-1 bg-primary rounded-full transition-all duration-500 ease-in-out"
            style={{ width: `${((step - 1) / (totalSteps - 1)) * 100}%` }}
          />
          {steps.map((s) => (
            <div key={s.num} className="relative z-10 flex flex-col items-center gap-2">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center transition-colors duration-300 shadow-sm ${
                  step >= s.num ? "bg-primary text-white" : "bg-white dark:bg-zinc-800 text-gray-400 border border-gray-200 dark:border-zinc-700"
                }`}
              >
                {step > s.num ? <Check className="w-5 h-5" /> : <s.icon className="w-5 h-5" />}
              </div>
              <span className={`text-xs font-semibold hidden md:block ${step >= s.num ? "text-primary" : "text-gray-400"}`}>
                {s.title}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Form Content */}
      <div className="p-6 md:p-10 min-h-[400px] flex flex-col">
        <AnimatePresence mode="wait">
          {step === 1 && (
            <motion.div key="step1" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="flex-1 space-y-6">
              <h3 className="text-xl font-semibold mb-4">Who is the patient?</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium mb-2">First Name</label>
                  <input type="text" className="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-zinc-700 bg-transparent focus:ring-2 focus:ring-primary outline-none transition-all" placeholder="John" />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Last Name</label>
                  <input type="text" className="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-zinc-700 bg-transparent focus:ring-2 focus:ring-primary outline-none transition-all" placeholder="Doe" />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Phone Number</label>
                  <input type="tel" className="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-zinc-700 bg-transparent focus:ring-2 focus:ring-primary outline-none transition-all" placeholder="+91 98765 43210" />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Email Address</label>
                  <input type="email" className="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-zinc-700 bg-transparent focus:ring-2 focus:ring-primary outline-none transition-all" placeholder="john@example.com" />
                </div>
              </div>
            </motion.div>
          )}

          {step === 2 && (
            <motion.div key="step2" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="flex-1 space-y-6">
              <h3 className="text-xl font-semibold mb-4">Choose Consultation Type</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {["In-Clinic Visit", "Video Consultation"].map((type) => (
                  <label key={type} className="flex items-center gap-4 p-4 rounded-xl border border-gray-200 dark:border-zinc-700 cursor-pointer hover:border-primary transition-colors">
                    <input type="radio" name="consultation" className="w-5 h-5 text-primary" />
                    <span className="font-medium">{type}</span>
                  </label>
                ))}
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Select Specialty</label>
                <select className="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-zinc-700 bg-transparent focus:ring-2 focus:ring-primary outline-none appearance-none">
                  <option>Cardiology</option>
                  <option>Neurology</option>
                  <option>Orthopedics</option>
                  <option>General Medicine</option>
                </select>
              </div>
            </motion.div>
          )}

          {step === 3 && (
            <motion.div key="step3" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="flex-1 space-y-6">
              <h3 className="text-xl font-semibold mb-4">Select Date & Time</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium mb-2">Preferred Date</label>
                  <input type="date" className="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-zinc-700 bg-transparent focus:ring-2 focus:ring-primary outline-none transition-all" />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Preferred Time Slot</label>
                  <div className="grid grid-cols-2 gap-2">
                    {["09:00 AM", "11:30 AM", "02:00 PM", "04:30 PM"].map((time) => (
                      <button key={time} className="py-2.5 rounded-lg border border-gray-200 dark:border-zinc-700 hover:border-primary hover:bg-primary/5 transition-colors font-medium text-sm">
                        {time}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {step === 4 && (
            <motion.div key="step4" initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="flex-1 flex flex-col items-center justify-center text-center space-y-4">
              <div className="w-20 h-20 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center text-green-500 mb-4">
                <CheckCircle className="w-10 h-10" />
              </div>
              <h3 className="text-2xl font-bold">Booking Confirmed!</h3>
              <p className="text-gray-600 dark:text-gray-400 max-w-sm">
                Your appointment has been successfully booked. A confirmation SMS and Email has been sent to you.
              </p>
              <div className="mt-8 p-6 bg-gray-50 dark:bg-zinc-800/50 rounded-2xl w-full max-w-sm text-left">
                <p className="text-sm text-gray-500 mb-1">Appointment Details</p>
                <p className="font-semibold mb-3">Cardiology - In-Clinic Visit</p>
                <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 mb-1">
                  <Calendar className="w-4 h-4" /> 24th October 2026, 11:30 AM
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                  <User className="w-4 h-4" /> John Doe
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Buttons */}
        <div className="mt-10 pt-6 border-t border-gray-100 dark:border-zinc-800 flex justify-between">
          {step > 1 && step < 4 ? (
            <button onClick={prevStep} className="px-6 py-2.5 rounded-xl font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-zinc-800 transition-colors flex items-center gap-2">
              <ChevronLeft className="w-4 h-4" /> Back
            </button>
          ) : <div />}

          {step < 4 && (
            <button onClick={nextStep} className="px-8 py-2.5 bg-primary text-white rounded-xl font-medium shadow-md hover:bg-primary-dark transition-colors flex items-center gap-2 ml-auto">
              {step === 3 ? "Confirm Booking" : "Next Step"} <ChevronRight className="w-4 h-4" />
            </button>
          )}

          {step === 4 && (
            <button onClick={() => setStep(1)} className="px-8 py-2.5 bg-primary text-white rounded-xl font-medium shadow-md hover:bg-primary-dark transition-colors mx-auto">
              Book Another
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
