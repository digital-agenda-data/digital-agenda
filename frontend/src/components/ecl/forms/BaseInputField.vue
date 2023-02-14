<script>
/**
 * Base component for input fields
 */
export default {
  name: "BaseInputField",
  props: {
    modelValue: {
      type: String,
      required: false,
      default: "",
    },
    label: {
      type: String,
      required: false,
      default: null,
    },
    inputName: {
      type: String,
      required: false,
      default: "",
    },
    helpText: {
      type: String,
      required: false,
      default: null,
    },
    required: {
      type: Boolean,
      required: false,
      default: false,
    },
    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    errors: {
      type: Array,
      required: false,
      default: null,
    },
    minLength: {
      type: [Number, String],
      required: false,
      default: null,
    },
    maxLength: {
      type: [Number, String],
      required: false,
      default: null,
    },
    size: {
      type: String,
      required: false,
      default: null,
      validator(value) {
        return ["s", "m", "l"].includes(value);
      },
    },
    placeholderText: {
      type: String,
      required: false,
      default: "",
    },
  },
  emits: ["update:modelValue"],
  computed: {
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },
    className() {
      return this.errorMustImplement("className");
    },
    classList() {
      const result = [this.className, `${this.className}--${this.size}`];

      if (this.disabled) {
        result.push(`${this.className}--disabled`);
      }
      if (this.errors && this.errors.length > 0) {
        result.push(`${this.className}--invalid`);
      }

      return result;
    },
  },
};
</script>

<style scoped></style>
