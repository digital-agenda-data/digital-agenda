import ColumnCompareCountries from "@/components/charts/ColumnCompareCountries.vue";
import ColumnCompareBreakdowns from "@/components/charts/ColumnCompareBreakdowns.vue";

import columnChartUrl from "@/assets/chart-images/column/column-chart.png";
import columnChartMultipleUrl from "@/assets/chart-images/column/column-chart-multiple.png";

export const CHARTS = {
  COLUMN_COMPARE_COUNTRIES: {
    component: ColumnCompareCountries,
    image: columnChartUrl,
  },
  COLUMN_COMPARE_BREAKDOWNS: {
    component: ColumnCompareBreakdowns,
    image: columnChartMultipleUrl,
  },
};
