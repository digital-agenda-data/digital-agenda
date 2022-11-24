<script>
import BaseSelectFilter from "@/components/filters/BaseSelectFilter.vue";

export default {
  name: "CountryFilter",
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
      return "Select the countries";
    },
    multiple() {
      return true;
    },
    defaultValue() {
      // Default to none
      return [];
    },
  },
};
</script>
