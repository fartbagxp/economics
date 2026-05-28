<script>
  import { Plot, Line, RuleY, Rect, HTMLTooltip, Frame } from 'svelteplot';

  let { data } = $props();

  function parse(rows) {
    return rows.map((d) => ({ date: new Date(d.date + 'T12:00:00'), value: d.value }));
  }

  const cutoff = new Date('1994-01-01');

  const unrate = $derived(parse(data.series.unrate).filter((d) => d.date >= cutoff));
  const u6rate = $derived(parse(data.series.u6rate).filter((d) => d.date >= cutoff));
  const civpart = $derived(parse(data.series.civpart).filter((d) => d.date >= cutoff));
  const icsa = $derived(parse(data.series.icsa).filter((d) => d.date >= cutoff));
  const cpiaucsl     = $derived(parse(data.series.cpiaucsl).filter((d) => d.date >= cutoff));
  const cpi_mom      = $derived(parse(data.series.cpiaucsl_mom).filter((d) => d.date >= cutoff));
  const cpi_yoy      = $derived(parse(data.series.cpiaucsl_yoy).filter((d) => d.date >= cutoff));
  const core_cpi_mom = $derived(parse(data.series.cpilfesl_mom).filter((d) => d.date >= cutoff));
  const core_cpi_yoy = $derived(parse(data.series.cpilfesl_yoy).filter((d) => d.date >= cutoff));
  const pce_mom      = $derived(parse(data.series.pcepi_mom).filter((d) => d.date >= cutoff));
  const pce_yoy      = $derived(parse(data.series.pcepi_yoy).filter((d) => d.date >= cutoff));
  const core_pce_mom = $derived(parse(data.series.pcepilfe_mom).filter((d) => d.date >= cutoff));
  const core_pce_yoy = $derived(parse(data.series.pcepilfe_yoy).filter((d) => d.date >= cutoff));
  const ppi_mom      = $derived(parse(data.series.ppifid_mom).filter((d) => d.date >= cutoff));
  const ppi_yoy      = $derived(parse(data.series.ppifid_yoy).filter((d) => d.date >= cutoff));
  const core_ppi_mom = $derived(parse(data.series.ppifes_mom).filter((d) => d.date >= cutoff));
  const core_ppi_yoy = $derived(parse(data.series.ppifes_yoy).filter((d) => d.date >= cutoff));
  const gdp = $derived(parse(data.series.gdp).filter((d) => d.date >= cutoff));
  const umcsent = $derived(parse(data.series.umcsent).filter((d) => d.date >= cutoff));

  const recessions = [
    { start: new Date('1990-07-01'), end: new Date('1991-03-01') },
    { start: new Date('2001-03-01'), end: new Date('2001-11-01') },
    { start: new Date('2007-12-01'), end: new Date('2009-06-01') },
    { start: new Date('2020-02-01'), end: new Date('2020-04-01') }
  ].filter((r) => r.end >= cutoff);

  function fmt(d) {
    if (!d) return '';
    const date = d instanceof Date ? d : new Date(d);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
  }

</script>

<svelte:head>
  <title>US Economic Dashboard</title>
</svelte:head>

