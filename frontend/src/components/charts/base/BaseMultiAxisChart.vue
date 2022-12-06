<script>
import BaseChart from "@/components/charts/base/BaseChart.vue";

export default {
  name: "BaseMultiAxisChart",
  extends: BaseChart,
  computed: {
    tooltip() {
      const parent = this;
      return {
        formatter() {
          const result = [
            `<b>${this.series.name}</b>`,
            parent.getAxisValueDisplay(this.point.x, "X"),
            parent.getAxisValueDisplay(this.point.y, "Y"),
            parent.getAxisValueDisplay(this.point.z, "Z"),
          ];

          return result.filter((value) => !!value).join("<br/>");
        },
      };
    },
  },
  methods: {
    getAxisValueDisplay(value, axis) {
      const unit = this.filterStore[axis].unit;
      if (value === undefined || !unit) return;

      return `<b>${axis}:&nbsp;</b>${this.getUnitDisplay(value, unit)}`;
    },
  },
};
</script>
