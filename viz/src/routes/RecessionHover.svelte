<script>
  import { usePlot } from 'svelteplot/hooks/usePlot.svelte.js';
  import { projectX } from 'svelteplot/helpers/scales.js';

  // Shows a small label pinned to the top of a shaded band while the cursor is
  // anywhere inside it. Purely passive (pointer-events: none) and positioned at
  // the top edge, so it never competes with HTMLTooltip's point tooltips.
  let { bands = [] } = $props();
  const plot = usePlot();

  let active = $state(null);
  let centerX = $state(0);

  const monthFmt = (d) => d.toLocaleDateString('en-US', { year: 'numeric', month: 'short' });

  function onPointerMove(evt) {
    if (!plot.body) return;
    const rect = plot.body.getBoundingClientRect();
    const relX = evt.clientX - rect.left;
    let hit = null;
    let cx = 0;
    for (const b of bands) {
      const x1 = projectX('x', plot.scales, b.start);
      const x2 = projectX('x', plot.scales, b.end);
      if (relX >= x1 && relX <= x2) {
        hit = b;
        cx = Math.min(Math.max((x1 + x2) / 2, 70), rect.width - 70);
        break;
      }
    }
    active = hit;
    centerX = cx;
  }

  function onPointerLeave() {
    active = null;
  }

  $effect(() => {
    plot.body?.addEventListener('pointermove', onPointerMove);
    plot.body?.addEventListener('pointerleave', onPointerLeave);
    return () => {
      plot.body?.removeEventListener('pointermove', onPointerMove);
      plot.body?.removeEventListener('pointerleave', onPointerLeave);
    };
  });
</script>

{#if active}
  <div class="band-note" style:left="{centerX}px">
    <b>{active.label}</b> · {monthFmt(active.start)} – {monthFmt(active.end)}
  </div>
{/if}

<style>
  .band-note {
    position: absolute;
    top: 6px;
    transform: translateX(-50%);
    pointer-events: none;
    background: var(--note-bg, rgba(255, 255, 255, 0.92));
    border: 1px solid var(--note-border, #d9dce1);
    border-radius: 6px;
    padding: 0.15rem 0.5rem;
    font-size: 0.72rem;
    color: var(--note-text, #444);
    white-space: nowrap;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  }

  .band-note b {
    font-weight: 600;
  }
</style>
