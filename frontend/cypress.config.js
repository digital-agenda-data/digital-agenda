require("dotenv").config({ path: "../.env" });

const { rmSync } = require("fs");
const { defineConfig } = require("cypress");

// XXX We don't actually know which one we should use
// XXX if there are more than one!
const frontendHost = process.env.FRONTEND_HOST.split(",")[0];

module.exports = defineConfig({
  scrollBehavior: "center",
  e2e: {
    baseUrl: `http://${frontendHost}`,
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
      });
    },
  },
});
