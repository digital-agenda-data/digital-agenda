import ColumnCompareCountries from "@/components/charts/column/ColumnCompareCountries.vue";
import ColumnCompareBreakdowns from "@/components/charts/column/ColumnCompareBreakdowns.vue";
import SplineCompareCountries from "@/components/charts/spline/SplineCompareCountries.vue";
import SplineCompareBreakdowns from "@/components/charts/spline/SplineCompareBreakdowns.vue";
import ScatterCompareTwoIndicators from "@/components/charts/scatter/ScatterCompareTwoIndicators.vue";
import BubbleCompareThreeIndicators from "@/components/charts/bubble/BubbleCompareThreeIndicators.vue";
import SplineCompareTwoIndicators from "@/components/charts/spline/SplineCompareTwoIndicators.vue";
import ColumnStackedCompareBreakdowns from "@/components/charts/column/ColumnStackedCompareBreakdowns.vue";

import columnChartUrl from "@/assets/chart-images/column/column-chart.png";
import columnChartMultipleUrl from "@/assets/chart-images/column/column-chart-multiple.png";
import columnChartStackedUrl from "@/assets/chart-images/column/column-chart-stacked.png";
import splineChartUrl from "@/assets/chart-images/spline/spline-chart.png";
import splineChart2Url from "@/assets/chart-images/spline/spline-chart-2.png";
import scatterChartUrl from "@/assets/chart-images/scatter/scatter-chart.png";
import bubbleChartUrl from "@/assets/chart-images/bubble/bubble-chart.png";

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
  COLUMN_STACKED_COMPARE_BREAKDOWNS: {
    component: ColumnStackedCompareBreakdowns,
    image: columnChartStackedUrl,
  },
  SPLINE_COMPARE_COUNTRIES: {
    component: SplineCompareCountries,
    image: splineChartUrl,
  },
  SPLINE_COMPARE_BREAKDOWNS: {
    component: SplineCompareBreakdowns,
    image: splineChart2Url,
  },
  SPLINE_COMPARE_TWO_INDICATORS: {
    component: SplineCompareTwoIndicators,
    image: splineChart2Url,
  },
  SCATTER_COMPARE_TWO_INDICATORS: {
    component: ScatterCompareTwoIndicators,
    image: scatterChartUrl,
  },
  BUBBLE_COMPARE_THREE_INDICATORS: {
    component: BubbleCompareThreeIndicators,
    image: bubbleChartUrl,
  },
};
