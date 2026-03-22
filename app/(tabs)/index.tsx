import { useCallback, useMemo } from 'react';
import { ActivityIndicator, StyleSheet, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { CTAButton } from '@/components/dashboard/CTAButton';
import { DashboardHeader } from '@/components/dashboard/DashboardHeader';
import { QuickStats } from '@/components/dashboard/QuickStats';
import { SafeMapView, type MapMarkerData } from '@/components/map/SafeMapView';
import { SipatColors } from '@/constants/theme';
import { useLGUMapMarkers, usePromiseStats } from '@/hooks/api';
import { useLanguage } from '@/hooks/use-language';
import { useMapStore } from '@/store/map-store';

// Philippines center coordinates
const PH_REGION = {
  latitude: 12.8797,
  longitude: 121.774,
  latitudeDelta: 12,
  longitudeDelta: 8,
};

export default function DashboardScreen() {
  const { t } = useLanguage();
  const { setSelectedMarker } = useMapStore();

  // Fetch map markers and promise stats from the API (falls back to mock data)
  const { data: markers = [], isLoading: markersLoading } = useLGUMapMarkers();
  const { data: stats, isLoading: statsLoading } = usePromiseStats();

  const total = stats?.total ?? 0;

  const handleMarkerPress = useCallback(
    (id: number) => setSelectedMarker(id),
    [setSelectedMarker],
  );

  const handleMapPress = useCallback(
    () => setSelectedMarker(null),
    [setSelectedMarker],
  );

  // Transform LGU markers -> SafeMapView format (memoized)
  const mapMarkers: MapMarkerData[] = useMemo(
    () =>
      markers.map((m) => ({
        id: m.id,
        coordinate: { latitude: m.lat, longitude: m.lng },
        name: m.name,
        score: m.score,
        onPress: () => handleMarkerPress(m.id),
      })),
    [markers, handleMarkerPress],
  );

  const isInitialLoading = markersLoading && markers.length === 0;

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <DashboardHeader />

      <View style={styles.mapContainer}>
        {isInitialLoading ? (
          <View style={styles.loadingOverlay}>
            <ActivityIndicator size="large" color={SipatColors.gold} />
          </View>
        ) : null}
        <SafeMapView
          style={styles.map}
          initialRegion={PH_REGION}
          markers={mapMarkers}
          onPress={handleMapPress}
        />
      </View>

      <View style={styles.bottomPanel}>
        <CTAButton text={t.dashboard.cta} />

        {statsLoading && !stats ? (
          <View style={styles.statsLoading}>
            <ActivityIndicator size="small" color={SipatColors.gold} />
          </View>
        ) : stats ? (
          <QuickStats
            stats={[
              { label: t.dashboard.promisesKept, value: stats.counts.kept, total, color: SipatColors.kept },
              { label: t.dashboard.promisesBroken, value: stats.counts.broken, total, color: SipatColors.broken },
              { label: t.dashboard.promisesPending, value: stats.counts.pending, total, color: SipatColors.pending },
              { label: t.dashboard.promisesInProgress, value: stats.counts.in_progress, total, color: SipatColors.inProgress },
            ]}
          />
        ) : null}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: SipatColors.dashboardBg,
  },
  mapContainer: {
    flex: 1,
  },
  map: {
    flex: 1,
  },
  loadingOverlay: {
    ...StyleSheet.absoluteFillObject,
    zIndex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'rgba(255,255,255,0.6)',
  },
  bottomPanel: {
    backgroundColor: '#FFFFFF',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    paddingTop: 20,
    paddingBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: -2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 8,
  },
  statsLoading: {
    paddingVertical: 20,
    alignItems: 'center',
  },
});
