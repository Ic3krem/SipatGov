import { format, formatDistanceToNow, parseISO } from 'date-fns';

/**
 * Format a number as Philippine Peso currency.
 * e.g., 5000000 -> "₱5,000,000.00"
 */
export function formatPeso(amount: number | null | undefined): string {
  if (amount == null) return '₱0.00';
  return `₱${amount.toLocaleString('en-PH', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
}

/**
 * Format a number in compact form for display.
 * e.g., 5000000 -> "₱5.0M", 150000 -> "₱150K"
 */
export function formatPesoCompact(amount: number | null | undefined): string {
  if (amount == null) return '₱0';
  if (amount >= 1_000_000_000) return `₱${(amount / 1_000_000_000).toFixed(1)}B`;
  if (amount >= 1_000_000) return `₱${(amount / 1_000_000).toFixed(1)}M`;
  if (amount >= 1_000) return `₱${(amount / 1_000).toFixed(0)}K`;
  return `₱${amount.toFixed(0)}`;
}

/**
 * Format a percentage (0-100) with one decimal place.
 */
export function formatPercent(value: number | null | undefined): string {
  if (value == null) return '0%';
  return `${value.toFixed(1)}%`;
}

/**
 * Format an ISO date string to a readable date.
 * e.g., "2026-03-22" -> "Mar 22, 2026"
 */
export function formatDate(dateStr: string | null | undefined): string {
  if (!dateStr) return '';
  try {
    return format(parseISO(dateStr), 'MMM d, yyyy');
  } catch {
    return '\u2014';
  }
}

/**
 * Format an ISO date string to a relative time.
 * e.g., "2026-03-20T..." -> "2 days ago"
 */
export function formatRelativeDate(dateStr: string | null | undefined): string {
  if (!dateStr) return '';
  try {
    return formatDistanceToNow(parseISO(dateStr), { addSuffix: true });
  } catch {
    return '\u2014';
  }
}

/**
 * Format a confidence score (0-1) to a display percentage.
 */
export function formatConfidence(score: number | null | undefined): string {
  if (score == null) return 'N/A';
  return `${(score * 100).toFixed(0)}%`;
}

/**
 * Format a large number with commas.
 */
export function formatNumber(value: number | null | undefined): string {
  if (value == null) return '0';
  return value.toLocaleString('en-PH');
}
