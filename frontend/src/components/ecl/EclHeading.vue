<template>
  <div :class="`ecl-u-type-heading-${size}`">
    {{ text }}
  </div>
</template>

<script>
export default {
  name: "EclHeading",
  props: {
    size: {
      type: [String, Number],
      required: false,
      default: "1",
      validator(value) {
        return ["1", "2", "3", "4", "5"].includes(value.toString());
      },
    },
    text: {
      type: String,
      required: false,
      default: "",
    },
  },
};
</script>

<style scoped></style>
