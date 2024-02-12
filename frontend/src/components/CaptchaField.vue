<template>
  <ecl-form-group
    label="Captcha"
    required
    help-text="Rotate the image so it is pointing up"
    :errors="errors"
  >
    <div class="captcha-field ecl-u-bg-grey-10">
      <div>
        <input type="hidden" :value="id" name="captchaId" />
        <input type="hidden" :value="token" name="captchaToken" />
      </div>
      <div class="captcha-img">
        <ecl-spinner v-if="loading" centered />
        <img
          v-else-if="captchaImg"
          :src="`data:image/png;base64,${captchaImg}`"
          alt="Captcha Image"
          :style="`transform: rotate(${rotate}deg)`"
        />
      </div>
      <div class="ecl-u-align-self-start">
        <ecl-button
          type="button"
          variant="ghost"
          label="Reload"
          aria-label="reload captcha image"
          @click="reloadCaptchaImg"
        />
      </div>
      <ecl-button
        type="button"
        variant="ghost"
        icon="solid-arrow"
        icon-rotate="270"
        icon-size="2xl"
        aria-label="decrease rotation"
        @click="turnImage(-1)"
      />
      <ecl-range
        v-model="rotate"
        :min="-360"
        :max="360"
        :step="stepDegree"
        class="ecl-u-width-100"
        input-name="captchaAnswer"
      />
      <ecl-button
        type="button"
        variant="ghost"
        icon="solid-arrow"
        icon-rotate="90"
        icon-size="2xl"
        aria-label="increase rotation"
        @click="turnImage(1)"
      />
    </div>
  </ecl-form-group>
</template>

<script>
import axios from "axios";

import EclButton from "@/components/ecl/EclButton.vue";
import EclSpinner from "@/components/ecl/EclSpinner.vue";
import EclFormGroup from "@/components/ecl/forms/EclFormGroup.vue";
import EclRange from "@/components/ecl/forms/EclRange.vue";
import { clamp } from "@/lib/utils";

const JWT_HEADER = "x-jwtString";

export const captchaApi = axios.create({
  baseURL: "https://api.eucaptcha.eu/api",
  withCredentials: true,
  params: {
    locale: "en-GB",
    captchaType: "WHATS_UP",
  },
});

/**
 * EU Captcha Field
 *
 * See https://wikis.ec.europa.eu/display/WEBGUIDE/09.+EU+CAPTCHA for details.
 */
export default {
  name: "CaptchaField",
  components: { EclButton, EclRange, EclFormGroup, EclSpinner },
  props: {
    modelValue: {
      type: Object,
      required: false,
      default: null,
    },
    errors: {
      type: Array,
      required: false,
      default: null,
    },
  },
  emits: ["update:modelValue"],
  data() {
    return {
      loading: false,
      id: this.modelValue?.id,
      rotate: this.modelValue?.answer ?? 0,
      token: this.modelValue?.token,
      stepDegree: null,
      captchaImg: null,
    };
  },
  computed: {
    captcha() {
      return {
        id: this.id,
        answer: this.rotate ?? 0,
        token: this.token,
      };
    },
  },
  watch: {
    captcha(newValue) {
      this.$emit("update:modelValue", newValue);
    },
  },
  mounted() {
    this.getCaptchaImg();
  },
  methods: {
    parseResponse(resp) {
      this.token = resp.headers.get(JWT_HEADER);
      this.id = resp.data.captchaId;
      this.captchaImg = resp.data.captchaImg;
      this.stepDegree = resp.data.degree;
    },
    async getCaptchaImg() {
      this.loading = true;
      try {
        this.parseResponse(await captchaApi.get("/captchaImg"));
      } finally {
        this.loading = false;
      }
    },
    async reloadCaptchaImg() {
      this.loading = true;
      this.rotate = 0;

      try {
        this.parseResponse(
          await captchaApi.get(`/reloadCaptchaImg/${this.id}`, {
            headers: {
              [JWT_HEADER]: this.token,
            },
          }),
        );
      } finally {
        this.loading = false;
      }
    },
    turnImage(stepDirection) {
      this.rotate = clamp(
        parseInt(this.rotate) + stepDirection * this.stepDegree,
        -360,
        360,
      );
    },
  },
};
</script>

<style scoped>
.captcha-field {
  padding-top: 1.5rem;
  display: grid;
  align-items: center;
  justify-items: center;
  grid-auto-flow: dense;
  grid-template-columns: min-content auto min-content;
}

@media (min-width: 768px) {
  .captcha-field {
    max-width: 443px;
  }
}

.captcha-img {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 253px;
  height: 253px;
}

.captcha-img img {
  max-width: 100%;
  max-height: 100%;
}
</style>
