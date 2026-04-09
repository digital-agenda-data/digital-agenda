<template>
  <tbody class="ecl-table__body">
    <slot></slot>
  </tbody>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "EclTbody",
});
</script>
