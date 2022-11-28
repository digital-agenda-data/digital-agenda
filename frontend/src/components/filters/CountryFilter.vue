<script>
import BaseSelectFilter from "@/components/filters/BaseSelectFilter.vue";

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
      return this.items[0]?.id;
    },
  },
};
</script>
