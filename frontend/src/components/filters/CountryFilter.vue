<script>
import BaseSelectFilter from "@/components/filters/base/BaseSelectFilter.vue";
import { randomChoice } from "@/lib/utils";

export default {
  name: "CountryMultiFilter",
  extends: BaseSelectFilter,
  props: {
    ignoreCountryGroups: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
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
    defaultSingleValue() {
      if (this.allowedValues.has("EU")) {
        return "EU";
      }
      return randomChoice(this.items)?.id;
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
