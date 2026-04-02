<template>
  <div v-if="value">
    <b v-if="label">{{ label }}&nbsp;</b>
    <!-- eslint-disable-next-line vue/no-v-html -->
    <span class="dimension-prop" v-html="value" />
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "DimensionProp",
  props: {
    value: {
      type: String,
      required: false,
      default: null,
    },
    label: {
      type: String,
      required: false,
      default: "",
    },
  },
});
</script>

<style>
.dimension-prop > p:first-of-type {
  display: inline;
}
</style>
