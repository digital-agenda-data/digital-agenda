<template>
  <thead class="ecl-table__head">
    <slot></slot>
  </thead>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "EclThead",
});
</script>
