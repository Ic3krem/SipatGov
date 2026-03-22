/**
 * SafeMapView — Interactive map using OpenLayers + OpenStreetMap tiles.
 *
 * Renders inside a WebView. If the native WebView module isn't available
 * (hasn't been compiled into the APK yet), falls back to a branded
 * placeholder grid. No Google Maps API key required.
 */

import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { SipatColors } from '@/constants/theme';

/* ─── Types ────────────────────────────────────────────── */

export interface MapMarkerData {
  id: string | number;
  coordinate: { latitude: number; longitude: number };
  name?: string;
  score?: number;
  onPress?: () => void;
  children?: React.ReactNode;
}

interface SafeMapViewProps {
  style?: any;
  initialRegion?: {
    latitude: number;
    longitude: number;
    latitudeDelta: number;
    longitudeDelta: number;
  };
  markers?: MapMarkerData[];
  onPress?: () => void;
}

/* ─── Lazy-load WebView ────────────────────────────────── */

let WebViewComponent: any = null;
let webViewAvailable = false;

try {
  WebViewComponent = require('react-native-webview').WebView;
  webViewAvailable = true;
} catch {
  webViewAvailable = false;
}

/* ─── Score color helper ───────────────────────────────── */

function getScoreHex(score?: number): string {
  if (score == null) return SipatColors.gold;
  if (score >= 75) return SipatColors.kept;
  if (score >= 50) return SipatColors.gold;
  return SipatColors.red;
}

/* ─── OpenLayers HTML Template ─────────────────────────── */

