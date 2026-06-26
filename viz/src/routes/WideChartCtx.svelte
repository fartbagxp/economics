<script>
  import { setPlotDefaults } from 'svelteplot';

  let { children } = $props();

  // Set initialWidth to match the actual wide-card content width so the
  // SVG is already at the right size on first paint (before bind:clientWidth fires).
  // Wide cards fill: min(viewport, 1100px) - 48px main padding - 40px card padding - 2px card border.
  // We only use this for *wide* charts (not half-column cards) to avoid overflow on narrow cards.
  setPlotDefaults({
    initialWidth: typeof window !== 'undefined'
      ? Math.min(window.innerWidth, 1100) - 90
      : 1000
  });
</script>
{@render children()}
