<script>
import EUMapCompareCountries from "@/components/charts/eu-map/EUMapCompareCountries.vue";
import topologyUrl from "@/assets/topology/world.json?url";

export default {
  name: "WorldMapCompareCountries",
  extends: EUMapCompareCountries,
  computed: {
    topologyUrl() {
      return topologyUrl;
    },
    panningEnabled() {
      return true;
    },
    mapNavigationEnabled() {
      return true;
    },
    mapView() {
      return {
        center: [925227.9025912888, 4886916.560814883],
        zoom: -14.49,
      };
    },
    mapViewMobile() {
      return this.mapView;
    },
  },
};
</script>

<style scoped></style>
