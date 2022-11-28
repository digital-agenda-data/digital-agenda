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
 * Check if two sets are equal
 *
 * @param s1 {Set}
 * @param s2 {Set}
 * @return {Boolean}
 */
export function setEquals(s1, s2) {
  if (s1.size !== s2.size) return false;
  for (const item of s1) {
    if (!s1.has(item)) return false;
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

/**
 * Get Meta value from route
 *
 * @param to {Object} RouterLocation
 * @param key {String}
 * @return {*}
 */
export function getRouteMeta(to, key) {
  if (typeof to.meta[key] === "function") {
    return to.meta[key]();
  }
  return to.meta[key];
}

/**
 * Convert text from camelCase to snake_case
 */
export function camelToSnakeCase(text) {
  return text.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);
}

/**
 * Get chart color for the specified country and series
 *
 * @param countryCode {String}
 * @param seriesIndex {Number}
 * @return {String} rgba
 */
export function colorForCountry(countryCode, seriesIndex = 0) {
  let color = new Highcharts.Color(
    SERIES_COLORS[seriesIndex % SERIES_COLORS.length]
  );

  if (countryCode === "EU") {
    color = color.brighten(-0.3);
  }

  return color.get();
}

/**
 * Get a suitable display string for this backend object
 *
 * @param item {Object} Dimension object from backend
 * @return {String}
 */
export function getDisplay(item) {
  return item && (item.alt_label || item.label || item.code);
}

/***
 * Return a random item from an array
 *
 * @param items {Array}
 * @return {*}
 */
export function randomChoice(items) {
  if (!items || !Array.isArray(items) || items.length === 0) {
    return undefined;
  }
  return items[Math.floor(Math.random() * items.length)];
}
