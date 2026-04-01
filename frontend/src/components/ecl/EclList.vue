<template>
  <component :is="ordered ? 'ol' : 'ul'" :class="classList">
    <li v-for="item in items" :key="item.id" :class="itemClassList">
      <slot :item="item">
        {{ item.label }}
      </slot>
    </li>
  </component>
</template>

<script>
/**
 * ECL Label component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/list/usage/
 *
 */
export default {
  name: "EclList",
  props: {
    ordered: {
      type: Boolean,
      required: false,
      default: false,
    },
    divider: {
      type: Boolean,
      required: false,
      default: false,
    },
    items: {
      type: Array,
      required: true,
    },
  },
  computed: {
    mainClass() {
      return this.ordered ? "ecl-ordered-list" : "ecl-unordered-list";
    },
    classList() {
      const result = [this.mainClass];
      if (this.divider) {
        result.push(`${this.mainClass}--divider`);
      }
      return result;
    },
    itemClassList() {
      return [`${this.mainClass}__item`, "ecl-u-pl-none", "ecl-u-pb-l"];
    },
  },
};
</script>

<style scoped></style>
