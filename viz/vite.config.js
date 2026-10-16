import adapter from '@sveltejs/adapter-static';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  // SvelteKit 3 takes its config here; it refuses to start if svelte.config.js exists
  plugins: [
    sveltekit({
      adapter: adapter(),
      paths: {
        // set by deploy-viz.yml to the repo name for GitHub Pages; empty locally
        base: process.env.BASE_PATH ?? ''
      }
    })
  ]
});
