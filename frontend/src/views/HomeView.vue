<template>
  <p>Home view</p>
  <p>
    Current user: <em>{{ userStore.email || "anonymous" }}</em>
  </p>
  {{ m1 }}
  <br />
  {{ m2 }}
  <ecl-select v-model="m1" :items="items" size="l" multiple />
  <ecl-select v-model="m2" :items="items" size="m" required />
</template>

<script>
import userStore from "@/stores/userStore";
import EclSelect from "@/components/ecl/forms/EclSelect.vue";

export default {
  name: "HomeView",
  components: { EclSelect },
  data() {
    return {
      m1: ["el5", "el1"],
      m2: "el5",
    };
  },
  computed: {
    userStore: () => userStore(),
    items() {
      return [
        {
          id: "el0",
          text: "Element 0",
        },
        {
          id: "group1",
          text: "Group 1",
          children: [
            { id: "el1", text: "Element 1" },
            { id: "el2", text: "Element 2", disabled: true },
          ],
        },
        {
          id: "group2",
          text: "Group 1",
          disabled: true,
          children: [
            { id: "el3", text: "Element 3" },
            { id: "el4", text: "Element 4" },
          ],
        },
        {
          id: "el5",
          text: "Element 5",
        },
      ];
    },
  },
};
</script>

<style scoped></style>
