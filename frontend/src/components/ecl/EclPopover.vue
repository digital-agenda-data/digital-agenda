<template>
  <div
    v-ecl-init="{
      attachClickListener: !manualControl,
      attachKeyListener: !manualControl,
    }"
    class="ecl-popover"
    data-ecl-auto-init="Popover"
  >
    <div
      class="ecl-popover__toggle"
      :aria-controls="contentId"
      data-ecl-popover-toggle=""
      :aria-expanded="manualControl ? undefined : 'false'"
      :role="manualControl ? undefined : 'button'"
      aria-label="Popover toggle"
    >
      <slot name="toggle"></slot>
    </div>

    <div :id="contentId" class="ecl-popover__container" hidden="">
      <div class="ecl-popover__content">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
/**
 * ECL Popover component, see documentation here:
 *
 *  https://ec.europa.eu/component-library/ec/components/popover/usage/
 *
 */
export default {
  name: "EclPopover",
  props: {
    /**
     * Disable the default click listener and toggle the popover manually
     * using openPopover and closePopover functions.
     */
    manualControl: {
      type: Boolean,
      required: false,
      default: false,
    },
    contentId: {
      type: String,
      required: true,
    },
  },
  computed: {},
  methods: {
    openPopover() {
      this.$el.ECLPopover.openPopover();
    },
    closePopover() {
      this.$el.ECLPopover.closePopover();
    },
  },
};
</script>

<style scoped></style>
