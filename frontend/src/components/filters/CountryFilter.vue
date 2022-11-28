<script>
import BaseSelectFilter from "@/components/filters/BaseSelectFilter.vue";
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
        this.$route.query.indicator &&
        `/indicators/${this.$route.query.indicator}/countries/`
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
