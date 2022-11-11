<template>
  <div>
    <p>
      Current user: <em>{{ userStore.email || "anonymous" }}</em>
    </p>
    <ol>
      <li v-for="dataset in datasetsStore.datasets" :key="dataset.code">
        <ecl-link
          :to="{
            name: 'charts',
            params: {
              datasetId: dataset.code,
            },
          }"
        >
          {{ dataset.name }}
        </ecl-link>
        <p>
        {{ dataset.description }}
        </p>
      </li>
    </ol>
  </div>
</template>
<script>
import userStore from "@/stores/userStore";
import datasetsStore from "@/stores/datasetsStore";
import EclLink from "@/components/ecl/navigation/EclLink.vue";

export default {
  name: "HomeView",
  components: { EclLink },
  computed: {
    userStore: () => userStore(),
    datasetsStore: () => datasetsStore(),
  },
};
</script>

<style scoped></style>
