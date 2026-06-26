<script>
  import { setPlotDefaults } from 'svelteplot';

  let { children } = $props();

  // These sections use grid-template-columns: minmax(500px, 1fr) minmax(500px, 1fr).
  // That makes each track at least 500px, so on mobile the grid overflows to 1020px
  // (500+20gap+500), matching sections that have regular half-column cards.
  // Figure width = max(1020px grid min, main-content-width) - 42px (card padding+border).
  // Starting the SVG at that size means bind:clientWidth never needs to resize it.
  setPlotDefaults({
    initialWidth: typeof window !== 'undefined'
      ? Math.max(1020, Math.min(window.innerWidth, 1100) - 48) - 42
      : 1000
  });
</script>
{@render children()}
