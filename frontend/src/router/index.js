import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import AboutView from "@/views/AboutView.vue";
import DatasetView from "@/views/DatasetView.vue";
import ChartListView from "@/views/datasets/ChartListView.vue";
import IndicatorView from "@/views/datasets/IndicatorView.vue";
import MetadataView from "@/views/datasets/MetadataView.vue";
import datasetsStore from "@/stores/datasetsStore";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: {
        name: "home",
      },
    },
    {
      path: "/about",
      name: "about",
      component: AboutView,
      meta: {
        name: "About data visualisation tool",
      },
    },
    {
      path: "/datasets/:datasetId",
      name: "datasets",
      component: DatasetView,
      meta: {
        name() {
          const datasetId = this.$route.params.datasetId;
          return datasetsStore().datasets.find(
            (item) => item.code === datasetId
          ).short_name;
        },
      },
      children: [
        {
          path: "charts",
          name: "charts",
          component: ChartListView,
          meta: {
            name: "charts",
          },
        },
        {
          path: "indicators",
          name: "indicators",
          component: IndicatorView,
          meta: {
            name: "indicators",
          },
        },
        {
          path: "",
          alias: "metadata",
          name: "metadata",
          component: MetadataView,
          meta: {
            name: "metadata",
          },
        },
      ],
    },
  ],
});

export default router;
