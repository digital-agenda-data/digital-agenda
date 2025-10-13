<template>
  <div class="card-nav">
    <router-link
      v-for="item in items"
      :key="item.id"
      :to="item.to"
      class="card-nav-item"
      active-class="card-nav-item-active"
      :aria-label="item.title"
      :aria-describedby="
        item.plaintextDescription && `card-nav-description-${item.id}`
      "
      :title="item.plaintextDescription"
    >
      <ecl-card :image="item.image" :title="item.title" :labels="item.label" />
      <div
        v-if="item.plaintextDescription"
        :id="`card-nav-description-${item.id}`"
        class="ecl-u-d-none"
        hidden
      >
        {{ item.plaintextDescription }}
      </div>
    </router-link>
  </div>
</template>

<script>
import EclCard from "@/components/ecl/EclCard.vue";

/**
 * Grid navigation using EclCard components.
 */
export default {
  name: "CardNav",
  components: { EclCard },
  props: {
    /**
     * Items must be in the following format:
     *
     *   {
     *     id: '',                    // unique ID for this item
     *     title: '',                 // text to use in the title
     *     to: {},                    // router link for this item
     *     image: '',                 // image url for this item
     *     label: '',                 // (optional) add a label to the item
     *     plaintextDescription: '',  // (optional) add a tooltip for the item
     *   }
     */
    items: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped lang="scss">
.card-nav {
  display: grid;
  grid-gap: 1rem;
  grid-template-columns: repeat(1, 1fr);
}

@media screen and (min-width: 375px) {
  .card-nav {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media screen and (min-width: 768px) {
  .card-nav {
    grid-gap: 2rem;
    grid-template-columns: repeat(3, 1fr);
  }
}

@media screen and (min-width: 996px) {
  .card-nav {
    grid-template-columns: repeat(4, 1fr);
  }
}

.card-nav-item {
  box-sizing: border-box;
  text-decoration: none !important;
  text-align: center;
  border: 3px solid transparent;
}

.card-nav-item-active {
  pointer-events: none;
}

.card-nav-item-active,
.card-nav-item:hover {
  .ecl-card {
    background-color: var(--ecl-color-neutral-60);;
  }
}
</style>
