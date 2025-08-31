import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

// https://vite.dev/config/
export default defineConfig({
  base: "/magic_8_ball/",
  plugins: [svelte()],
});