function buildMapHTML(
  center: [number, number],
  zoom: number,
  markers: MapMarkerData[],
): string {
  const markersJSON = JSON.stringify(
    markers.map((m) => ({
      id: m.id,
      lon: m.coordinate.longitude,
      lat: m.coordinate.latitude,
      name: m.name ?? '',
      score: m.score ?? 0,
      color: getScoreHex(m.score),
    })),
  );

  return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/ol@10.5.0/ol.css" />
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body, #map { width: 100%; height: 100%; }
    .marker {
      width: 32px; height: 32px; border-radius: 50%;
      border: 2px solid #fff;
      display: flex; align-items: center; justify-content: center;
      font-size: 10px; font-weight: 800; color: #fff;
      cursor: pointer;
      box-shadow: 0 2px 6px rgba(0,0,0,0.3);
      transition: transform 0.15s ease;
    }
    .marker:hover, .marker.selected {
      transform: scale(1.25);
      border-color: ${SipatColors.gold};
    }
    .popup {
      position: absolute; bottom: 44px; left: 50%;
      transform: translateX(-50%);
      background: ${SipatColors.navy};
      color: #fff; font-size: 11px; font-weight: 600;
      padding: 4px 10px; border-radius: 6px;
      white-space: nowrap; pointer-events: none;
      opacity: 0; transition: opacity 0.15s;
    }
    .marker.selected .popup { opacity: 1; }
    .popup::after {
      content: ''; position: absolute;
      top: 100%; left: 50%; transform: translateX(-50%);
      border: 5px solid transparent;
      border-top-color: ${SipatColors.navy};
    }
    .ol-attribution { font-size: 10px; }
  </style>
</head>
<body>
  <div id="map"></div>
  <script src="https://cdn.jsdelivr.net/npm/ol@10.5.0/dist/ol.js"><\/script>
  <script>
    const markers = ${markersJSON};
    let selectedId = null;
    const map = new ol.Map({
      target: 'map',
      layers: [new ol.layer.Tile({ source: new ol.source.OSM() })],
      view: new ol.View({
        center: ol.proj.fromLonLat([${center[0]}, ${center[1]}]),
        zoom: ${zoom}, minZoom: 5, maxZoom: 18
      }),
      controls: ol.control.defaults.defaults({ attribution: true, zoom: true, rotate: false })
    });
    markers.forEach(m => {
      const el = document.createElement('div');
      el.className = 'marker';
      el.id = 'marker-' + m.id;
      el.style.backgroundColor = m.color;
      el.innerHTML = '<span>' + Math.round(m.score) + '</span><div class="popup">' + m.name + '</div>';
      el.addEventListener('click', (e) => {
        e.stopPropagation();
        if (selectedId) {
          const prev = document.getElementById('marker-' + selectedId);
          if (prev) prev.classList.remove('selected');
        }
        selectedId = m.id;
        el.classList.add('selected');
        window.ReactNativeWebView.postMessage(JSON.stringify({ type: 'marker_press', id: m.id }));
      });
      map.addOverlay(new ol.Overlay({
        element: el,
        position: ol.proj.fromLonLat([m.lon, m.lat]),
        positioning: 'bottom-center',
        offset: [0, -4], stopEvent: false
      }));
    });
    map.on('click', () => {
      if (selectedId) {
        const prev = document.getElementById('marker-' + selectedId);
        if (prev) prev.classList.remove('selected');
        selectedId = null;
        window.ReactNativeWebView.postMessage(JSON.stringify({ type: 'map_press' }));
      }
    });
  <\/script>
</body>
</html>`;
}

/* ─── Fallback (when WebView not available) ────────────── */

function MapFallback({ markers, onPress }: SafeMapViewProps) {
  return (
    <View style={styles.fallback}>
      <View style={styles.headerSection}>
        <Text style={styles.phEmoji}>🇵🇭</Text>
        <Text style={styles.fallbackTitle}>Interactive Map</Text>
        <Text style={styles.fallbackSub}>
          {markers?.length ?? 0} LGU markers ready
        </Text>
        <View style={styles.badge}>
          <MaterialIcons name="info-outline" size={14} color={SipatColors.navyLight} />
          <Text style={styles.badgeText}>
            Rebuild APK for interactive map: npx expo run:android
          </Text>
        </View>
      </View>

      {markers && markers.length > 0 && (
        <View style={styles.gridContainer}>
          <Text style={styles.gridTitle}>LGU Scores</Text>
          <View style={styles.markerGrid}>
            {markers.slice(0, 12).map((m) => (
              <TouchableOpacity
                key={m.id}
                style={styles.markerCell}
                onPress={m.onPress}
                activeOpacity={0.7}
              >
                <View
                  style={[
                    styles.markerDot,
                    { backgroundColor: getScoreHex(m.score) },
                  ]}
                >
                  <Text style={styles.markerScore}>
                    {m.score != null ? Math.round(m.score) : '?'}
                  </Text>
                </View>
                {m.name ? (
                  <Text style={styles.markerName} numberOfLines={1}>
                    {m.name}
                  </Text>
                ) : null}
              </TouchableOpacity>
            ))}
            {markers.length > 12 && (
              <View style={styles.markerCell}>
                <View style={styles.moreCircle}>
                  <Text style={styles.moreText}>+{markers.length - 12}</Text>
                </View>
                <Text style={styles.markerName}>more</Text>
              </View>
            )}
          </View>
        </View>
      )}
    </View>
  );
}

/* ─── OpenLayers Map (WebView) ─────────────────────────── */

function OLMapView({ style, initialRegion, markers = [], onPress }: SafeMapViewProps) {
  const center: [number, number] = useMemo(
    () => [initialRegion?.longitude ?? 121.774, initialRegion?.latitude ?? 12.8797],
    [initialRegion?.longitude, initialRegion?.latitude],
  );

  const zoom = useMemo(() => {
    if (!initialRegion?.latitudeDelta) return 6;
    return Math.round(Math.log2(360 / initialRegion.latitudeDelta));
  }, [initialRegion?.latitudeDelta]);

  const html = useMemo(
    () => buildMapHTML(center, zoom, markers),
    [center, zoom, markers],
  );

  const pressHandlers = useRef(new Map<string | number, (() => void) | undefined>());

  useEffect(() => {
    pressHandlers.current.clear();
    markers.forEach((m) => {
      if (m.onPress) pressHandlers.current.set(m.id, m.onPress);
    });
  }, [markers]);

  const handleMessage = useCallback(
    (event: any) => {
      try {
        const data = JSON.parse(event.nativeEvent.data);
        if (data.type === 'marker_press') {
          pressHandlers.current.get(data.id)?.();
        } else if (data.type === 'map_press') {
          onPress?.();
        }
      } catch { /* ignore */ }
    },
    [onPress],
  );

  return (
    <View style={[styles.container, style]}>
      <WebViewComponent
        source={{ html }}
        style={styles.webview}
        originWhitelist={['*']}
        onMessage={handleMessage}
        javaScriptEnabled
        domStorageEnabled
        scrollEnabled={false}
        bounces={false}
        overScrollMode="never"
        showsVerticalScrollIndicator={false}
        showsHorizontalScrollIndicator={false}
        androidLayerType="hardware"
        cacheEnabled
        cacheMode="LOAD_CACHE_ELSE_NETWORK"
      />
    </View>
  );
}

/* ─── Main Export ──────────────────────────────────────── */

export function SafeMapView(props: SafeMapViewProps) {
  const [crashed, setCrashed] = useState(false);

  if (!webViewAvailable || crashed) {
    return <MapFallback {...props} />;
  }

  return (
    <MapErrorBoundary onError={() => setCrashed(true)}>
      <OLMapView {...props} />
    </MapErrorBoundary>
  );
}

/* ─── Error Boundary ──────────────────────────────────── */

interface EBProps { onError: () => void; children: React.ReactNode }

class MapErrorBoundary extends React.Component<EBProps, { hasError: boolean }> {
  state = { hasError: false };
  static getDerivedStateFromError() { return { hasError: true }; }
  componentDidCatch() { this.props.onError(); }
  render() {
    return this.state.hasError ? null : this.props.children;
  }
}

export const nativeMapsAvailable = webViewAvailable;

/* ─── Styles ──────────────────────────────────────────── */

const styles = StyleSheet.create({
  container: { flex: 1 },
  webview: { flex: 1, backgroundColor: SipatColors.dashboardBg },

  fallback: {
    flex: 1,
    backgroundColor: SipatColors.dashboardBg,
    paddingHorizontal: 20,
    paddingVertical: 16,
  },
  headerSection: {
    alignItems: 'center',
    paddingTop: 12,
    paddingBottom: 16,
  },
  phEmoji: { fontSize: 60, marginBottom: 8 },
  fallbackTitle: {
    fontSize: 20, fontWeight: '700',
    color: SipatColors.navyLight, marginBottom: 2,
  },
  fallbackSub: {
    fontSize: 14, color: SipatColors.textSecondary, marginBottom: 12,
  },
  badge: {
    flexDirection: 'row', alignItems: 'center', gap: 6,
    backgroundColor: SipatColors.goldPale,
    paddingHorizontal: 14, paddingVertical: 6, borderRadius: 8,
  },
  badgeText: { fontSize: 11, color: SipatColors.navyLight },

  gridContainer: {
    flex: 1, backgroundColor: '#FFFFFF', borderRadius: 16, padding: 16,
    shadowColor: SipatColors.navy, shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06, shadowRadius: 8, elevation: 3,
  },
  gridTitle: {
    fontSize: 13, fontWeight: '700', color: SipatColors.navyLight,
    marginBottom: 12, letterSpacing: 0.3, textTransform: 'uppercase',
  },
  markerGrid: {
    flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'flex-start', gap: 6,
  },
  markerCell: {
    width: '23%' as any,
    alignItems: 'center', paddingVertical: 8,
    borderRadius: 10, backgroundColor: SipatColors.dashboardBg, marginBottom: 4,
  },
  markerDot: {
    width: 32, height: 32, borderRadius: 16,
    alignItems: 'center', justifyContent: 'center',
    borderWidth: 2, borderColor: '#fff', marginBottom: 4,
  },
  markerScore: { fontSize: 10, fontWeight: '800', color: '#fff' },
  markerName: {
    fontSize: 9, fontWeight: '600', color: SipatColors.textSecondary,
    textAlign: 'center', paddingHorizontal: 2,
  },
  moreCircle: {
    width: 32, height: 32, borderRadius: 16,
    backgroundColor: SipatColors.cardBorder,
    alignItems: 'center', justifyContent: 'center', marginBottom: 4,
  },
  moreText: { fontSize: 11, fontWeight: '700', color: SipatColors.textSecondary },
});
