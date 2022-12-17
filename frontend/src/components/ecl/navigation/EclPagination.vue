<template>
  <nav v-if="totalPages > 1" class="ecl-pagination" aria-label="Pagination">
    <ul class="ecl-pagination__list">
      <li class="ecl-pagination__item ecl-pagination__item--previous">
        <ecl-link
          v-visible="currentPage > 1"
          :to="getRoute(currentPage - 1)"
          label="Previous"
          icon="corner-arrow"
          icon-rotate="270"
          class="ecl-pagination__link"
          icon-left
          no-visited
        />
      </li>
      <li
        v-for="i in pages"
        :key="i"
        class="ecl-pagination__item"
        :class="{ 'ecl-pagination__item--current': i === currentPage }"
      >
        <ecl-link
          v-if="i !== currentPage"
          :to="getRoute(i)"
          :label="i.toString()"
          :aria-label="`Go to page ${i}`"
          class="ecl-pagination__link"
          no-visited
        />
        <template v-else>
          <span
            class="ecl-pagination__text ecl-pagination__text--summary"
            aria-current="true"
          >
            {{ i }}
          </span>
          <span
            class="ecl-pagination__text ecl-pagination__text--full"
            aria-current="true"
          >
            Page {{ i }}
          </span>
        </template>
      </li>
      <li class="ecl-pagination__item ecl-pagination__item--next">
        <ecl-link
          v-visible="currentPage < totalPages"
          :to="getRoute(currentPage + 1)"
          label="Next"
          icon="corner-arrow"
          icon-rotate="90"
          class="ecl-pagination__link"
          icon-left
          no-visited
        />
      </li>
    </ul>
  </nav>
</template>

<script>
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import { useRouteQuery } from "@vueuse/router";
import { clamp, range } from "@/lib/utils";

/**
 * ECL Pagination component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/navigation/pagination/usage/
 */
export default {
  name: "EclPagination",
  components: { EclLink },
  props: {
    // Total number of results
    total: {
      type: Number,
      required: true,
    },
    // Number of results on a single page
    pageSize: {
      type: Number,
      required: true,
    },
    // Number of maximum pages to display
    totalVisible: {
      type: Number,
      required: false,
      default: 5,
      validator(value) {
        return value > 0;
      },
    },
    queryName: {
      type: String,
      required: false,
      default: "page",
    },
  },
  data() {
    return {
      page: useRouteQuery(this.queryName),
    };
  },
  computed: {
    currentPage() {
      return parseInt(this.page ?? "1");
    },
    totalPages() {
      return Math.ceil(this.total / this.pageSize);
    },
    pages() {
      let start, end;
      const maxLeftSide = Math.floor(this.totalVisible / 2);
      const maxRightSide = Math.ceil(this.totalVisible / 2) - 1;

      if (this.currentPage <= maxLeftSide) {
        // Current page is the first few pages
        start = 1;
        end = this.totalVisible;
      } else if (this.currentPage + maxRightSide >= this.totalPages) {
        // Current page is the last few pages
        start = this.totalPages - this.totalVisible + 1;
        end = this.totalPages;
      } else {
        // Everything else
        start = this.currentPage - maxLeftSide;
        end = this.currentPage + maxRightSide;
      }

      // Make sure we don't exceed limits
      start = clamp(start, 1, this.totalPages);
      end = clamp(end, 1, this.totalPages);

      return range(start, end + 1);
    },
  },
  methods: {
    getRoute(page) {
      return {
        query: {
          ...this.$route.query,
          page,
        },
      };
    },
  },
};
</script>

<style scoped></style>
