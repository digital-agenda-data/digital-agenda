# Adding a new chart type

## Adding a new backend choice

- Add new chart type choice in the [Chart model](../digital_agenda/apps/charts/models.py)
- Migrate the DB to include the new choice:
```shell
python manage.py makemigrations
python manage.py migrate
```
- Add a new chart for the new type in the desired chart group via the [admin](http://localhost:8000/admin/charts/chart/add/)
- _Optionally_ dump new fixtures for thew new chart type. The custom utility can be used:
```shell
python manage.py dump_chart_fixtures
```

## Registering the new component in frontend

- Add new single file component for the chart in the corresponding chart directory [frontend/src/components/charts](../frontend/src/components/charts/) (e.g. column, map, bubble etc.)
```vue
<!-- frontend/src/components/charts/column/MyNewChart.vue -->

<script>
export default {
  name: "MyNewChart",
}
</script>
```
- Add the new chart component to the registry [frontend/src/lib/chartRegistry.js](../frontend/src/lib/chartRegistry.js)
- _Optionally_ add an image for the new chart type to the defaults [frontend/src/lib/chartDefaultImages.js](../frontend/src/lib/chartDefaultImages.js) 

## Implementing a new component 
- Have the new component extend one of the [base chart](../frontend/src/components/charts/base/) or any other existing chart. Example:
```vue
<script>
import BaseChart from "@/components/charts/base/BaseChart.vue";

export default {
  name: "MyNewChart",
  extends: BaseChart,   
}
</script>
```
- Implement required computed properties. A simple column chart example:
```vue
<script>
import BaseChart from "@/components/charts/base/BaseChart.vue";
import IndicatorGroupFilter from "@/components/filters/IndicatorGroupFilter.vue";
import IndicatorFilter from "@/components/filters/IndicatorFilter.vue";
import PeriodFilter from "@/components/filters/PeriodFilter.vue";
import UnitFilter from "@/components/filters/UnitFilter.vue";
import BreakdownGroupFilter from "@/components/filters/BreakdownGroupFilter.vue";
import BreakdownFilter from "@/components/filters/BreakdownFilter.vue";

export default {
  name: "MyNewChart",
  extends: BaseChart,
  computed: {
    chartType() {
      return "column";
    },
    // Filters to display for the user 
    filterComponents() {
      return [
        IndicatorGroupFilter,
        IndicatorFilter,
        BreakdownGroupFilter,
        BreakdownFilter,
        PeriodFilter,
        UnitFilter,
      ];
    },
    // Filters to send to the backend
    endpointFilters() {
      return ["breakdown", "period", "indicator", "unit"];
    },
    // Series used for the chart
    series() {
      return [
        {
          data: this.apiData.map((fact) => {
            return {
              y: fact.value || 0,
              name: fact.country,
              // Include the fact in the series as may be needed for some 
              // tooltip/labels. E.g. to determine when to display the "N/A" 
              // data label if there is no data available.
              fact,
            };
          }),
        },
      ];
    },
    // Extra options
    chartOptions() {
      return {
        xAxis: {
          type: "category",
        },
      };
    },
  },
};
</script>
```

See the documentation for each computed property in the [BaseChart](../frontend/src/components/charts/base/BaseChart.vue) for further explanation; as well as the [highcharts api documentation](https://api.highcharts.com/highcharts/).

 