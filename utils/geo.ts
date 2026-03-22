// Philippines geographic constants and utilities

/** Philippines center coordinates */
export const PH_CENTER = {
  latitude: 12.8797,
  longitude: 121.774,
} as const;

/** Default zoom level for Philippines overview */
export const PH_ZOOM = 5;

/** Manila coordinates (default fallback) */
export const MANILA_CENTER = {
  latitude: 14.5995,
  longitude: 120.9842,
} as const;

/**
 * Calculate distance between two coordinates in kilometers (Haversine formula).
 */
export function distanceKm(
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number,
): number {
  const R = 6371;
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

function toRad(deg: number): number {
  return deg * (Math.PI / 180);
}

/**
 * Check if coordinates are within Philippine boundaries (rough bounding box).
 */
export function isWithinPhilippines(lat: number, lng: number): boolean {
  return lat >= 4.5 && lat <= 21.5 && lng >= 116.0 && lng <= 127.0;
}
