<script>
import userStore from "@/stores/userStore";
import EclIcon from "@/components/ecl/EclIcon.vue";

export default {
  name: "HomeView",
  components: { EclIcon },
  computed: {
    userStore: () => userStore(),
  },
};
</script>

<template>
  <div>
    Current user {{ userStore.email }}
    <ecl-icon icon="hamburger" />
    <ecl-icon icon="hamburger" color="primary" />
    <ecl-icon icon="growth" size="2xl" />
    <ecl-icon icon="growth" size="xl" />
    <ecl-icon icon="growth" size="l" />
    <ecl-icon icon="growth" size="m" />
    <ecl-icon icon="growth" size="s" />
    <ecl-icon icon="growth" size="xs" />
    <ecl-icon icon="growth" size="2xs" />

    <ecl-icon icon="corner-arrow" rotate="0" />
    <ecl-icon icon="corner-arrow" rotate="90" />
    <ecl-icon icon="corner-arrow" rotate="180" />
    <ecl-icon icon="corner-arrow" rotate="270" />

    <ecl-icon icon="rss" />
    <ecl-icon icon="rss" flip-horizontal />
    <ecl-icon icon="rss" flip-vertical />
    <ecl-icon icon="rss" flip-horizontal flip-vertical />
  </div>
</template>

<style scoped></style>
