/**
 * ClearAir AI — Action Catalog
 * Science-backed indoor air hacks, daily routines, and community mitigations
 * with deterministic emission coefficients and physical aerosol mechanisms.
 */

export const ACTION_CATALOG = [
  // --- DAILY ROUTINES ---
  {
    id: "act_veh_recirc",
    title: "Vehicle Cabin HVAC Recirculation Lock",
    category: "Daily Routines",
    type: "routine",
    defaultSelected: true,
    impactTag: "-70% Cabin Particulates",
    bestFit: ["Personal Car"],
    pm25Reduction: 12,
    toxinsAvoidedGrams: 45,
    co2SavedKg: 0.5,
    whyItWorks: "Prevents drawing direct raw tailpipe PM2.5 and NOx from leading diesel trucks; standard cabin filters drop cabin PM by 70% in recirc mode."
  },
  {
    id: "act_zero_idling",
    title: "School Gate & Driveway Zero-Idling",
    category: "Daily Routines",
    type: "routine",
    defaultSelected: false,
    impactTag: "-90% Local NOx Spikes",
    bestFit: ["Kids", "Personal Car"],
    pm25Reduction: 8,
    toxinsAvoidedGrams: 35,
    co2SavedKg: 1.8,
    whyItWorks: "Idling produces twice the emissions of a moving vehicle; young children inhale 50% more air per pound of body weight at car exhaust height."
  },
  {
    id: "act_mixing_errands",
    title: "Afternoon Mixing-Window Errand Shifting",
    category: "Daily Routines",
    type: "routine",
    defaultSelected: true,
    impactTag: "-35% Commute Inhalation",
    bestFit: ["Asthma/Resp.", "Elderly"],
    pm25Reduction: 14,
    toxinsAvoidedGrams: 20,
    co2SavedKg: 0.2,
    whyItWorks: "Planetary boundary layer expands from 150m at dawn to over 1,200m at midday, diluting surface pollutant concentration by up to 60%."
  },
  {
    id: "act_transit_swap",
    title: "Metro / Transit Swap with N95 Seal",
    category: "Daily Routines",
    type: "routine",
    defaultSelected: false,
    impactTag: "-85% Tailpipe Emissions",
    bestFit: ["Personal Car", "2-Wheeler / Walk"],
    pm25Reduction: 16,
    toxinsAvoidedGrams: 80,
    co2SavedKg: 3.2,
    whyItWorks: "Removes ~4.2 kg CO2 and 90g NOx per trip compared to solo ICE vehicles, while certified N95 stops 95% of fine sub-micron soot."
  },

  // --- INDOOR AIR HACKS ---
  {
    id: "act_weatherstrip",
    title: "High-Density Window Frame Weatherstrip Bar",
    category: "Indoor Air Hacks",
    type: "indoor",
    defaultSelected: true,
    impactTag: "-28% Infiltration Rate",
    bestFit: ["Apartment", "House / Villa"],
    pm25Reduction: 18,
    toxinsAvoidedGrams: 60,
    co2SavedKg: 0.8,
    whyItWorks: "Stops micro-draft leaks where 70% of external particulate mass penetrates residential apartment window frame tolerances."
  },
  {
    id: "act_corsi_rosenthal",
    title: "DIY Corsi-Rosenthal MERV-13 Box Fan",
    category: "Indoor Air Hacks",
    type: "indoor",
    defaultSelected: false,
    impactTag: "-80% Indoor PM2.5 (450 CFM)",
    bestFit: ["Kids", "Asthma/Resp."],
    pm25Reduction: 26,
    toxinsAvoidedGrams: 110,
    co2SavedKg: 0.4,
    whyItWorks: "Quad-filter geometry delivers 450 CFM Clean Air Delivery Rate (CADR) with very low static pressure resistance at 1/5th cost of commercial units."
  },
  {
    id: "act_vented_exhaust",
    title: "Kitchen Negative Pressure Exhaust Isolation",
    category: "Indoor Air Hacks",
    type: "indoor",
    defaultSelected: false,
    impactTag: "-75% Cooking NOx & UFP",
    bestFit: ["LPG/Gas"],
    pm25Reduction: 15,
    toxinsAvoidedGrams: 50,
    co2SavedKg: 0.1,
    whyItWorks: "LPG burner combustion generates up to 100 ppb NOx and ultrafine droplets; venting exterior doors prevents chamber dispersion to bedrooms."
  },
  {
    id: "act_wet_mop",
    title: "Electrostatic Microfiber Damp-Mop Protocol",
    category: "Indoor Air Hacks",
    type: "indoor",
    defaultSelected: false,
    impactTag: "-40% Settled Dust Resuspension",
    bestFit: ["Kids", "Elderly"],
    pm25Reduction: 10,
    toxinsAvoidedGrams: 25,
    co2SavedKg: 0.0,
    whyItWorks: "Dry sweeping aerosolizes settled heavy particulate matter into infant breathing zones; damp microfibers trap electrostatic soot permanently."
  },

  // --- COMMUNITY ACTION ---
  {
    id: "act_carpool_circle",
    title: "3-Family School Carpool Pod",
    category: "Community Action",
    type: "community",
    defaultSelected: false,
    impactTag: "-66% School Run Emissions",
    bestFit: ["Kids", "Personal Car"],
    pm25Reduction: 11,
    toxinsAvoidedGrams: 95,
    co2SavedKg: 4.8,
    whyItWorks: "Consolidates three round-trips into one cold-start trip, preventing 380g of NOx per week right in neighborhood school zones."
  },
  {
    id: "act_zero_burn_pledge",
    title: "Apartment Gate Zero-Idling & Leaf Composting Pact",
    category: "Community Action",
    type: "community",
    defaultSelected: true,
    impactTag: "-90% Ground Smoke Plumes",
    bestFit: ["Apartment", "House / Villa"],
    pm25Reduction: 15,
    toxinsAvoidedGrams: 140,
    co2SavedKg: 2.1,
    whyItWorks: "Eliminates smoldering leaf waste fires that release acrolein, dioxins, and concentrated carbon black under nightly thermal inversions."
  },
  {
    id: "act_induction_share",
    title: "Community Induction Cooktop Rental Bank",
    category: "Community Action",
    type: "community",
    defaultSelected: false,
    impactTag: "-100% Indoor Combustion",
    bestFit: ["Biomass", "LPG/Gas"],
    pm25Reduction: 22,
    toxinsAvoidedGrams: 85,
    co2SavedKg: 1.6,
    whyItWorks: "Replaces unvented fossil gas and biomass burner cycles with magnetic induction, cutting household PM2.5 spikes by up to 88%."
  },
  {
    id: "act_barrier_greenery",
    title: "Dense Balcony PM-Trapping Foliage Barrier",
    category: "Community Action",
    type: "community",
    defaultSelected: false,
    impactTag: "-18% Particulate Infiltration",
    bestFit: ["Apartment"],
    pm25Reduction: 7,
    toxinsAvoidedGrams: 30,
    co2SavedKg: 0.3,
    whyItWorks: "Coniferous and hairy leaf structures act as electrostatic micro-sieves that adsorb airborne soot particles before entering vents."
  }
];
