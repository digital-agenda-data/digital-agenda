import columnChartUrl from "@/assets/chart-images/column/column-chart.png";
import columnChartMultipleUrl from "@/assets/chart-images/column/column-chart-multiple.png";
import columnChartStackedUrl from "@/assets/chart-images/column/column-chart-stacked.png";
import splineChartUrl from "@/assets/chart-images/spline/spline-chart.png";
import splineChart2Url from "@/assets/chart-images/spline/spline-chart-2.png";
import scatterChartUrl from "@/assets/chart-images/scatter/scatter-chart.png";
import bubbleChartUrl from "@/assets/chart-images/bubble/bubble-chart.png";
import mapChartUrl from "@/assets/chart-images/map/map-chart.png";

// Map values from the backend to default images
export default {
  COLUMN_COMPARE_COUNTRIES: columnChartUrl,
  COLUMN_COMPARE_BREAKDOWNS: columnChartMultipleUrl,
  COLUMN_STACKED_COMPARE_BREAKDOWNS: columnChartMultipleUrl,
  COLUMN_STACKED_COMPARE_BREAKDOWNS_WEIGHTED: columnChartStackedUrl,
  BAR_COMPARE_COUNTRIES: null,
  BAR_COMPARE_BREAKDOWNS: null,
  BAR_STACKED_COMPARE_BREAKDOWNS: null,
  BAR_STACKED_COMPARE_BREAKDOWNS_WEIGHTED: null,
  SPLINE_COMPARE_COUNTRIES: splineChartUrl,
  SPLINE_COMPARE_BREAKDOWNS: splineChart2Url,
  SPLINE_COMPARE_TWO_INDICATORS: splineChart2Url,
  SCATTER_COMPARE_TWO_INDICATORS: scatterChartUrl,
  BUBBLE_COMPARE_THREE_INDICATORS: bubbleChartUrl,
  MAP_COMPARE_COUNTRIES: mapChartUrl,
  TABLE_DEBUG_DATA: null,
};
