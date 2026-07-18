import SiteNavbar from "../components/nav/SiteNavbar";
import LandingHero from "../components/landing/LandingHero";
import LandingRule from "../components/landing/LandingRule";
import LandingCompare from "../components/landing/LandingCompare";
import LandingLoop from "../components/landing/LandingLoop";
import LandingDarkFeatures from "../components/landing/LandingDarkFeatures";
import LandingAudience from "../components/landing/LandingAudience";
import LandingProof from "../components/landing/LandingProof";
import LandingResults from "../components/landing/LandingResults";
import LandingCta from "../components/landing/LandingCta";
import LandingFooter from "../components/landing/LandingFooter";

export default function LandingPage() {
  return (
    <div className="lp-page">
      <SiteNavbar variant="landing" />
      <LandingHero />
      <LandingRule />
      <LandingCompare />
      <LandingLoop />
      <LandingDarkFeatures />
      <LandingAudience />
      <LandingProof />
      <LandingResults />
      <LandingCta />
      <LandingFooter />
    </div>
  );
}
