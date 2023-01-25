require("dotenv").config({ path: "../.env" });

const { defineConfig } = require("cypress");

// XXX We don't actually know which one we should use
// XXX if there are more than one!
const frontendHost = process.env.FRONTEND_HOST.split(",")[0];

module.exports = defineConfig({
  e2e: {
    baseUrl: `http://${frontendHost}`,
  },
});
