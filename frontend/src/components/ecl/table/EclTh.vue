<template>
  <th class="ecl-table__header">
    <slot></slot>
  </th>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "EclTh",
});
</script>
