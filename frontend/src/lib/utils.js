import { useChartStore } from "@/stores/chartStore";
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

  document.querySelector(window.location.hash)?.scrollIntoView({
    behavior: "smooth",
  });
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
 *  - remove any axis reference (_x, _y, _z) from the end of the key
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
    SERIES_COLORS[seriesIndex % SERIES_COLORS.length],
  );

  // Highlight any "group" countries like: EU/EU27/EU28 by
  // darkening the color used for their series
  if (country.is_group) {
    color = color.brighten(-0.3);
  }

  return color.get();
}

/**
 * Get the appropriate label to use for this dimension in the currentChart.
 *
 * @param dimensionType {string} indicator/breakdown/unit/period/country
 * @param dimensionObj {Object} Dimension Object from the backend
 * @param defaultLabel {string} Default value to use if not specified in the backend
 * @return {string}
 */
function getDimensionLabel(
  dimensionType,
  dimensionObj,
  defaultLabel = "alt_label",
) {
  if (!dimensionObj) {
    return undefined;
  }

  const labelType =
    useChartStore().currentChart?.[`${dimensionType}_label`] || defaultLabel;

  switch (labelType) {
    case "code":
      return dimensionObj.code;
    case "label":
      return dimensionObj.label || dimensionObj.alt_label || dimensionObj.code;
    default:
    case "alt_label":
      return dimensionObj.alt_label || dimensionObj.label || dimensionObj.code;
  }
}

export function getIndicatorLabel(obj, defaultLabel = "alt_label") {
  return getDimensionLabel("indicator", obj, defaultLabel);
}

export function getBreakdownLabel(obj, defaultLabel = "alt_label") {
  return getDimensionLabel("breakdown", obj, defaultLabel);
}

// Default to the "long" label for periods as they include the time period type
// (Year: 2020 or Desi Period: 2020)
export function getPeriodLabel(obj, defaultLabel = "label") {
  return getDimensionLabel("period", obj, defaultLabel);
}

export function getUnitLabel(obj, defaultLabel = "alt_label") {
  return getDimensionLabel("unit", obj, defaultLabel);
}

