import BookingForm from "@/components/BookingForm";

export default function BookPage() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-black py-12 md:py-20 relative overflow-hidden">
      {/* Background Decor */}
      <div className="absolute top-0 left-0 w-full h-[300px] bg-primary/5 dark:bg-primary/10 rounded-b-[100px]" />
      
      <div className="container mx-auto px-4 md:px-6 relative z-10">
        <BookingForm />
      </div>
    </div>
  );
}
