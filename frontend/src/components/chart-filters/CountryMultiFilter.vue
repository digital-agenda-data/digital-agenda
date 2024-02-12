<script>
import CountryFilter from "@/components/chart-filters/CountryFilter.vue";
import { randomChoice } from "@/lib/utils";

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
  },
};
</script>
