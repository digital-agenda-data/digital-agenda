import BarCompareCountries from "@/components/charts/BarCompareCountries.vue";
import BarCompareBreakdowns from "@/components/charts/BarCompareBreakdowns.vue";

import barChartUrl from "@/assets/chart-images/bar/bar-chart.png?url";
import barChartMultipleUrl from "@/assets/chart-images/bar/bar-chart-multiple.png?url";

export const CHARTS = {
  BAR_COMPARE_COUNTRIES: {
    component: BarCompareCountries,
    image: barChartUrl,
  },
  BAR_COMPARE_BREAKDOWNS: {
    component: BarCompareBreakdowns,
    image: barChartMultipleUrl,
  },
};
