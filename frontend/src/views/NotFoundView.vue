<template>
  <div class="ecl-u-mt-l">
    <span>We can't find what you are looking for.</span>
    <span>&nbsp;</span>
    <ecl-link
      :to="{ name: 'search' }"
      no-visited
      label="Click here to go the search page"
    />
  </div>
</template>

<script>
import EclLink from "@/components/ecl/navigation/EclLink.vue";

export default {
  name: "NotFoundView",
  components: { EclLink },
};
</script>

<style scoped></style>
