<template>
  <div>
    <router-view />

    <ul>
      <li v-for="item in navRoutes" :key="item">
        <ecl-link
          :to="{ name: item, params: $route.params }"
          :label="item"
          no-visited
        />
      </li>
    </ul>
  </div>
</template>

<script>
import EclLink from "@/components/ecl/navigation/EclLink.vue";
export default {
  name: "DatasetView",
  components: { EclLink },
  computed: {
    navRoutes() {
      return ["charts", "indicators", "metadata", "comments"];
    },
  },
};
</script>

<style scoped></style>
