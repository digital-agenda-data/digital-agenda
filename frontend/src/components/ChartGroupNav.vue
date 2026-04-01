<template>
  <div
    class="ecl-row ecl-u-pt-m ecl-u-d-flex"
    :class="`ecl-u-d-${mobileBreakpoint}-none`"
  >
    <div class="ecl-col-12">
      <ecl-tabs :items="navRoutes" hide-controls />
    </div>
  </div>

  <div class="ecl-row">
    <div class="ecl-col-12" :class="`ecl-col-${mobileBreakpoint}-8`">
      <slot></slot>
    </div>

    <div
      class="ecl-u-d-none ecl-col-4"
      :class="`ecl-u-d-${mobileBreakpoint}-flex`"
    >
      <div class="ecl-u-pa-xs">
        <h2>About this dataset</h2>
        <div class="ecl-u-pb-none ecl-u-bg-neutral-50 ecl-u-ph-xl ecl-u-pv-m">
          <ecl-list v-slot="{ item }" :items="navRoutes" divider>
            <ecl-link
              :to="item.to"
              :label="item.text"
              :variant="$route.name === item.to.name ? 'none' : 'standalone'"
            />
          </ecl-list>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import EclList from "@/components/ecl/EclList.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import EclTabs from "@/components/ecl/navigation/EclTabs.vue";

export default {
  name: "ChartGroupNav",
  components: { EclLink, EclList, EclTabs },
  data() {
    return {
      mobileBreakpoint: "l",
    };
  },
  computed: {
    navRoutes() {
      const params = {
        chartGroupCode: this.$route.params.chartGroupCode,
      };

      return [
        {
          id: "charts",
          text: "Charts",
          to: { name: "charts", params },
        },
        {
          id: "indicators",
          text: "Indicators",
          to: { name: "indicators", params },
        },
        {
          id: "metadata",
          text: "Metadata",
          to: { name: "metadata", params },
        },
        {
          id: "feedback",
          text: "Submit feedback",
          to: { name: "feedback" },
        },
      ];
    },
  },
};
</script>

<style scoped></style>
