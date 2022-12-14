<template>
  <ecl-list-illustration
    :items="items"
    :loading="chartGroupStore.isLoading"
    zebra
  >
    <template #description="{ item }">
      <div class="ecl-u-type-align-justify" v-html="item.description" />

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
import EclListIllustration from "@/components/ecl/EclListIllustration.vue";
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import { useChartGroupStore } from "@/stores/chartGroupStore";
import { mapStores } from "pinia";

export default {
  name: "HomeView",
  components: { EclLink, EclListIllustration },
  computed: {
    ...mapStores(useChartGroupStore),
    items() {
      return this.chartGroupStore.chartGroupList.map((chartGroup, index) => {
        return {
          id: chartGroup.code,
          title: `${index + 1}. ${chartGroup.name}`,
          image: chartGroup.image || placeholderImageURL,
          description: chartGroup.description,
          to: {
            name: "charts",
            params: {
              chartGroupCode: chartGroup.code,
            },
          },
          label: chartGroup.is_draft ? "draft" : null,
          labelVariant: "high",
        };
      });
    },
  },
};
</script>

<style scoped></style>
