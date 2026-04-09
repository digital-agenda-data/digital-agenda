<template>
  <tfoot class="ecl-table__foot">
    <slot></slot>
  </tfoot>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "EclTFoot",
});
</script>
