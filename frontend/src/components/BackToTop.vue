<template>
  <div class="back-to-top" :class="{ hidden: !isVisible }">
    <ecl-button
      icon-only
      icon="arrow-up"
      variant="primary"
      title="Back to top"
      @click="backToTop"
    />
  </div>
</template>

<script>
import EclButton from "@/components/ecl/EclButton.vue";

export default {
  name: "BackToTop",
  components: { EclButton },

  data() {
    return {
      isVisible: false,
    };
  },

  mounted() {
    window.addEventListener("scroll", this.handleScroll);
  },

  beforeUnmount() {
    window.removeEventListener("scroll", this.handleScroll);
  },

  methods: {
    handleScroll() {
      this.isVisible = window.scrollY > window.innerHeight / 1.5;
    },

    backToTop() {
      if (this.$route.hash) {
        this.$router.replace({
          path: this.$route.path,
          query: this.$route.query,
          hash: "",
        });
      }

      document.getElementById("nav")?.scrollIntoView({
        behavior: "smooth",
      });
    },
  },
};
</script>

<style scoped lang="scss">
.back-to-top {
  position: fixed;
  bottom: 4rem;
  right: 4rem;
  z-index: 1000;

  opacity: 1;
  transition: opacity 0.2s ease;
}

.back-to-top.hidden {
  opacity: 0;
}

@media (max-width: 768px) {
  .back-to-top {
    bottom: 2rem;
    right: 2rem;
  }
}
</style>
