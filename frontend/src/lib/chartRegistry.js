import ColumnCompareCountries from "@/components/charts/column/ColumnCompareCountries.vue";
import ColumnCompareBreakdowns from "@/components/charts/column/ColumnCompareBreakdowns.vue";
import ColumnStackedCompareBreakdowns from "@/components/charts/column/ColumnStackedCompareBreakdowns.vue";
import ColumnStackedCompareBreakdownsWeighted from "@/components/charts/column/ColumnStackedCompareBreakdownsWeighted.vue";

import BarCompareBreakdowns from "@/components/charts/bar/BarCompareBreakdowns.vue";
import BarCompareCountries from "@/components/charts/bar/BarCompareCountries.vue";
import BarStackedCompareBreakdowns from "@/components/charts/bar/BarStackedCompareBreakdowns.vue";
import BarStackedCompareBreakdownsWeighted from "@/components/charts/bar/BarStackedCompareBreakdownsWeighted.vue";

import SplineCompareCountries from "@/components/charts/spline/SplineCompareCountries.vue";
import SplineCompareBreakdowns from "@/components/charts/spline/SplineCompareBreakdowns.vue";
import SplineCompareTwoIndicators from "@/components/charts/spline/SplineCompareTwoIndicators.vue";

import ScatterCompareTwoIndicators from "@/components/charts/scatter/ScatterCompareTwoIndicators.vue";
import BubbleCompareThreeIndicators from "@/components/charts/bubble/BubbleCompareThreeIndicators.vue";

import MapCompareCountries from "@/components/charts/map/MapCompareCountries.vue";
import TableDebugData from "@/components/charts/table/TableDebugData.vue";

// Map values from the backend to frontend components
export default {
  COLUMN_COMPARE_COUNTRIES: ColumnCompareCountries,
  COLUMN_COMPARE_BREAKDOWNS: ColumnCompareBreakdowns,
  COLUMN_STACKED_COMPARE_BREAKDOWNS: ColumnStackedCompareBreakdowns,
  COLUMN_STACKED_COMPARE_BREAKDOWNS_WEIGHTED:
    ColumnStackedCompareBreakdownsWeighted,
  BAR_COMPARE_COUNTRIES: BarCompareCountries,
  BAR_COMPARE_BREAKDOWNS: BarCompareBreakdowns,
  BAR_STACKED_COMPARE_BREAKDOWNS: BarStackedCompareBreakdowns,
  BAR_STACKED_COMPARE_BREAKDOWNS_WEIGHTED: BarStackedCompareBreakdownsWeighted,
  SPLINE_COMPARE_COUNTRIES: SplineCompareCountries,
  SPLINE_COMPARE_BREAKDOWNS: SplineCompareBreakdowns,
  SPLINE_COMPARE_TWO_INDICATORS: SplineCompareTwoIndicators,
  SCATTER_COMPARE_TWO_INDICATORS: ScatterCompareTwoIndicators,
  BUBBLE_COMPARE_THREE_INDICATORS: BubbleCompareThreeIndicators,
  MAP_COMPARE_COUNTRIES: MapCompareCountries,
  TABLE_DEBUG_DATA: TableDebugData,
};
