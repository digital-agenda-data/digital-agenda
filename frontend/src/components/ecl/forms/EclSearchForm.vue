<template>
  <form
    class="ecl-search-form"
    role="search"
    :action="searchAction"
    :method="method"
  >
    <div class="ecl-form-group">
      <div v-if="helpText" class="ecl-help-block">
        {{ helpText }}
      </div>
      <label :for="inputName" class="ecl-form-label ecl-search-form__label">
        Search
      </label>
      <input
        v-model="value"
        :name="inputName"
        type="search"
        class="ecl-text-input ecl-text-input--m ecl-search-form__text-input"
        :placeholder="placeholder"
        aria-label="Search"
      />
    </div>

    <ecl-button
      variant="search"
      label="Search"
      icon="search"
      type="submit"
      class="ecl-search-form__button"
    />
  </form>
</template>

<script>
import EclButton from "@/components/ecl/EclButton.vue";

/**
 * ECL Search Form component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/forms/search-form/usage/
 *
 */
export default {
  name: "EclSearchForm",
  components: { EclButton },
  props: {
    modelValue: {
      type: String,
      required: false,
      default: "",
    },
    placeholder: {
      type: String,
      required: false,
      default: "Search",
    },
    helpText: {
      type: String,
      required: false,
      default: null,
    },
    method: {
      type: String,
      required: false,
      default: "GET",
    },
    inputName: {
      type: String,
      required: false,
      default: "q",
    },
  },
  emits: ["update:modelValue"],
  computed: {
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
    searchAction() {
      return this.$router.resolve({ name: "search" }).fullPath;
    },
  },
};
</script>

<style scoped></style>
