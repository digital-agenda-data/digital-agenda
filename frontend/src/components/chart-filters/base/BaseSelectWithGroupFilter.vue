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
    apiDataByCode() {
      return groupByUnique(this.apiData);
    },
    items() {
      const result = [];

      for (const group of this.groups ?? []) {
        const children = [];

        for (const code of group.members) {
          const item = this.apiDataByCode.get(code);
          if (item) {
            children.push({
              id: item.code,
              text: item.display,
            });
          }
        }

        result.push({
          id: group.code,
          text: group.display,
          children,
        });
      }

      return result;
    },
  },
  methods: {
    async loadExtra() {
      this.groups = (
        await api.get(this.groupEndpoint, {
          params: this.endpointParams,
        })
      ).data;
    },
  },
};
</script>
