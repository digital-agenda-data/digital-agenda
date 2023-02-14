<template>
  <form class="feedback-form" @submit.prevent="submitFeedback">
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
    />
    <ecl-button label="Submit" type="submit" />
  </form>
</template>

<script>
import EclButton from "@/components/ecl/EclButton.vue";
import EclTextArea from "@/components/ecl/forms/EclTextArea.vue";
import EclTextField from "@/components/ecl/forms/EclTextField.vue";
import { api } from "@/lib/api";

export default {
  name: "FeedbackView",
  components: { EclButton, EclTextArea, EclTextField },
  data() {
    return {
      email: "",
      message: "",
    };
  },
  methods: {
    async submitFeedback() {
      const previousURL = new URL(
        this.$router.options.history.state.back,
        window.location
      ).href;

      await api.post("/feedback/", {
        url: previousURL,
        email: this.email,
        message: this.message,
      });
    },
  },
};
</script>

<style scoped>
.feedback-form {
  margin-top: 2rem;
}

.feedback-form > * + * {
  margin-top: 1rem;
}
</style>
