import imgURL from "@/assets/placeholder.png?url";

export const placeholderImageURL = imgURL;
export const FILTERS = [
  "indicatorGroup",
  "indicator",
  "breakdownGroup",
  "breakdown",
  "period",
  "unit",
  "country",
];

export const FILTER_SUFFIXES = ["X", "Y", "Z", ""];

export const SERIES_COLORS = [
  "#63b8ff",
  "#E41A1C",
  "#4DAF4A",
  "#984EA3",
  "#FF7F00",
  "#FFFF33",
  "#A65628",
  "#F781BF",
  "#0d233a",
  "#AABC66",
  "#FD8245",
  "#21FF00",
  "#FF5400",
  "#1C3FFD",
  "#FFC600",
  "#45BF55",
  "#0EEAFF",
  "#6A07B0",
  "#044C29",
  "#7FB2F0",
  "#15A9FA",
  "#33EED2",
  "#D40D12",
  "#ADF0F6",
  "#662293",
  "#19BC01",
  "#9A24ED",
  "#D50356",
  "#D59AFE",
  "#35478C",
  "#FF40F4",
  "#F70A9B",
  "#FF1D23",
  "#FFFC00",
  "#1B76FF",
  "#436B06",
  "#648E23",
  "#7DC30F",
  "#9900AB",
  "#D000C4",
  "#D000C4",
  "#0B4EA2",
];

// Hardcoded list determining what axes are the "value" axis
// depending on the chart type. Used for custom axis ranges.
export const VALUE_AXIS = {
  bar: ["xAxis"],
  bubble: ["xAxis", "yAxis"],
  column: ["yAxis"],
  scatter: ["xAxis", "yAxis"],
  spline: ["yAxis"],
};
// Hardcoded list determining what axes are the "year" axis
// depending on the chart type. Used for custom axis ranges.
export const YEAR_AXIS = {
  spline: ["xAxis"],
};
