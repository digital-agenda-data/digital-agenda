/* eslint-env node */
require("@rushstack/eslint-patch/modern-module-resolution");

const pluginsExtends = [
  "plugin:vue/vue3-recommended",
  "eslint:recommended",
  "@vue/eslint-config-prettier",
  "plugin:prettier/recommended",
  "plugin:compat/recommended",
  "plugin:cypress/recommended",
];

module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
  },
  extends: pluginsExtends,
  parserOptions: {
    ecmaVersion: "latest",
  },
  overrides: [
    // Settings onlly for TS
    {
      files: ["*.ts", "*.tsx"],
      extends: [...pluginsExtends, "plugin:@typescript-eslint/recommended"],
    },
  ],
};