<main>
  <h1>US Economic Dashboard</h1>
  <p class="subtitle">Hover over any data point for details &nbsp;·&nbsp; Source: FRED / BLS</p>

  <!-- ── Labor Market ─────────────────────────────────────────── -->
  <h3 class="section-label">Labor Market</h3>
  <section class="grid">

    <!-- Unemployment Rate (U-3) -->
    <div class="card">
      <h2>Unemployment Rate (U-3)</h2>
      <p class="meta">Monthly · Seasonally Adjusted · Percent · Official measure</p>
      <Plot height={220} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: '%', grid: true }}>
        <Frame />
        <RuleY data={[0]} />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={unrate} x="date" y="value" stroke="#1a6faf" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={unrate} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip">
                  <span class="tip-label">Unemployment Rate (U-3)</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toFixed(1)}%</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <!-- U-6 Unemployment -->
    <div class="card">
      <h2>U-6 Unemployment Rate</h2>
      <p class="meta">Monthly · Seasonally Adjusted · Percent · Broadest measure</p>
      <Plot height={220} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: '%', grid: true }}>
        <Frame />
        <RuleY data={[0]} />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={u6rate} x="date" y="value" stroke="#6a4c93" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={u6rate} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip">
                  <span class="tip-label">U-6 Unemployment</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toFixed(1)}%</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <!-- Labor Force Participation -->
    <div class="card">
      <h2>Labor Force Participation Rate</h2>
      <p class="meta">Monthly · Seasonally Adjusted · Percent</p>
      <Plot height={220} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: '%', grid: true }}>
        <Frame />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={civpart} x="date" y="value" stroke="#457b9d" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={civpart} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip">
                  <span class="tip-label">Labor Force Participation</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toFixed(1)}%</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <!-- Initial Jobless Claims -->
    <div class="card">
      <h2>Initial Jobless Claims</h2>
      <p class="meta">Weekly · Seasonally Adjusted · Number of Claims</p>
      <Plot height={220} marginLeft={64} marginRight={10} x={{ type: 'time' }} y={{ label: 'Claims', grid: true }}>
        <Frame />
        <RuleY data={[0]} />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={icsa} x="date" y="value" stroke="#bc4749" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={icsa} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip">
                  <span class="tip-label">Initial Claims</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toLocaleString('en-US', { maximumFractionDigits: 0 })}</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

  </section>

  <!-- ── Prices & Output ───────────────────────────────────────── -->
  <h3 class="section-label">Prices &amp; Output</h3>
  <section class="grid">

    <!-- CPI -->
    <div class="card">
      <h2>Consumer Price Index (CPI)</h2>
      <p class="meta">Monthly · Seasonally Adjusted · Index 1982–84=100</p>
      <Plot height={220} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: 'Index', grid: true }}>
        <Frame />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={cpiaucsl} x="date" y="value" stroke="#e76f51" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={cpiaucsl} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip">
                  <span class="tip-label">CPI</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toFixed(2)}</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <!-- Consumer Sentiment -->
    <div class="card">
      <h2>Consumer Sentiment (U. Michigan)</h2>
      <p class="meta">Monthly · Not Seasonally Adjusted · Index 1966:Q1=100</p>
      <Plot height={220} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: 'Index', grid: true }}>
        <Frame />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={umcsent} x="date" y="value" stroke="#f4a261" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={umcsent} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip">
                  <span class="tip-label">Consumer Sentiment</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toFixed(1)}</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <!-- GDP — full width -->
    <div class="card wide">
      <h2>Gross Domestic Product</h2>
      <p class="meta">Quarterly · SAAR · Billions of Dollars</p>
      <Plot height={200} marginLeft={56} marginRight={10} x={{ type: 'time' }} y={{ label: '$B', grid: true }}>
        <Frame />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={gdp} x="date" y="value" stroke="#2a9d8f" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={gdp} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip">
                  <span class="tip-label">GDP</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">${datum.value.toLocaleString('en-US', { maximumFractionDigits: 0 })}B</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

  </section>

  <!-- ── Inflation ────────────────────────────────────────────── -->
  <h3 class="section-label">Inflation</h3>

  <p class="sub-label">Year-over-Year Change (%)</p>
  <section class="grid">

    <div class="card">
      <h2>CPI — Year-over-Year</h2>
      <p class="meta">
        Monthly · SA ·
        <span class="legend-swatch" style="background:#e63946"></span> Headline &nbsp;
        <span class="legend-swatch dashed" style="border-color:#ff9f43"></span> Core (ex. Food &amp; Energy)
      </p>
      <Plot height={220} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: '%', grid: true }}>
        <Frame />
        <RuleY data={[0]} />
        <RuleY data={[2]} stroke="#bbb" strokeDasharray="4,3" />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={core_cpi_yoy} x="date" y="value" stroke="#ff9f43" strokeWidth={1.5} strokeDasharray="5,3" />
        <Line data={cpi_yoy} x="date" y="value" stroke="#e63946" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={cpi_yoy} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip">
                  <span class="tip-label">CPI YoY</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toFixed(2)}%</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <div class="card">
      <h2>PCE — Year-over-Year</h2>
      <p class="meta">
        Monthly · SA ·
        <span class="legend-swatch" style="background:#2a9d8f"></span> Headline &nbsp;
        <span class="legend-swatch dashed" style="border-color:#52b788"></span> Core — Fed's preferred
      </p>
      <Plot height={220} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: '%', grid: true }}>
        <Frame />
        <RuleY data={[0]} />
        <RuleY data={[2]} stroke="#bbb" strokeDasharray="4,3" />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={core_pce_yoy} x="date" y="value" stroke="#52b788" strokeWidth={1.5} strokeDasharray="5,3" />
        <Line data={pce_yoy} x="date" y="value" stroke="#2a9d8f" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={pce_yoy} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip">
                  <span class="tip-label">PCE YoY</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toFixed(2)}%</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <div class="card wide">
      <h2>PPI Final Demand — Year-over-Year</h2>
      <p class="meta">
        Monthly · SA · Data from Nov 2009 ·
        <span class="legend-swatch" style="background:#457b9d"></span> Headline &nbsp;
        <span class="legend-swatch dashed" style="border-color:#74b3ce"></span> Core (ex. Foods &amp; Energy)
      </p>
      <Plot height={200} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: '%', grid: true }}>
        <Frame />
        <RuleY data={[0]} />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={core_ppi_yoy} x="date" y="value" stroke="#74b3ce" strokeWidth={1.5} strokeDasharray="5,3" />
        <Line data={ppi_yoy} x="date" y="value" stroke="#457b9d" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={ppi_yoy} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip">
                  <span class="tip-label">PPI YoY</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toFixed(2)}%</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <div class="card wide">
      <h2>Core Inflation Comparison — Year-over-Year</h2>
      <p class="meta">
        Monthly · SA · Ex. Food &amp; Energy ·
        <span class="legend-swatch" style="background:#ff9f43"></span> Core CPI &nbsp;
        <span class="legend-swatch" style="background:#52b788"></span> Core PCE (Fed's preferred) &nbsp;
        <span class="legend-swatch" style="background:#74b3ce"></span> Core PPI
      </p>
      <Plot height={200} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: '%', grid: true }}>
        <Frame />
        <RuleY data={[0]} />
        <RuleY data={[2]} stroke="#bbb" strokeDasharray="4,3" />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={core_cpi_yoy} x="date" y="value" stroke="#ff9f43" strokeWidth={1.5} />
        <Line data={core_pce_yoy} x="date" y="value" stroke="#52b788" strokeWidth={1.5} />
        <Line data={core_ppi_yoy} x="date" y="value" stroke="#74b3ce" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={core_pce_yoy} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip">
                  <span class="tip-label">Core PCE YoY</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toFixed(2)}%</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

  </section>

  <p class="sub-label">Month-over-Month Change (%)</p>
  <section class="grid">

    <div class="card">
      <h2>CPI — Month-over-Month</h2>
      <p class="meta">
        Monthly · SA ·
        <span class="legend-swatch" style="background:#e63946"></span> Headline &nbsp;
        <span class="legend-swatch dashed" style="border-color:#ff9f43"></span> Core (ex. Food &amp; Energy)
      </p>
      <Plot height={220} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: '%', grid: true }}>
        <Frame />
        <RuleY data={[0]} />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={core_cpi_mom} x="date" y="value" stroke="#ff9f43" strokeWidth={1.5} strokeDasharray="5,3" />
        <Line data={cpi_mom} x="date" y="value" stroke="#e63946" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={cpi_mom} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip">
                  <span class="tip-label">CPI MoM</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toFixed(2)}%</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <div class="card">
      <h2>PCE — Month-over-Month</h2>
      <p class="meta">
        Monthly · SA ·
        <span class="legend-swatch" style="background:#2a9d8f"></span> Headline &nbsp;
        <span class="legend-swatch dashed" style="border-color:#52b788"></span> Core — Fed's preferred
      </p>
      <Plot height={220} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: '%', grid: true }}>
        <Frame />
        <RuleY data={[0]} />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={core_pce_mom} x="date" y="value" stroke="#52b788" strokeWidth={1.5} strokeDasharray="5,3" />
        <Line data={pce_mom} x="date" y="value" stroke="#2a9d8f" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={pce_mom} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip">
                  <span class="tip-label">PCE MoM</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toFixed(2)}%</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <div class="card wide">
      <h2>PPI Final Demand — Month-over-Month</h2>
      <p class="meta">
        Monthly · SA · Data from Nov 2009 ·
        <span class="legend-swatch" style="background:#457b9d"></span> Headline &nbsp;
        <span class="legend-swatch dashed" style="border-color:#74b3ce"></span> Core (ex. Foods &amp; Energy)
      </p>
      <Plot height={200} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: '%', grid: true }}>
        <Frame />
        <RuleY data={[0]} />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={core_ppi_mom} x="date" y="value" stroke="#74b3ce" strokeWidth={1.5} strokeDasharray="5,3" />
        <Line data={ppi_mom} x="date" y="value" stroke="#457b9d" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={ppi_mom} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip">
                  <span class="tip-label">PPI MoM</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toFixed(2)}%</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <div class="card wide">
      <h2>Core Inflation Comparison — Month-over-Month</h2>
      <p class="meta">
        Monthly · SA · Ex. Food &amp; Energy ·
        <span class="legend-swatch" style="background:#ff9f43"></span> Core CPI &nbsp;
        <span class="legend-swatch" style="background:#52b788"></span> Core PCE (Fed's preferred) &nbsp;
        <span class="legend-swatch" style="background:#74b3ce"></span> Core PPI
      </p>
      <Plot height={200} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: '%', grid: true }}>
        <Frame />
        <RuleY data={[0]} />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={core_cpi_mom} x="date" y="value" stroke="#ff9f43" strokeWidth={1.5} />
        <Line data={core_pce_mom} x="date" y="value" stroke="#52b788" strokeWidth={1.5} />
        <Line data={core_ppi_mom} x="date" y="value" stroke="#74b3ce" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={core_pce_mom} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip">
                  <span class="tip-label">Core PCE MoM</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toFixed(2)}%</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

  </section>
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: #f8f9fa;
    color: #1a1a2e;
  }

  main {
    max-width: 1100px;
    margin: 0 auto;
    padding: 2rem 1.5rem 4rem;
  }

  h1 {
    font-size: 1.75rem;
    font-weight: 700;
    margin: 0 0 0.25rem;
    letter-spacing: -0.02em;
  }

  .subtitle {
    color: #666;
    margin: 0 0 2rem;
    font-size: 0.875rem;
  }

  .section-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #999;
    margin: 2rem 0 0.75rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #e5e7eb;
  }

  .grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.25rem;
  }

  .card {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 1.25rem 1.25rem 0.75rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  }

  .card.wide {
    grid-column: 1 / -1;
  }

  h2 {
    font-size: 0.95rem;
    font-weight: 600;
    margin: 0 0 0.1rem;
  }

  .meta {
    font-size: 0.72rem;
    color: #888;
    margin: 0 0 0.75rem;
  }

  .sub-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #666;
    margin: 1.25rem 0 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  .legend-swatch {
    display: inline-block;
    width: 18px;
    height: 3px;
    border-radius: 2px;
    vertical-align: middle;
    margin-right: 2px;
  }

  .legend-swatch.dashed {
    background: none;
    border-top: 2.5px dashed;
    border-radius: 0;
  }

  :global(.tip) {
    display: flex;
    flex-direction: column;
    gap: 0.1rem;
    padding: 0.5rem 0.75rem;
    background: rgba(15, 15, 30, 0.88);
    color: #fff;
    border-radius: 7px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 0.8rem;
    backdrop-filter: blur(4px);
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.22);
    white-space: nowrap;
    pointer-events: none;
  }

  :global(.tip-label) {
    font-weight: 600;
    font-size: 0.68rem;
    opacity: 0.7;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  :global(.tip-date) {
    font-size: 0.78rem;
    opacity: 0.85;
  }

  :global(.tip-val) {
    font-size: 1.05rem;
    font-weight: 700;
    margin-top: 0.1rem;
  }
</style>
