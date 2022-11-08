<script>
import userStore from "@/stores/userStore";

export default {
  name: "HomeView",
  computed: {
    userStore: () => userStore(),
  },
};
</script>

<template>
  <div>Current user {{ userStore.email }}</div>
</template>

<style scoped></style>
