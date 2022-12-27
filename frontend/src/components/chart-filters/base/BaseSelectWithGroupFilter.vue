<script>
import BaseSelectFilter from "@/components/chart-filters/base/BaseSelectFilter.vue";
import { api } from "@/lib/api";

export default {
  name: "BaseSelectWithGroupFilter",
  extends: BaseSelectFilter,
  data() {
    return {
      groups: [],
    };
  },
  computed: {
    groupEndpoint() {
      return this.errorMustImplement("groupEndpoint");
    },
    items() {
      const groups = new Map();

      for (const group of this.groups) {
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
      if (!this.groupEndpoint) return;

      this.groups = (await api.get(this.groupEndpoint)).data;
    },
  },
};
</script>
