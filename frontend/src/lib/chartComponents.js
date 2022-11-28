import ColumnCompareCountries from "@/components/charts/column/ColumnCompareCountries.vue";
import ColumnCompareBreakdowns from "@/components/charts/column/ColumnCompareBreakdowns.vue";
import SplineCompareCountries from "@/components/charts/spline/SplineCompareCountries.vue";

import columnChartUrl from "@/assets/chart-images/column/column-chart.png";
import columnChartMultipleUrl from "@/assets/chart-images/column/column-chart-multiple.png";
import splineChartUrl from "@/assets/chart-images/spline/spline-chart.png";

// Map values from the backend to frontend components
export default {
  COLUMN_COMPARE_COUNTRIES: {
    component: ColumnCompareCountries,
    image: columnChartUrl,
  },
  COLUMN_COMPARE_BREAKDOWNS: {
    component: ColumnCompareBreakdowns,
    image: columnChartMultipleUrl,
  },
  SPLINE_COMPARE_COUNTRIES: {
    component: SplineCompareCountries,
    image: splineChartUrl,
  },
};
