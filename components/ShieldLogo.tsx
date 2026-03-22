import Svg, { Defs, LinearGradient, RadialGradient, Stop, Path, Circle, Ellipse, G } from 'react-native-svg';

interface ShieldLogoProps {
  size?: number;
}

/**
 * SipatGov Shield Emblem
 *
 * Matches the brand logo: a shield with a red central figure (arms spread),
 * blue eye-arc at the crown, gold pupil, gold side curves, on a deep
 * navy / purple body.
 */
export function ShieldLogo({ size = 160 }: ShieldLogoProps) {
  return (
    <Svg width={size} height={size * 1.15} viewBox="0 0 160 184">
      <Defs>
        {/* Shield body — deep navy to purple */}
        <LinearGradient id="shieldBody" x1="0" y1="0" x2="0" y2="1">
          <Stop offset="0" stopColor="#1E1040" />
          <Stop offset="0.5" stopColor="#140E30" />
          <Stop offset="1" stopColor="#0A0E1A" />
        </LinearGradient>

        {/* Red figure — warm coral-red */}
        <LinearGradient id="redFigure" x1="0.5" y1="0" x2="0.5" y2="1">
          <Stop offset="0" stopColor="#E8384F" />
          <Stop offset="0.6" stopColor="#CE1126" />
          <Stop offset="1" stopColor="#8B0D1A" />
        </LinearGradient>

        {/* Dark red wings */}
        <LinearGradient id="redWings" x1="0" y1="0" x2="0" y2="1">
          <Stop offset="0" stopColor="#8B2240" />
          <Stop offset="1" stopColor="#4A0E20" />
        </LinearGradient>

        {/* Blue eye arc */}
        <LinearGradient id="blueArc" x1="0" y1="0" x2="0" y2="1">
          <Stop offset="0" stopColor="#1E6FD9" />
          <Stop offset="1" stopColor="#0038A8" />
        </LinearGradient>

        {/* Gold border curves */}
        <LinearGradient id="goldCurve" x1="0" y1="0" x2="1" y2="1">
          <Stop offset="0" stopColor="#E8C96A" />
          <Stop offset="0.5" stopColor="#D4A843" />
          <Stop offset="1" stopColor="#B8912E" />
        </LinearGradient>

        {/* Navy bottom section */}
        <LinearGradient id="navyBottom" x1="0" y1="0" x2="0" y2="1">
          <Stop offset="0" stopColor="#1B2A5B" />
          <Stop offset="1" stopColor="#0A1235" />
        </LinearGradient>

        {/* Ambient glow behind logo */}
        <RadialGradient id="glow" cx="0.5" cy="0.35" r="0.5">
          <Stop offset="0" stopColor="#D4A843" stopOpacity="0.15" />
          <Stop offset="1" stopColor="#D4A843" stopOpacity="0" />
        </RadialGradient>
      </Defs>

      {/* Ambient glow */}
      <Circle cx="80" cy="65" r="75" fill="url(#glow)" />

      {/* ── Gold side curves (outer border) ─────────── */}
      <Path
        d="M30 55 C25 75 22 100 28 130 C34 155 55 170 80 180"
        stroke="url(#goldCurve)"
        strokeWidth="2.5"
        fill="none"
        strokeLinecap="round"
      />
      <Path
        d="M130 55 C135 75 138 100 132 130 C126 155 105 170 80 180"
        stroke="url(#goldCurve)"
        strokeWidth="2.5"
        fill="none"
        strokeLinecap="round"
      />

      {/* ── Shield body ─────────────────────────────── */}
      <Path
        d="M80 10 C55 10 38 25 35 40 C32 55 30 75 32 95 C34 120 48 150 80 172 C112 150 126 120 128 95 C130 75 128 55 125 40 C122 25 105 10 80 10 Z"
        fill="url(#shieldBody)"
      />

      {/* ── Dark-red side petals (wings) ────────────── */}
      <Path
        d="M40 65 C42 80 48 100 55 110 C60 118 68 122 75 118 C70 105 62 90 55 78 C50 70 44 65 40 65 Z"
        fill="url(#redWings)"
        opacity={0.9}
      />
      <Path
        d="M120 65 C118 80 112 100 105 110 C100 118 92 122 85 118 C90 105 98 90 105 78 C110 70 116 65 120 65 Z"
        fill="url(#redWings)"
        opacity={0.9}
      />

      {/* ── Red central figure (spread arms) ────────── */}
      <Path
        d="M80 45 C76 55 68 70 56 82 C52 86 54 92 58 90 C66 86 74 78 80 68 C86 78 94 86 102 90 C106 92 108 86 104 82 C92 70 84 55 80 45 Z"
        fill="url(#redFigure)"
      />
      {/* Central body drop */}
      <Path
        d="M76 90 C78 110 79 135 80 165 C81 135 82 110 84 90 C82 95 78 95 76 90 Z"
        fill="url(#redFigure)"
        opacity={0.9}
      />

      {/* ── Blue eye arc (crown) ────────────────────── */}
      <Path
        d="M56 42 C60 32 70 26 80 26 C90 26 100 32 104 42 C100 36 90 32 80 32 C70 32 60 36 56 42 Z"
        fill="url(#blueArc)"
      />
      {/* Thicker blue arc */}
      <Path
        d="M52 48 C58 34 68 28 80 28 C92 28 102 34 108 48 C104 38 92 30 80 30 C68 30 56 38 52 48 Z"
        fill="url(#blueArc)"
        opacity={0.7}
      />

      {/* ── Central eye ─────────────────────────────── */}
      <Ellipse cx="80" cy="48" rx="10" ry="6" fill="#0038A8" opacity={0.5} />
      <Ellipse cx="80" cy="48" rx="6" ry="4" fill="#FFD700" />
      <Circle cx="80" cy="48" r="2" fill="#0038A8" />

      {/* ── Navy blue bottom section ────────────────── */}
      <Path
        d="M42 120 C50 140 64 155 80 164 C96 155 110 140 118 120 C112 138 98 152 80 158 C62 152 48 138 42 120 Z"
        fill="url(#navyBottom)"
        opacity={0.85}
      />
      {/* Blue accent line */}
      <Path
        d="M50 125 C58 142 68 152 80 156 C92 152 102 142 110 125"
        stroke="#1E6FD9"
        strokeWidth="1.5"
        fill="none"
        opacity={0.6}
      />
    </Svg>
  );
}
