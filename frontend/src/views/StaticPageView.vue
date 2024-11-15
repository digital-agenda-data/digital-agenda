<template>
  <!-- eslint-disable-next-line vue/no-v-html -->
  <div v-html="currentStaticPage.body" />
</template>

<script>
import { useStaticPageStore } from "@/stores/staticPageStore";
import { mapState } from "pinia";

export default {
  name: "StaticPageView",
  computed: {
    ...mapState(useStaticPageStore, ["currentStaticPage"]),
  },
};
</script>

<style scoped></style>
