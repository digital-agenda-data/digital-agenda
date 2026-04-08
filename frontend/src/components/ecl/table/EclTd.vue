<template>
  <td class="ecl-table__cell" :data-ecl-table-header="header">
    <slot></slot>
  </td>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "EclTd",
  props: {
    header: {
      type: String,
      required: false,
      default: "",
    },
  },
});
</script>
