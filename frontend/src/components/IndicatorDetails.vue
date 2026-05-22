<template>
  <h2
    :id="`indicator-group-${parent.code}`"
    :style="{ color: parent.colors[0] }"
  >
    <img v-if="parent.icon" :src="parent.icon" alt="" />
    <span>{{ parent.label || currentChartGroup.short_name }}</span>
  </h2>
  <div
    v-for="group in parent.members"
    :id="`indicator-group-${group.code}`"
    :key="group.code"
  >
    <h3 :style="{ color: parent.colors[0] }">
      <span>{{ group.label }}</span>
    </h3>
    <hr />
    <div
      v-for="indicator in group.indicators"
      :id="`indicator-${indicator.code}`"
      :key="indicator.code"
    >
      <h4>
        <span>
          <ecl-link
            :to="getChartLink(group, indicator)"
            :label="indicator.label"
            no-visited
            variant="brand"
          />
        </span>
      </h4>
      <div class="indicator-details">
        <p>
          <strong>Notation</strong>
          <br />
          <span>{{ indicator.code }}</span>
        </p>
        <p v-if="indicator.definition">
          <strong>Definition</strong>
          <br />
          <!-- eslint-disable-next-line vue/no-v-html -->
          <span v-html="indicator.definition" />
        </p>
        <p v-if="indicator.note">
          <strong>Notes</strong>
          <br />
          <!-- eslint-disable-next-line vue/no-v-html -->
          <span v-html="indicator.note" />
        </p>
        <p>
          <strong>Time coverage</strong>
          <br />
          <span v-if="indicator.time_coverage">
            {{ indicator.time_coverage }}
          </span>
        </p>
        <p v-if="indicator.data_sources.length > 0">
          <strong>Source</strong>
          <br />
          <template
            v-for="data_source in indicator.data_sources"
            :key="indicator.code + data_source"
          >
            <ecl-link
              v-if="dataSourceByCode.get(data_source)?.url"
              :to="dataSourceByCode.get(data_source)?.url"
              :label="dataSourceByCode.get(data_source)?.label"
              no-visited
            />
            <span v-else>
              {{ dataSourceByCode.get(data_source)?.label }}
            </span>
          </template>
        </p>
        <p>
          <strong>Export</strong>
          <br />
          <ecl-link
            :to="`${apiURL}/indicators/${indicator.code}/facts/`"
            no-visited
            download-class
            label="data"
          />
          <span>,&nbsp;</span>
          <ecl-link
            :to="`${apiURL}/countries/?indicator=${indicator.code}&format=csv`"
            no-visited
            download-class
            label="countries"
          />
          <span>,&nbsp;</span>
          <ecl-link
            :to="`${apiURL}/breakdowns/?indicator=${indicator.code}&format=csv`"
            no-visited
            download-class
            label="breakdowns"
          />
          <span>,&nbsp;</span>
          <ecl-link
            :to="`${apiURL}/units/?indicator=${indicator.code}&format=csv`"
            no-visited
            download-class
            label="units"
          />
        </p>
        <hr />
      </div>
    </div>
  </div>
</template>

<script>
import EclLink from "@/components/ecl/navigation/EclLink.vue";
import { apiURL } from "@/lib/api.js";
import { useChartGroupStore } from "@/stores/chartGroupStore.js";
import { useChartStore } from "@/stores/chartStore.js";
import { useDataSourceStore } from "@/stores/dataSourceStore.js";
import { mapState } from "pinia";

export default {
  name: "IndicatorDetails",
  components: { EclLink },
  props: {
    parent: {
      type: Object,
      required: false,
      default: null,
    },
  },
  data() {
    return {
      apiURL,
      collapsed: true,
    };
  },
  computed: {
    ...mapState(useChartGroupStore, ["currentChartGroup"]),
    ...mapState(useChartStore, ["defaultChartForCurrentGroup"]),
    ...mapState(useDataSourceStore, ["dataSourceByCode"]),
  },
  methods: {
    getChartLink(group, indicator) {
      return {
        name: "chart-view",
        params: {
          chartCode: this.defaultChartForCurrentGroup.code,
          chartGroupCode: this.currentChartGroup.code,
        },
        query: {
          indicator: indicator.code,
          // Specify the time period from the sample fact to ensure the link
          // works even when the indicator filter comes after the period
          period: indicator.sample_fact.period,
        },
      };
    },
  },
};
</script>

<style scoped lang="scss">
h2 {
  margin-top: 7.5rem !important;

  display: flex;
  align-items: center;
  gap: 0.5rem;

  img {
    height: 1.125rem;
  }

  span {
    font-size: 1.25rem;
    text-transform: uppercase;
    font-weight: 700;
    line-height: 1.5rem;
  }
}

h3 {
  margin-top: 7.5rem !important;
  margin-bottom: 1.5rem !important;

  span {
    font-weight: 300;
    font-size: 2.5rem;
    letter-spacing: 0.5px;
  }
}

h2 + div > h3 {
  margin-top: 0.625rem !important;
}

h4 {
  margin-top: 1.5rem !important;
  margin-bottom: 1.5rem !important;

  span {
    font-weight: 300;
    font-size: 1.75rem;
  }
}

.indicator-details {
  margin-left: 0.875rem;
  color: var(--cm-on-surface-brand);

  & > p {
    margin-bottom: 1.5rem;
  }

  hr {
    margin-top: 4rem !important;
    margin-bottom: 4rem !important;
  }
}
</style>
