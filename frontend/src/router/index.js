import { createRouter, createWebHistory } from "vue-router";

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
  scrollBehavior(to) {
    if (to.hash) {
      return {
        el: to.hash,
      };
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
      path: "/search",
      name: "search",
      component: SearchView,
      meta: {
        title(route) {
          return `Search results for "${route.query.q || ""}"`;
        },
        breadcrumb: "Search",
      },
    },
    {
      path: "/chart-group/:chartGroupCode",
      name: "chart-group",
      component: DatasetView,
      redirect: {
        name: "home",
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
