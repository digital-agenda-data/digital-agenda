<template>
  <ecl-range :key="queryName" v-model="modelValue" :max="10" />
</template>

<script>
import EclRange from "@/components/ecl/forms/EclRange.vue";

export default {
  name: "RangeFilter",
  components: { EclRange },
  props: {
    queryName: {
      type: String,
      required: true,
    },
  },
  computed: {
    modelValue: {
      get() {
        return parseInt(this.$route.query[this.queryName]);
      },
      set(value) {
        const query = {
          ...this.$route.query,
          [this.queryName]: value.toString(),
        };
        this.$router.replace({ query });
      },
    },
  },
};
</script>
