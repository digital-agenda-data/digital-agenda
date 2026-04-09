<template>
  <tr class="ecl-table__row">
    <slot></slot>
  </tr>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "EclTr",
});
</script>
