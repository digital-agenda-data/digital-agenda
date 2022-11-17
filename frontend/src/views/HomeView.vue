<template>
  <div>
    <p>
      Current user: <em>{{ userStore.email || "anonymous" }}</em>
    </p>
    <ol>
      <li v-for="dataset in chartGroupStore.chartGroups" :key="dataset.code">
        <ecl-link
          :to="{
            name: 'charts',
            params: {
              chartGroupCode: dataset.code,
            },
          }"
          no-visited
        >
          {{ dataset.name }}
        </ecl-link>
        <p v-html="dataset.description" />
      </li>
    </ol>
  </div>
</template>
<script>
import userStore from "@/stores/userStore";
import chartGroupStore from "@/stores/chartGroupStore";
import EclLink from "@/components/ecl/navigation/EclLink.vue";

export default {
  name: "HomeView",
  components: { EclLink },
  computed: {
    userStore: () => userStore(),
    chartGroupStore: () => chartGroupStore(),
  },
};
</script>

<style scoped></style>
