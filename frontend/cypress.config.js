require("dotenv").config({ path: "../.env" });

const { rmSync, readdirSync } = require("fs");
const { defineConfig } = require("cypress");

// XXX We don't actually know which one we should use
// XXX if there are more than one!
const backendHost = process.env.BACKEND_HOST.split(",")[0];
const frontendHost = process.env.FRONTEND_HOST.split(",")[0];

module.exports = defineConfig({
  scrollBehavior: "center",
  env: {
    backendHost,
    frontendHost,
    grepFilterSpecs: true,
    grepOmitFiltered: true,
    grepIntegrationFolder: ".",
  },
  e2e: {
    baseUrl: `http://${frontendHost}`,
    // Viewport used for non-responsive checks (e.g. checks in the admin)
    viewportWidth: 1920,
    viewportHeight: 1080,
    // List of viewports used for responsive checks. All tests responsive
    // tests are run on the entire list here. (Using `describeResponsive`)
    viewports: [
      [1920, 1080],
      [1440, 900],
      [1366, 768],
      [1280, 800],
      [1024, 768],
      [768, 1024],
      [800, 1280],
      [600, 960],
      [480, 853],
      [414, 896],
      [375, 667],
      [360, 640],
    ],
    setupNodeEvents(on, config) {
      on("task", {
        log(message) {
          console.log(message);
          return null;
        },
        cleanDownloadsFolder() {
          rmSync(config.downloadsFolder, {
            recursive: true,
            force: true,
          });
          return null;
        },
        downloads() {
          return readdirSync(config.downloadsFolder);
        },
      });
      require("@cypress/grep/src/plugin")(config);
      return config;
    },
  },
  retries: {
    // Configure retry attempts for `cypress run`
    // Default is 0
    runMode: 3,
    // Configure retry attempt for `cypress open`
    // Default is 0
    // openMode: 0,
  },
});
