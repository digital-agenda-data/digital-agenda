import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AboutView from "@/views/AboutView.vue";
import DatasetView from "@/views/DatasetView.vue";
import ChartListView from "@/views/datasets/ChartListView.vue";
import IndicatorView from "@/views/datasets/IndicatorView.vue";
import MetadataView from "@/views/datasets/MetadataView.vue";
import datasetsStore from "@/stores/datasetsStore";
import SearchView from "@/views/SearchView.vue";

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
      path: "/datasets/:datasetId",
      component: DatasetView,
      name: "datasets",
      redirect: {
        name: "home",
      },
      meta: {
        title(route) {
          return datasetsStore().datasets.find(
            (item) => item.code === route.params.datasetId
          )?.name;
        },
        breadcrumb(route) {
          return (
            datasetsStore().datasets.find(
              (item) => item.code === route.params.datasetId
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
      ],
    },
  ],
});

export default router;
