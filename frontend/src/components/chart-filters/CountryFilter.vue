<script>
import BaseSelectFilter from "@/components/chart-filters/base/BaseSelectFilter.vue";
import { randomChoice } from "@/lib/utils";
import { useChartStore } from "@/stores/chartStore.js";
import { mapState } from "pinia";

export default {
  name: "CountryFilter",
  extends: BaseSelectFilter,
  props: {
    ignoreCountryGroups: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    ...mapState(useChartStore, ["currentChart"]),
    queryName() {
      return "country";
    },
    endpoint() {
      return "/countries/";
    },
    label() {
      return this.multiple ? "Select the countries" : "Country";
    },
    multiple() {
      return this.currentChart.country_multi_filter ?? true;
    },
    defaultSingleValue() {
      if (this.allowedValues.has("EU")) {
        return "EU";
      }
      return randomChoice(this.items)?.id;
    },
    defaultMultiValue() {
      const result = [];
      if (this.allowedValues.has("EU")) {
        result.push("EU");
      }

      const another = randomChoice(
        this.allowedValuesArray.filter((code) => code !== "EU"),
      );
      if (another) {
        result.push(another);
      }

      return result.sort();
    },
    items() {
      const result = this.super(BaseSelectFilter).items();

      if (this.ignoreCountryGroups) {
        return result.filter((item) => !item.apiProps.is_group);
      }
      return result;
    },
  },
};
</script>
