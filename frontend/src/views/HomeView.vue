<template>
  <ecl-list-illustration :items="items" zebra>
    <template #description="{ item }">
      <div v-html="item.description" />

      <ul>
        <li>
          <ecl-link
            no-visited
            :to="{
              name: 'indicators',
              params: {
                chartGroupCode: item.id,
              },
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
              params: {
                chartGroupCode: item.id,
              },
            }"
          >
            Entire dataset metadata and download services
          </ecl-link>
        </li>
      </ul>
    </template>
  </ecl-list-illustration>
</template>

<script>
import placeholderImageURL from "@/assets/placeholder.png?url";
import chartGroupStore from "@/stores/chartGroupStore";
import EclListIllustration from "@/components/ecl/EclListIllustration.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";

export default {
  name: "HomeView",
  components: { EclLink, EclListIllustration },
  computed: {
    chartGroupStore: () => chartGroupStore(),
    items() {
      return this.chartGroupStore.chartGroups.map((chartGroup) => {
        return {
          id: chartGroup.code,
          title: chartGroup.name,
          image: chartGroup.image || placeholderImageURL,
          description: chartGroup.description,
          to: {
            name: "charts",
            params: {
              chartGroupCode: chartGroup.code,
            },
          },
        };
      });
    },
  },
};
</script>

<style scoped></style>
