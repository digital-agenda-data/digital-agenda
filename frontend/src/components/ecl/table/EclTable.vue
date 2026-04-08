<template>
  <table class="ecl-table" :class="{ 'ecl-table--zebra': zebra }">
    <slot></slot>
  </table>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "EclTable",
  props: {
    zebra: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
});
</script>
