<template>
  <p>Home view</p>
  <p>
    Current user: <em>{{ userStore.email || "anonymous" }}</em>
  </p>
</template>
<script>
import userStore from "@/stores/userStore";

export default {
  name: "HomeView",
  computed: {
    userStore: () => userStore(),
  },
};
</script>

<style scoped></style>
