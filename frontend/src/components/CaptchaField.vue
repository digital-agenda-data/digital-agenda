<template>
  <ecl-form-group label="Captcha" required :errors="errors">
    <div v-ec-wt-render="{ service: 'captcha' }" />
  </ecl-form-group>
</template>

<script>
import EclFormGroup from "@/components/ecl/forms/EclFormGroup.vue";

/**
 * EU Captcha Field
 *
 * See https://webgate.ec.europa.eu/fpfis/wikis/display/webtools/Sliding+Captcha for details.
 */
export default {
  name: "CaptchaField",
  components: { EclFormGroup },
  props: {
    errors: {
      type: Array,
      required: false,
      default: null,
    },
  },
};
</script>

<style scoped></style>
