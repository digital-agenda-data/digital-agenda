<template>
  <ul>
    <li>
      <ecl-link
        no-visited
        :to="{
          name: 'indicators',
          params: { chartGroupCode },
        }"
      >
        Consult the list of indicators, their definition and sources
      </ecl-link>
    </li>
    <li>
      <ecl-link
        no-visited
        :to="{
          name: 'metadata',
          params: { chartGroupCode },
        }"
      >
        Entire dataset metadata and download services
      </ecl-link>
    </li>
  </ul>
</template>

<script>
import EclLink from "@/components/ecl/navigation/EclLink.vue";

export default {
  name: "ChartGroupExtraLinks",
  components: { EclLink },
  props: {
    chartGroupCode: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped></style>
