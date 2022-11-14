<template>
  <p>No indicators found for "{{ searchQuery }}".</p>
</template>

<script>
export default {
  name: "SearchView",
  data() {
    return {
      searchQuery: this.$route.query.q,
    };
  },
  watch: {
    $route() {
      this.searchQuery = this.$route.query.q;
    },
  },
};
</script>

<style scoped></style>
