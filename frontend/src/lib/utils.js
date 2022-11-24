import Highcharts from "highcharts";
import { SERIES_COLORS } from "@/lib/constants";

/**
 * Check if two arrays are equal
 *
 * @param a1 {Array}
 * @param a2 {Array}
 * @return {Boolean}
 */
export function arrayEquals(a1, a2) {
  if (a1.length !== a2.length) return false;
  for (let i = 0; i < a1.length; i++) {
    if (a1[i] !== a2[i]) return false;
  }
  return true;
}

/**
 * Scroll to the hash location in the URL
 */
export function scrollToHash() {
  const el = document.querySelector(window.location.hash);
  if (el) {
    el.scrollIntoView({
      behavior: "smooth",
    });
  }
}

export function getRouteMeta(to, key) {
  if (typeof to.meta[key] === "function") {
    return to.meta[key]();
  }
  return to.meta[key];
}

export function camelToSnakeCase(text) {
  return text.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);
}

export function colorForCountry(countryCode, seriesIndex = 0) {
  let color = new Highcharts.Color(
    SERIES_COLORS[seriesIndex % SERIES_COLORS.length]
  );

  if (countryCode === "EU") {
    color = color.brighten(-0.3);
  }

  return color.get();
}
