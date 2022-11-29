<script>
import CountryFilter from "@/components/filters/CountryFilter.vue";
import { randomChoice } from "@/lib/utils";

export default {
  name: "CountryMultiFilter",
  extends: CountryFilter,
  props: {
    allInitialCountries: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    label() {
      return "Select the countries";
    },
    multiple() {
      return true;
    },
    defaultValue() {
      const allCodesArray = Array.from(this.allowedValues);

      if (this.allInitialCountries) {
        return allCodesArray.sort();
      }

      const result = [];
      if (this.allowedValues.has("EU")) {
        result.push("EU");
      }

      const another = randomChoice(
        allCodesArray.filter((code) => code !== "EU")
      );
      if (another) {
        result.push(another);
      }

      return result.sort();
    },
  },
};
</script>
