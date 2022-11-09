<template>
  <div>Current user {{ userStore.email }}</div>
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
