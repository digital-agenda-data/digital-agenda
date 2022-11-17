import { createRouter, createWebHistory } from "vue-router";

import chartGroupStore from "@/stores/chartGroupStore";

import HomeView from "@/views/HomeView.vue";
import AboutView from "@/views/AboutView.vue";
import SearchView from "@/views/SearchView.vue";

import DatasetView from "@/views/DatasetView.vue";
import CommentsView from "@/views/datasets/CommentsView.vue";
import MetadataView from "@/views/datasets/MetadataView.vue";
import ChartListView from "@/views/datasets/ChartListView.vue";
import IndicatorView from "@/views/datasets/IndicatorView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
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
      path: "/datasets/:chartGroupCode",
      name: "datasets",
      component: DatasetView,
      redirect: {
        name: "home",
      },
      meta: {
        title(route) {
          return chartGroupStore().chartGroups.find(
            (item) => item.code === route.params.chartGroupCode
          )?.name;
        },
        breadcrumb(route) {
          return (
            chartGroupStore().chartGroups.find(
              (item) => item.code === route.params.chartGroupCode
            )?.short_name || "Datasets"
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
