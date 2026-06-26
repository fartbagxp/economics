<script>
  import { setPlotDefaults } from 'svelteplot';

  let { children } = $props();

  // Cards using this context have min-width: 600px, which forces the grid to overflow on
  // mobile (matching the behaviour of sections that have regular half-column cards — those
  // push 1fr tracks to 500px each, creating a 1020px-wide grid on mobile).
  // The card's figure content width = max(min(viewport, 1100) - 90, 600 - 42) = max(…, 558).
  // We start the SVG at that size so bind:clientWidth never needs to resize it.
  setPlotDefaults({
    initialWidth: typeof window !== 'undefined'
      ? Math.max(Math.min(window.innerWidth, 1100) - 90, 558)
      : 1000
  });
</script>
{@render children()}
