<script>
import BaseSelectFilter from "@/components/chart-filters/base/BaseSelectFilter.vue";
import { api } from "@/lib/api";
import { groupByUnique } from "@/lib/utils";

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
    ignoredGroupCodes() {
      return new Set(
        this.currentFilterOptions.ignored[this.queryName + "Group"],
      );
    },
    apiDataByCode() {
      return groupByUnique(this.apiData);
    },
    items() {
      const result = [];

      for (const group of this.groups ?? []) {
        const children = [];

        if (this.ignoredGroupCodes.has(group.code)) {
          continue;
        }

        for (const code of group.members) {
          const item = this.apiDataByCode.get(code);
          if (item) {
            children.push({
              id: item.code,
              text: item.display,
            });
          }
        }

        if (children.length > 0) {
          result.push({
            id: group.code,
            text: group.display,
            children,
          });
        }
      }

      return result;
    },
  },
  methods: {
    async loadExtra() {
      this.groups = (
        await api.get(this.groupEndpoint, {
          params: this.mergedEndpointParams,
        })
      ).data;
    },
  },
};
</script>
