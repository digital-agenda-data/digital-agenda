<script>
import CountryFilter from "@/components/filters/CountryFilter.vue";

export default {
  name: "CountryMultiFilter",
  extends: CountryFilter,
  computed: {
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
