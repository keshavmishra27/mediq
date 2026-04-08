import HeroSlider from "@/components/HeroSlider";
import ServicesGrid from "@/components/ServicesGrid";
import Testimonials from "@/components/Testimonials";
import MapSection from "@/components/MapSection";

export default function Home() {
  return (
    <>
      <HeroSlider />
      <ServicesGrid />
      <Testimonials />
      <MapSection />
    </>
  );
}
