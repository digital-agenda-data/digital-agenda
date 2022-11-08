/* eslint-env node */
require("@rushstack/eslint-patch/modern-module-resolution");

module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
  },
  extends: [
    "plugin:vue/vue3-recommended",
    "eslint:recommended",
    "@vue/eslint-config-prettier",
    "plugin:prettier/recommended",
    "plugin:compat/recommended",
  ],
  parserOptions: {
    ecmaVersion: "latest",
  },
};
