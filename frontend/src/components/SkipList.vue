<template>
  <ul class="skip">
    <li v-for="item in skipList" :key="item.id">
      <a :href="`#${item.id}`">{{ item.label }}</a>
    </li>
  </ul>
</template>

<script>
export default {
  name: "SkipList",
  data() {
    return {
      skipList: [
        { id: "main", label: "Jump to main content" },
        { id: "header", label: "Jump to header" },
        { id: "nav", label: "Jump to navigation" },
        { id: "footer", label: "Jump to footer" },
      ],
    };
  },
};
</script>

<style scoped>
.skip {
  margin: 0;
  padding: 0;
}

.skip li {
  list-style: none;
}

.skip li a {
  position: absolute;
  top: -200rem;
  left: -200rem;
  padding: 1rem;
  background-color: white;
  z-index: 9999;
}

.skip li a:focus {
  top: 0;
  left: 0;
}
</style>
