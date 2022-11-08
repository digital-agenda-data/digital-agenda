<script>
import { mapActions } from "pinia";
import userStore from "@/stores/userStore";

export default {
  name: "App",
  mounted() {
    this.loadInitialData();
  },
  methods: {
    ...mapActions(userStore, ["getCurrentUser"]),
    async loadInitialData() {
      await Promise.all([this.getCurrentUser()]);
    },
  },
};
</script>

<template>
  <header>
    <nav>
      <router-link to="/">Home</router-link>
      <router-link to="/about">About</router-link>
    </nav>
  </header>
  <router-view />
</template>

<style scoped></style>
