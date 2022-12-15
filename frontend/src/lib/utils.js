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
 * Check if two objects are equal
 *
 * @param o1 {Object}
 * @param o2 {Object}
 * @return {Boolean}
 */
export function objectEquals(o1, o2) {
  const o1Keys = Object.keys(o1 || {});
  const o2Keys = Object.keys(o2 || {});

  if (o1Keys.length !== o2Keys.length) return false;
  for (const key of o1Keys) {
    if (o1[key] !== o2[key]) return false;
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
  if (!window.location.hash) return;

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
 * Convert filter store key to api key:
 *  - convert to snake case
 *  - remove any _x or _y from the of the key
 */
export function toAPIKey(key) {
  return camelToSnakeCase(key).replace(/_[xyz]$/i, "");
}

/**
 * Get chart color for the specified country and series
 *
 * @param country {Object} Country object from the backend
 * @param seriesIndex {Number}
 * @return {String} rgba
 */
export function colorForCountry(country, seriesIndex = 0) {
  let color = new Highcharts.Color(
    SERIES_COLORS[seriesIndex % SERIES_COLORS.length]
  );

  // Highlight any "group" countries like: EU/EU27/EU28 by
  // darkening the color used for their series
  if (country.is_group) {
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

/**
 * Get a suitable display string for this unit value
 *
 * @param value {Number} Unit value
 * @param unit {Object} Unit object from the backend
 * @return {string}
 */
export function getUnitDisplay(value, unit) {
  if (!unit) return;

  if (value === null || value === undefined) {
    return `N/A ${unit.alt_label}`;
  } else if (unit.alt_label.startsWith("%")) {
    return `${value}${unit.alt_label}`;
  } else {
    return `${value} ${unit.alt_label}`;
  }
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
