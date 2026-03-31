<template>
  <footer id="footer" class="ecl-site-footer">
    <div class="ecl-site-footer__main">
      <div class="ecl-container ecl-site-footer__container">
        <ecl-site-footer-specific />
        <ecl-site-footer-common />
      </div>
    </div>
  </footer>
</template>

<script>
import EclSiteFooterCommon from "@/components/ecl/site-wide/EclSiteFooterCommon.vue";
import EclSiteFooterSpecific from "@/components/ecl/site-wide/EclSiteFooterSpecific.vue";

/**
 * ECL Site Footer component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/site-wide/site-footer/usage/
 *
 */
export default {
  name: "EclSiteFooter",
  components: {
    EclSiteFooterCommon,
    EclSiteFooterSpecific,
  },
};
</script>

<style scoped></style>
