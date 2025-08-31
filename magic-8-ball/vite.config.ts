import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

// https://vite.dev/config/
export default defineConfig({
  // Read the base path from an environment variable, defaulting to '/'
  // for local development.
  base: process.env.BASE_URL || "/",
  plugins: [svelte()],
});
