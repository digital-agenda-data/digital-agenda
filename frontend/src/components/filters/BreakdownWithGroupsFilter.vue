<script>
import BaseSelectFilter from "@/components/filters/BaseSelectFilter.vue";
import { apiCall } from "@/lib/api";

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
        this.$route.query.indicator &&
        `/indicators/${this.$route.query.indicator}/breakdowns/`
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
          text: group.alt_label || group.label || group.code,
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
            text: item.alt_label || item.label || item.code,
          });
        }
      }

      // Maps preserve order, so no sorting is required.
      return Array.from(groups.values());
    },
  },
  methods: {
    async loadExtra() {
      if (!this.$route.query.indicator) return;

      this.breakdownGroups = await apiCall(
        "GET",
        `/indicators/${this.$route.query.indicator}/breakdown-groups/`
      );
    },
  },
};
</script>
