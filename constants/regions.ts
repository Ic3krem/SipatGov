// Philippine regions from PSGC (Philippine Standard Geographic Code)
// Static data for offline onboarding region picker

export interface RegionData {
  id: number;
  code: string;
  name: string;
}

export const PHILIPPINE_REGIONS: RegionData[] = [
  { id: 1, code: 'NCR', name: 'National Capital Region (NCR)' },
  { id: 2, code: 'CAR', name: 'Cordillera Administrative Region (CAR)' },
  { id: 3, code: 'I', name: 'Region I - Ilocos Region' },
  { id: 4, code: 'II', name: 'Region II - Cagayan Valley' },
  { id: 5, code: 'III', name: 'Region III - Central Luzon' },
  { id: 6, code: 'IV-A', name: 'Region IV-A - CALABARZON' },
  { id: 7, code: 'IV-B', name: 'Region IV-B - MIMAROPA' },
  { id: 8, code: 'V', name: 'Region V - Bicol Region' },
  { id: 9, code: 'VI', name: 'Region VI - Western Visayas' },
  { id: 10, code: 'VII', name: 'Region VII - Central Visayas' },
  { id: 11, code: 'VIII', name: 'Region VIII - Eastern Visayas' },
  { id: 12, code: 'IX', name: 'Region IX - Zamboanga Peninsula' },
  { id: 13, code: 'X', name: 'Region X - Northern Mindanao' },
  { id: 14, code: 'XI', name: 'Region XI - Davao Region' },
  { id: 15, code: 'XII', name: 'Region XII - SOCCSKSARGEN' },
  { id: 16, code: 'XIII', name: 'Region XIII - Caraga' },
  { id: 17, code: 'BARMM', name: 'Bangsamoro Autonomous Region in Muslim Mindanao (BARMM)' },
];
