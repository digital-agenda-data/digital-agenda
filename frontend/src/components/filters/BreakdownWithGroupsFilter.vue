<script>
import BaseSelectFilter from "@/components/filters/BaseSelectFilter.vue";
import { api } from "@/lib/api";

export default {
  name: "BreakdownWithGroupsFilter",
  extends: BaseSelectFilter,
  data() {
    return {
      breakdownGroups: [],
    };
  },
  computed: {
    queryName() {
      return "breakdown";
    },
    endpoint() {
      return (
        this.filterStore.indicator &&
        `/indicators/${this.filterStore.indicator.code}/breakdowns/`
      );
    },
    label() {
      return "Breakdown";
    },
    items() {
      const groups = new Map();

      for (const group of this.breakdownGroups) {
        groups.set(group.code, {
          id: group.code,
          text: this.getDisplay(group),
          children: [],
        });
      }

      for (const item of this.apiData) {
        for (const groupCode of item.groups) {
          const groupObject = groups.get(groupCode);

          if (!groupObject) {
            continue;
          }

          groupObject.children.push({
            id: item.code,
            text: this.getDisplay(item),
          });
        }
      }

      // Maps preserve order, so no sorting is required.
      return Array.from(groups.values());
    },
  },
  methods: {
    async loadExtra() {
      if (!this.filterStore.indicator) return;

      this.breakdownGroups = (
        await api.get(
          `/indicators/${this.filterStore.indicator.code}/breakdown-groups/`
        )
      ).data;
    },
  },
};
</script>
