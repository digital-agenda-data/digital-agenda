<script>
import BaseSelectFilter from "@/components/filters/base/BaseSelectFilter.vue";
import { randomChoice } from "@/lib/utils";

export default {
  name: "CountryMultiFilter",
  extends: BaseSelectFilter,
  computed: {
    queryName() {
      return "country";
    },
    endpoint() {
      return (
        this.filterStore.indicator &&
        `/indicators/${this.filterStore.indicator.code}/countries/`
      );
    },
    label() {
      return "Country";
    },
    defaultValue() {
      if (this.allowedValues.has("EU")) {
        return "EU";
      }
      return randomChoice(this.items)?.id;
    },
  },
};
</script>
