import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 8080,
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          topology: ["./src/assets/topology.json"],
          highcharts: [
            "node_modules/highcharts/highcharts.js",
            "node_modules/highcharts/highcharts-more.js",
            "node_modules/highcharts/modules/map.js",
            "node_modules/highcharts/modules/exporting.js",
            "node_modules/highcharts/modules/export-data.js",
            "node_modules/highcharts/modules/offline-exporting.js",
            "node_modules/highcharts/modules/accessibility.js",
            "node_modules/highcharts/modules/no-data-to-display.js",
          ],
        },
      },
    },
  },
});