export function getCountryLabel(obj, defaultLabel = "alt_label") {
  return getDimensionLabel("country", obj, defaultLabel);
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

  let numberFormat;
  const label = getUnitLabel(unit);
  const code = unit.code.toLowerCase();

  if (value === null || value === undefined || Number.isNaN(value)) {
    return "<b>Data not available</b>";
  }

  if (code.startsWith("pc_") || code.endsWith("_score")) {
    // Round to 2 fixed decimals for what is likely a percentage.
    // (E.g. 35.80%)
    numberFormat = {
      notation: "standard",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    };
  } else if (value < 100) {
    // No rounding for smaller values
    numberFormat = {
      notation: "standard",
      // We're still limited by 64bit float arithmetics rules, tho'
      maximumSignificantDigits: 17,
    };
  } else if (value < Math.pow(10, 6)) {
    // If less than 1 million, round to integer and include thousands' separators.
    // (E.g. 123,456)
    numberFormat = {
      notation: "standard",
      maximumFractionDigits: 0,
      useGrouping: "true",
    };
  } else {
    // Show the compact version for anything bigger, with 2 fixed decimals
    // (E.g. 24.20M)
    numberFormat = {
      notation: "compact",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
      useGrouping: "true",
    };
  }

  const valueStr = value.toLocaleString("en", numberFormat);

  if (label.startsWith("%")) {
    // No extra space if there is a percent in the unit label, as "5 %"
    // looks bad!
    return `${valueStr}${label}`;
  }
  return `${valueStr} ${label}`;
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

/**
 * Generate a sequence of numbers
 *
 * @param start {Number} value to start the range at
 * @param stop {Number} value to stop the range at (not included)
 * @param step {Number} value to increment by
 * @return {Number[]}
 */
export function range(start, stop, step = 1) {
  // Based on:
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/from#sequence_generator_range
  return Array.from(
    { length: (stop - start) / step },
    (_, i) => start + i * step,
  );
}

/**
 * Clamp a value between two other values.
 *
 * @param i {Number}
 * @param min {Number}
 * @param max {Number}
 * @return {Number}
 */
export function clamp(i, min, max) {
  return Math.min(max, Math.max(min, i));
}

/**
 * Group an Array of Objects by one unique property.
 *
 * @param items {Object[]}
 * @param key {String}
 * @param valueKey {String} if specified use the value of this key for the map
 *  instead of the actual object
 * @return {Map}
 */
export function groupByUnique(items, key = "code", valueKey = null) {
  const result = new Map();
  for (const item of items) {
    result.set(item[key], valueKey ? item[valueKey] : item);
  }
  return result;
}

/**
 * Group an Array of Objects by one property
 *
 * @param items {Object[]}
 * @param key {String}
 * @return {{String: Array}}
 */
export function groupBy(items, key) {
  const result = {};
  for (const item of items) {
    result[item[key]] ??= [];
    result[item[key]].push(item);
  }
  return result;
}

/**
 * Group array of objects by the specified keys. All values for the keys
 * must also be strings for this to work. Results in an Object structure like:
 *
 * {
 *   "<value for key1>": {
 *     "<value for key2>": <item>,
 *     "<value for key2>": <item>
 *     ...
 *   },
 *   ...
 * }
 *
 * The combination of keys must be unique, otherwise items will be lost
 *
 * @param items {Object[]}
 * @param keys {String[]}
 * @param valueKey {String} if specified use the value of this key for the final
 *  group instead of the actual item
 * @return {{}}
 */
export function groupByMulti(items, keys, valueKey = null) {
  if (!items || !keys || keys.length === 0) {
    return {};
  }

  if (keys.length === 1) {
    return Object.fromEntries(groupByUnique(items, keys[0], valueKey));
  }

  const otherKeys = keys.slice(1);
  const result = groupBy(items, keys[0]);

  for (const resultKey in result) {
    result[resultKey] = groupByMulti(result[resultKey], otherKeys, valueKey);
  }
  return result;
}

/**
 * Force the item to an Array.
 *
 * @param item {*}
 * @return {[]}
 */
export function forceArray(item) {
  if (!item) return [];
  if (Array.isArray(item)) return item;
  return [item];
}

/**
 * Convert an HTML string to plaintext
 *
 * @param html {String}
 * @return {string}
 */
export function htmlToText(html) {
  const el = document.createElement("div");
  el.innerHTML = html;
  return el.textContent;
}

/**
 * Create a copy of the array, and sort it based on numeric comparison
 *
 * @param array {Array}
 * @param reverse {Boolean} reverse the order if set to true
 * @param keyFunc {Function} function used to get the number from an array item;
 *  if not specified the item itself is expected to be a valid number
 * @return {Array} the new sorted array
 */
export function sortNumeric(array, { reverse = false, keyFunc = (i) => i }) {
  return Array.from(array).sort((item1, item2) => {
    const val1 = keyFunc(item1);
    const val2 = keyFunc(item2);

    return reverse ? val2 - val1 : val1 - val2;
  });
}

/**
 * Given a single chart options object or an array of such objects return
 * the first existing custom marker symbol value.
 *
 * @param iterable {Array|Object}
 * @return {string}
 */
export function getMarkerSymbol(iterable) {
  for (const item of forceArray(iterable)) {
    if (!item) continue;

    if (item.custom_symbol) {
      return `url(${item.custom_symbol})`;
    }
    if (item.symbol) {
      return item.symbol;
    }
  }
}

/**
 * Return a date corresponding to the January first of the specified year.
 *
 * @param year {Number}
 * @return {Number}
 */
export function getDateFromYear(year) {
  if (!year || year < 0) return null;
  return Date.UTC(year, 0, 1);
}
