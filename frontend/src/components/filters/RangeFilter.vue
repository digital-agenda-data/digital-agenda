<template>
  <ecl-range :key="queryName" v-model="modelValue" :max="10" />
</template>

<script>
import EclRange from "@/components/ecl/forms/EclRange.vue";
import { useRouteQuery } from "@vueuse/router";

export default {
  name: "RangeFilter",
  components: { EclRange },
  props: {
    queryName: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      model: useRouteQuery(this.queryName),
    };
  },
  computed: {
    modelValue: {
      get() {
        return parseInt(this.model);
      },
      set(value) {
        this.model = value;
      },
    },
  },
};
</script>
