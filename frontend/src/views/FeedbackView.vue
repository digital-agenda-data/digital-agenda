<template>
  <form class="feedback-form" @submit.prevent="submitFeedback">
    <ecl-spinner v-if="loading" absolute centered />
    <ecl-text-field
      v-model="email"
      type="email"
      :required="false"
      input-name="email"
      label="Email address"
      placeholder-text="email@example.com"
      size="l"
      max-length="200"
      help-text="Provide your email address if you want to be contacted back"
      :errors="errors.email"
    />
    <ecl-text-area
      v-model="message"
      :required="true"
      input-name="message"
      label="Message"
      size="l"
      rows="20"
      min-length="10"
      max-length="10000"
      placeholder-text="Type in your message"
      :errors="errors.message"
    />
    <captcha-field ref="captchaField" :errors="errors.captcha" />
    <ecl-button label="Submit" type="submit" />
  </form>
</template>

<script>
import EclSpinner from "@/components/ecl/EclSpinner.vue";
import CaptchaField from "@/components/CaptchaField.vue";
import EclButton from "@/components/ecl/EclButton.vue";
import EclTextArea from "@/components/ecl/forms/EclTextArea.vue";
import EclTextField from "@/components/ecl/forms/EclTextField.vue";
import { api } from "@/lib/api";
import { useMessagesStore } from "@/stores/messagesStore";
import { mapActions } from "pinia";

export default {
  name: "FeedbackView",
  components: {
    EclSpinner,
    CaptchaField,
    EclButton,
    EclTextArea,
    EclTextField,
  },
  data() {
    return {
      loading: false,
      errors: {
        email: [],
        message: [],
        captcha: [],
        error: "",
      },
      email: "",
      message: "",
      captcha: null,
    };
  },
  methods: {
    ...mapActions(useMessagesStore, ["addMessage"]),
    getCaptcha() {
      const inputs = this.$refs.captchaField.$el.querySelectorAll("input");
      const result = {};
      for (const inputEl of inputs) {
        result[inputEl.name] = inputEl.value;
      }
      return result;
    },
    getPostData() {
      return {
        url: new URL(
          this.$router.options.history.state.back ?? "/",
          window.location,
        ).href,
        email: this.email,
        message: this.message,
        captcha: this.getCaptcha(),
      };
    },
    async submitFeedback() {
      try {
        this.loading = true;
        this.resetErrors();
        await api.post("/feedback/", this.getPostData());
        this.addMessage({
          id: "feedback-alert",
          type: "success",
          title: "Feedback message sent",
          description:
            "Your message has been sent. Thank you for your feedback!",
        });
        this.resetForm();
      } catch (e) {
        this.setErrors(e);
        this.addMessage({
          id: "feedback-alert",
          type: "error",
          title: "Unable to send feedback",
          description: (this.errors.error ?? []).join(","),
        });
      } finally {
        this.loading = false;
        // Regardless of result, reload the captcha, as the challenge
        // would have already been invalidated server side.
        window.$wt?.captcha.refresh();
      }
    },
    resetForm() {
      this.email = "";
      this.message = "";
    },
    resetErrors() {
      Object.keys(this.errors).forEach((key) => (this.errors[key] = []));
    },
    setErrors(error) {
      const reason = error.response.data;

      if (reason.details) {
        if (typeof reason.details === "string") {
          this.errors.error = [reason.details];
        } else {
          Object.entries(reason.details).forEach((entry) => {
            this.errors[entry[0]] = entry[1];
          });
        }
      } else if (reason.detail || reason.error) {
        this.errors.error = reason.detail || reason.error;
      } else if (typeof reason === "object") {
        Object.entries(reason).forEach(([key, messages]) => {
          this.errors[key] = messages;
        });
      } else {
        this.errors.error = ["Unknown error."];
      }
    },
  },
};
</script>

<style scoped>
.feedback-form {
  margin-top: 1rem;
}

.feedback-form > * + * {
  margin-top: 1rem;
}
</style>
