<script>
  import { onMount } from 'svelte';

  let { children, height = 220 } = $props();
  let visible = $state(false);
  let el;

  onMount(() => {
    const obs = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          visible = true;
          obs.disconnect();
        }
      },
      { rootMargin: '400px' }
    );
    obs.observe(el);
    return () => obs.disconnect();
  });
</script>

<div bind:this={el} style:min-height="{height}px">
  {#if visible}
    {@render children()}
  {/if}
</div>
