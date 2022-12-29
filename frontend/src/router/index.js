import { createRouter, createWebHistory, useRoute } from "vue-router";

import { useChartStore } from "@/stores/chartStore";
import { useChartGroupStore } from "@/stores/chartGroupStore";

import HomeView from "@/views/HomeView.vue";
import AboutView from "@/views/AboutView.vue";
import SearchView from "@/views/SearchView.vue";

import DatasetView from "@/views/DatasetView.vue";
import CommentsView from "@/views/chart-group/CommentsView.vue";
import MetadataView from "@/views/chart-group/MetadataView.vue";
import ChartListView from "@/views/chart-group/ChartListView.vue";
import IndicatorView from "@/views/chart-group/IndicatorView.vue";
import ChartView from "@/views/chart-group/ChartView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return { el: to.hash };
    }

    if (savedPosition) {
      return savedPosition;
    }

    if (to.path !== from.path) {
      return { top: 0 };
    }
  },
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "about",
      component: AboutView,
      meta: {
        title: "About data visualisation tool",
        breadcrumb: "About data visualisation tool",
      },
    },
    {
      path: "/search/:page?",
      name: "search",
      component: SearchView,
      meta: {
        title() {
          return `Search results for "${useRoute()?.query?.q || ""}"`;
        },
        breadcrumb: "Search",
      },
    },
    {
      path: "/chart-group/:chartGroupCode",
      name: "chart-group",
      component: DatasetView,
      redirect: {
        // Default view for chart-groups
        name: "charts",
      },
      meta: {
        title() {
          return useChartGroupStore().currentChartGroup?.name;
        },
        breadcrumb() {
          return (
            useChartGroupStore().currentChartGroup?.short_name || "Datasets"
          );
        },
      },
      children: [
        {
          path: "charts",
          name: "charts",
          component: ChartListView,
          meta: {
            breadcrumb: "Charts",
          },
          children: [
            {
              path: ":chartCode",
              name: "chart-view",
              component: ChartView,
              meta: {
                title() {
                  return useChartStore().currentChart?.name;
                },
                breadcrumb() {
                  return useChartStore().currentChart?.name;
                },
              },
            },
          ],
        },
        {
          path: "indicators",
          name: "indicators",
          component: IndicatorView,
          meta: {
            breadcrumb: "Indicators",
          },
        },
        {
          path: "metadata",
          name: "metadata",
          component: MetadataView,
          meta: {
            breadcrumb: "Metadata",
          },
        },
        {
          path: "comments",
          name: "comments",
          component: CommentsView,
          meta: {
            breadcrumb: "Comments",
          },
        },
      ],
    },
  ],
});

export default router;
