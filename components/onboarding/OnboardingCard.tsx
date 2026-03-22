import React from 'react';
import { Dimensions, StyleSheet, Text, View } from 'react-native';
import Svg, { Defs, LinearGradient, Stop, Path } from 'react-native-svg';

import { SipatColors } from '@/constants/theme';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

interface OnboardingCardProps {
  title: string;
  subtitle: string;
  body: string;
}

/**
 * Onboarding card matching the design mockup:
 *   • Top: Red arch flowing downward (like the shield's red figure)
 *   • Center: White area with text
 *   • Bottom: Navy/blue arch rising upward (like the shield's bottom)
 *
 * The two arches mirror the shield emblem, split apart to reveal content.
 */
export const OnboardingCard = React.memo(function OnboardingCard({ title, subtitle, body }: OnboardingCardProps) {
  const cardH = SCREEN_HEIGHT * 0.78; // leave room for dots/controls
  const archH = cardH * 0.28;

  return (
    <View style={[styles.card, { height: cardH }]}>
      {/* ── Top red arch ───────────────────────────── */}
      <View style={[styles.archContainer, { height: archH }]}>
        <Svg
          width={SCREEN_WIDTH}
          height={archH}
          viewBox={`0 0 ${SCREEN_WIDTH} ${archH}`}
          preserveAspectRatio="none"
        >
          <Defs>
            <LinearGradient id="topRed" x1="0.5" y1="0" x2="0.5" y2="1">
              <Stop offset="0" stopColor={SipatColors.red} />
              <Stop offset="0.8" stopColor={SipatColors.redLight} />
              <Stop offset="1" stopColor={SipatColors.red} stopOpacity="0.6" />
            </LinearGradient>
          </Defs>
          {/* Flowing arch — widest at top, narrows to a point */}
          <Path
            d={`
              M 0 0
              L ${SCREEN_WIDTH} 0
              L ${SCREEN_WIDTH} ${archH * 0.25}
              C ${SCREEN_WIDTH * 0.75} ${archH * 0.6}
                ${SCREEN_WIDTH * 0.6} ${archH * 0.85}
                ${SCREEN_WIDTH * 0.5} ${archH}
              C ${SCREEN_WIDTH * 0.4} ${archH * 0.85}
                ${SCREEN_WIDTH * 0.25} ${archH * 0.6}
                0 ${archH * 0.25}
              Z
            `}
            fill="url(#topRed)"
          />
        </Svg>
      </View>

      {/* ── Center text ────────────────────────────── */}
      <View style={styles.textArea}>
        <Text style={styles.title}>{title}</Text>
        <Text style={styles.subtitle}>{subtitle}</Text>
        <Text style={styles.body}>{body}</Text>
      </View>

      {/* ── Bottom navy/blue arch ──────────────────── */}
      <View style={[styles.archContainer, { height: archH }]}>
        <Svg
          width={SCREEN_WIDTH}
          height={archH}
          viewBox={`0 0 ${SCREEN_WIDTH} ${archH}`}
          preserveAspectRatio="none"
        >
          <Defs>
            <LinearGradient id="botNavy" x1="0.5" y1="1" x2="0.5" y2="0">
              <Stop offset="0" stopColor={SipatColors.navy} />
              <Stop offset="0.4" stopColor={SipatColors.navyLight} />
              <Stop offset="1" stopColor={SipatColors.blue} stopOpacity="0.7" />
            </LinearGradient>
            <LinearGradient id="botBlue" x1="0.5" y1="1" x2="0.5" y2="0">
              <Stop offset="0" stopColor={SipatColors.blue} />
              <Stop offset="1" stopColor={SipatColors.blueLight} stopOpacity="0.5" />
            </LinearGradient>
          </Defs>
          {/* Navy arch — inverted, rising from bottom */}
          <Path
            d={`
              M 0 ${archH}
              L ${SCREEN_WIDTH} ${archH}
              L ${SCREEN_WIDTH} ${archH * 0.7}
              C ${SCREEN_WIDTH * 0.78} ${archH * 0.35}
                ${SCREEN_WIDTH * 0.62} ${archH * 0.12}
                ${SCREEN_WIDTH * 0.5} 0
              C ${SCREEN_WIDTH * 0.38} ${archH * 0.12}
                ${SCREEN_WIDTH * 0.22} ${archH * 0.35}
                0 ${archH * 0.7}
              Z
            `}
            fill="url(#botNavy)"
          />
          {/* Inner blue accent arc */}
          <Path
            d={`
              M ${SCREEN_WIDTH * 0.15} ${archH}
              L ${SCREEN_WIDTH * 0.85} ${archH}
              L ${SCREEN_WIDTH * 0.85} ${archH * 0.82}
              C ${SCREEN_WIDTH * 0.72} ${archH * 0.55}
                ${SCREEN_WIDTH * 0.6} ${archH * 0.4}
                ${SCREEN_WIDTH * 0.5} ${archH * 0.28}
              C ${SCREEN_WIDTH * 0.4} ${archH * 0.4}
                ${SCREEN_WIDTH * 0.28} ${archH * 0.55}
                ${SCREEN_WIDTH * 0.15} ${archH * 0.82}
              Z
            `}
            fill="url(#botBlue)"
            opacity={0.35}
          />
        </Svg>
      </View>
    </View>
  );
});

const styles = StyleSheet.create({
  card: {
    width: SCREEN_WIDTH,
    backgroundColor: '#FFFFFF',
  },
  archContainer: {
    width: SCREEN_WIDTH,
    overflow: 'hidden',
  },
  textArea: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 36,
  },
  title: {
    fontSize: 20,
    fontWeight: '400',
    color: SipatColors.textPrimary,
    textAlign: 'center',
    letterSpacing: 0.5,
  },
  subtitle: {
    fontSize: 28,
    fontWeight: '700',
    color: SipatColors.navyLight,
    textAlign: 'center',
    marginTop: 4,
  },
  body: {
    fontSize: 15,
    color: SipatColors.textSecondary,
    textAlign: 'center',
    marginTop: 16,
    lineHeight: 22,
  },
});
