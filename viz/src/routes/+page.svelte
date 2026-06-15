<script>
  import { Plot, Line, RuleY, Rect, HTMLTooltip, Frame } from 'svelteplot';

  let { data } = $props();

  function parse(rows) {
    return rows.map((d) => ({ date: new Date(d.date + 'T12:00:00'), value: d.value }));
  }

  // Merges named series into a flat array (for HTMLTooltip data) and a date→values Map
  function multiLine(named) {
    const entries = Object.entries(named);
    const all = entries.flatMap(([, arr]) => arr);
    const m = new Map();
    for (const [key, arr] of entries) {
      for (const d of arr) {
        if (!m.has(d.date.getTime())) m.set(d.date.getTime(), { date: d.date });
        m.get(d.date.getTime())[key] = d.value;
      }
    }
    return { all, byDate: m };
  }

  const cutoff = new Date('1994-01-01');
  const midDate = new Date((cutoff.getTime() + new Date().getTime()) / 2);

  const unrate       = $derived(parse(data.series.unrate).filter((d) => d.date >= cutoff));
  const u6rate       = $derived(parse(data.series.u6rate).filter((d) => d.date >= cutoff));
  const ltunempPct   = $derived(parse(data.series.lns13008397).filter((d) => d.date >= cutoff));
  const ltunempCount = $derived(parse(data.series.uemp27ov).filter((d) => d.date >= cutoff));
  const civpart      = $derived(parse(data.series.civpart).filter((d) => d.date >= cutoff));
  const lfprMen      = $derived(parse(data.series.lns11300001).filter((d) => d.date >= cutoff));
  const lfprWomen    = $derived(parse(data.series.lns11300002).filter((d) => d.date >= cutoff));
  const lfprLtHs     = $derived(parse(data.series.lns11327659));
  const lfprHsOnly   = $derived(parse(data.series.lns11327660));
  const lfprSomeCol  = $derived(parse(data.series.lns11327689));
  const lfprBachPlus = $derived(parse(data.series.lns11327662));

  // Merged dataset so HTMLTooltip fires near any of the 4 education lines
  const eduAllPoints = $derived([
    ...lfprLtHs.map((d) => ({ ...d, cat: 'ltHs' })),
    ...lfprHsOnly.map((d) => ({ ...d, cat: 'hsOnly' })),
    ...lfprSomeCol.map((d) => ({ ...d, cat: 'someCol' })),
    ...lfprBachPlus.map((d) => ({ ...d, cat: 'bachPlus' })),
  ]);

  // Date-keyed lookup for all 4 values so the tooltip can show them together
  const eduByDate = $derived(
    (() => {
      const m = new Map();
      for (const d of lfprBachPlus) m.set(d.date.getTime(), { bachPlus: d.value });
      for (const d of lfprSomeCol) { const e = m.get(d.date.getTime()); if (e) e.someCol = d.value; }
      for (const d of lfprHsOnly)  { const e = m.get(d.date.getTime()); if (e) e.hsOnly  = d.value; }
      for (const d of lfprLtHs)    { const e = m.get(d.date.getTime()); if (e) e.ltHs    = d.value; }
      return m;
    })()
  );
  const icsa         = $derived(parse(data.series.icsa).filter((d) => d.date >= cutoff));
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

  const pi       = $derived(parse(data.series.pi).filter((d) => d.date >= cutoff));
  const dspi     = $derived(parse(data.series.dspi).filter((d) => d.date >= cutoff));
  const pce      = $derived(parse(data.series.pce).filter((d) => d.date >= cutoff));
  const psave    = $derived(parse(data.series.psave).filter((d) => d.date >= cutoff));
  const psavert  = $derived(parse(data.series.psavert).filter((d) => d.date >= cutoff));
  const mich     = $derived(parse(data.series.mich).filter((d) => d.date >= cutoff));
  const t5yie    = $derived(parse(data.series.t5yie).filter((d) => d.date >= cutoff));
  const t10yie   = $derived(parse(data.series.t10yie).filter((d) => d.date >= cutoff));

  const incomeML  = $derived(multiLine({ income: pi, disposable: dspi }));
  const inflExpML = $derived(multiLine({ mich: mich, b5y: t5yie, b10y: t10yie }));

  const cpiYoyML  = $derived(multiLine({ headline: cpi_yoy,     core: core_cpi_yoy }));
  const pceYoyML  = $derived(multiLine({ headline: pce_yoy,     core: core_pce_yoy }));
  const ppiYoyML  = $derived(multiLine({ headline: ppi_yoy,     core: core_ppi_yoy }));
  const coreYoyML = $derived(multiLine({ cpi: core_cpi_yoy, pce: core_pce_yoy, ppi: core_ppi_yoy }));
  const cpiMomML  = $derived(multiLine({ headline: cpi_mom,     core: core_cpi_mom }));
  const pceMomML  = $derived(multiLine({ headline: pce_mom,     core: core_pce_mom }));
  const ppiMomML  = $derived(multiLine({ headline: ppi_mom,     core: core_ppi_mom }));
  const coreMomML = $derived(multiLine({ cpi: core_cpi_mom, pce: core_pce_mom, ppi: core_ppi_mom }));

  const recessions = [
    { start: new Date('1990-07-01'), end: new Date('1991-03-01') },
    { start: new Date('2001-03-01'), end: new Date('2001-11-01') },
    { start: new Date('2007-12-01'), end: new Date('2009-06-01') },
    { start: new Date('2020-02-01'), end: new Date('2020-04-01') }
  ].filter((r) => r.end >= cutoff);

  function tipTransform(datum) {
    if (!datum) return 'translate(8px, -50%)';
    return datum.date > midDate
      ? 'translate(calc(-100% - 8px), -50%)'
      : 'translate(8px, -50%)';
  }

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
                <div class="tip" style:transform={tipTransform(datum)}>
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
                <div class="tip" style:transform={tipTransform(datum)}>
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

    <!-- Long-term Unemployed — % of total -->
    <div class="card">
      <h2>Long-Term Unemployed (27+ Weeks)</h2>
      <p class="meta">Monthly · Seasonally Adjusted · % of Total Unemployed</p>
      <Plot height={220} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: '%', grid: true }}>
        <Frame />
        <RuleY data={[0]} />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={ltunempPct} x="date" y="value" stroke="#d62828" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={ltunempPct} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip" style:transform={tipTransform(datum)}>
                  <span class="tip-label">Long-Term Unemployed</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toFixed(1)}%</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <!-- Long-term Unemployed — count -->
    <div class="card">
      <h2>Long-Term Unemployed — Count</h2>
      <p class="meta">Monthly · Seasonally Adjusted · Thousands of Persons</p>
      <Plot height={220} marginLeft={54} marginRight={10} x={{ type: 'time' }} y={{ label: 'Thousands', grid: true }}>
        <Frame />
        <RuleY data={[0]} />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={ltunempCount} x="date" y="value" stroke="#e07a5f" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={ltunempCount} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip" style:transform={tipTransform(datum)}>
                  <span class="tip-label">Long-Term Unemployed</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toLocaleString('en-US', { maximumFractionDigits: 0 })}K</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <!-- Labor Force Participation -->
    <div class="card wide">
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
                <div class="tip" style:transform={tipTransform(datum)}>
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

    <!-- LFPR Men -->
    <div class="card">
      <h2>Labor Force Participation — Men</h2>
      <p class="meta">Monthly · Seasonally Adjusted · Percent</p>
      <Plot height={220} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: '%', grid: true }}>
        <Frame />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={lfprMen} x="date" y="value" stroke="#1a6faf" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={lfprMen} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip" style:transform={tipTransform(datum)}>
                  <span class="tip-label">LFPR Men</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toFixed(1)}%</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <!-- LFPR Women -->
    <div class="card">
      <h2>Labor Force Participation — Women</h2>
      <p class="meta">Monthly · Seasonally Adjusted · Percent</p>
      <Plot height={220} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: '%', grid: true }}>
        <Frame />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={lfprWomen} x="date" y="value" stroke="#e76f51" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={lfprWomen} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip" style:transform={tipTransform(datum)}>
                  <span class="tip-label">LFPR Women</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toFixed(1)}%</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <!-- LFPR by Educational Attainment -->
    <div class="card wide">
      <h2>Labor Force Participation by Educational Attainment (25+)</h2>
      <p class="meta">
        Monthly · Seasonally Adjusted · Percent · Data from Jan 1992 ·
        <span class="legend-swatch" style="background:#bc4749"></span> Less than HS &nbsp;
        <span class="legend-swatch" style="background:#f4a261"></span> HS grad, no college &nbsp;
        <span class="legend-swatch" style="background:#457b9d"></span> Some college / Associate &nbsp;
        <span class="legend-swatch" style="background:#2a9d8f"></span> Bachelor's and higher
      </p>
      <Plot height={300} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: '%', grid: true }}>
        <Frame />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={lfprLtHs}     x="date" y="value" stroke="#bc4749" strokeWidth={1.5} />
        <Line data={lfprHsOnly}   x="date" y="value" stroke="#f4a261" strokeWidth={1.5} />
        <Line data={lfprSomeCol}  x="date" y="value" stroke="#457b9d" strokeWidth={1.5} />
        <Line data={lfprBachPlus} x="date" y="value" stroke="#2a9d8f" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={eduAllPoints} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                {@const edu = eduByDate.get(datum.date.getTime())}
                <div class="tip" style:transform={tipTransform(datum)}>
                  <span class="tip-label">LFPR by Education (25+)</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  {#if edu}
                    <span class="tip-edu-row"><span style="color:#2a9d8f">●</span> Bach+    <b>{edu.bachPlus?.toFixed(1)}%</b></span>
                    <span class="tip-edu-row"><span style="color:#457b9d">●</span> Some col <b>{edu.someCol?.toFixed(1)}%</b></span>
                    <span class="tip-edu-row"><span style="color:#f4a261">●</span> HS only  <b>{edu.hsOnly?.toFixed(1)}%</b></span>
                    <span class="tip-edu-row"><span style="color:#bc4749">●</span> &lt; HS   <b>{edu.ltHs?.toFixed(1)}%</b></span>
                  {/if}
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <!-- Initial Jobless Claims -->
    <div class="card wide">
      <h2>Initial Jobless Claims</h2>
      <p class="meta">Weekly · Seasonally Adjusted · Number of Claims</p>
      <Plot height={300} marginLeft={64} marginRight={10} x={{ type: 'time' }} y={{ label: 'Claims', grid: true }}>
        <Frame />
        <RuleY data={[0]} />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={icsa} x="date" y="value" stroke="#bc4749" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={icsa} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip" style:transform={tipTransform(datum)}>
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
                <div class="tip" style:transform={tipTransform(datum)}>
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
                <div class="tip" style:transform={tipTransform(datum)}>
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
                <div class="tip" style:transform={tipTransform(datum)}>
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
          <HTMLTooltip data={cpiYoyML.all} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                {@const v = cpiYoyML.byDate.get(datum.date.getTime())}
                <div class="tip" style:transform={tipTransform(datum)}>
                  <span class="tip-label">CPI YoY</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  {#if v}
                    <span class="tip-edu-row"><span style="color:#e63946">●</span> Headline <b>{v.headline?.toFixed(2)}%</b></span>
                    <span class="tip-edu-row"><span style="color:#ff9f43">●</span> Core     <b>{v.core?.toFixed(2)}%</b></span>
                  {/if}
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
          <HTMLTooltip data={pceYoyML.all} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                {@const v = pceYoyML.byDate.get(datum.date.getTime())}
                <div class="tip" style:transform={tipTransform(datum)}>
                  <span class="tip-label">PCE YoY</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  {#if v}
                    <span class="tip-edu-row"><span style="color:#2a9d8f">●</span> Headline <b>{v.headline?.toFixed(2)}%</b></span>
                    <span class="tip-edu-row"><span style="color:#52b788">●</span> Core     <b>{v.core?.toFixed(2)}%</b></span>
                  {/if}
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
          <HTMLTooltip data={ppiYoyML.all} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                {@const v = ppiYoyML.byDate.get(datum.date.getTime())}
                <div class="tip" style:transform={tipTransform(datum)}>
                  <span class="tip-label">PPI YoY</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  {#if v}
                    <span class="tip-edu-row"><span style="color:#457b9d">●</span> Headline <b>{v.headline?.toFixed(2)}%</b></span>
                    <span class="tip-edu-row"><span style="color:#74b3ce">●</span> Core     <b>{v.core?.toFixed(2)}%</b></span>
                  {/if}
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
          <HTMLTooltip data={coreYoyML.all} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                {@const v = coreYoyML.byDate.get(datum.date.getTime())}
                <div class="tip" style:transform={tipTransform(datum)}>
                  <span class="tip-label">Core Inflation YoY</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  {#if v}
                    <span class="tip-edu-row"><span style="color:#ff9f43">●</span> Core CPI <b>{v.cpi?.toFixed(2)}%</b></span>
                    <span class="tip-edu-row"><span style="color:#52b788">●</span> Core PCE <b>{v.pce?.toFixed(2)}%</b></span>
                    <span class="tip-edu-row"><span style="color:#74b3ce">●</span> Core PPI <b>{v.ppi?.toFixed(2)}%</b></span>
                  {/if}
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
          <HTMLTooltip data={cpiMomML.all} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                {@const v = cpiMomML.byDate.get(datum.date.getTime())}
                <div class="tip" style:transform={tipTransform(datum)}>
                  <span class="tip-label">CPI MoM</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  {#if v}
                    <span class="tip-edu-row"><span style="color:#e63946">●</span> Headline <b>{v.headline?.toFixed(2)}%</b></span>
                    <span class="tip-edu-row"><span style="color:#ff9f43">●</span> Core     <b>{v.core?.toFixed(2)}%</b></span>
                  {/if}
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
          <HTMLTooltip data={pceMomML.all} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                {@const v = pceMomML.byDate.get(datum.date.getTime())}
                <div class="tip" style:transform={tipTransform(datum)}>
                  <span class="tip-label">PCE MoM</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  {#if v}
                    <span class="tip-edu-row"><span style="color:#2a9d8f">●</span> Headline <b>{v.headline?.toFixed(2)}%</b></span>
                    <span class="tip-edu-row"><span style="color:#52b788">●</span> Core     <b>{v.core?.toFixed(2)}%</b></span>
                  {/if}
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
          <HTMLTooltip data={ppiMomML.all} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                {@const v = ppiMomML.byDate.get(datum.date.getTime())}
                <div class="tip" style:transform={tipTransform(datum)}>
                  <span class="tip-label">PPI MoM</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  {#if v}
                    <span class="tip-edu-row"><span style="color:#457b9d">●</span> Headline <b>{v.headline?.toFixed(2)}%</b></span>
                    <span class="tip-edu-row"><span style="color:#74b3ce">●</span> Core     <b>{v.core?.toFixed(2)}%</b></span>
                  {/if}
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
          <HTMLTooltip data={coreMomML.all} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                {@const v = coreMomML.byDate.get(datum.date.getTime())}
                <div class="tip" style:transform={tipTransform(datum)}>
                  <span class="tip-label">Core Inflation MoM</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  {#if v}
                    <span class="tip-edu-row"><span style="color:#ff9f43">●</span> Core CPI <b>{v.cpi?.toFixed(2)}%</b></span>
                    <span class="tip-edu-row"><span style="color:#52b788">●</span> Core PCE <b>{v.pce?.toFixed(2)}%</b></span>
                    <span class="tip-edu-row"><span style="color:#74b3ce">●</span> Core PPI <b>{v.ppi?.toFixed(2)}%</b></span>
                  {/if}
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

  </section>

  <!-- ── Consumer Spending & Income ───────────────────────────── -->
  <h3 class="section-label">Consumer Spending &amp; Income</h3>
  <section class="grid">

    <!-- Personal Income vs Disposable Income -->
    <div class="card wide">
      <h2>Personal Income &amp; Disposable Personal Income</h2>
      <p class="meta">
        Monthly · SAAR · Billions of Dollars ·
        <span class="legend-swatch" style="background:#1a6faf"></span> Personal Income &nbsp;
        <span class="legend-swatch dashed" style="border-color:#f4a261"></span> Disposable Personal Income
      </p>
      <Plot height={220} marginLeft={64} marginRight={10} x={{ type: 'time' }} y={{ label: '$B', grid: true }}>
        <Frame />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={dspi} x="date" y="value" stroke="#f4a261" strokeWidth={1.5} strokeDasharray="5,3" />
        <Line data={pi} x="date" y="value" stroke="#1a6faf" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={incomeML.all} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                {@const v = incomeML.byDate.get(datum.date.getTime())}
                <div class="tip" style:transform={tipTransform(datum)}>
                  <span class="tip-label">Income</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  {#if v}
                    <span class="tip-edu-row"><span style="color:#1a6faf">●</span> Personal Income &nbsp;<b>${v.income?.toLocaleString('en-US', { maximumFractionDigits: 0 })}B</b></span>
                    <span class="tip-edu-row"><span style="color:#f4a261">●</span> Disposable &nbsp;<b>${v.disposable?.toLocaleString('en-US', { maximumFractionDigits: 0 })}B</b></span>
                  {/if}
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <!-- Personal Consumption Expenditures -->
    <div class="card wide">
      <h2>Personal Consumption Expenditures</h2>
      <p class="meta">Monthly · SAAR · Billions of Dollars</p>
      <Plot height={220} marginLeft={64} marginRight={10} x={{ type: 'time' }} y={{ label: '$B', grid: true }}>
        <Frame />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={pce} x="date" y="value" stroke="#2a9d8f" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={pce} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip" style:transform={tipTransform(datum)}>
                  <span class="tip-label">PCE</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">${datum.value.toLocaleString('en-US', { maximumFractionDigits: 0 })}B</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <!-- Personal Savings Level -->
    <div class="card">
      <h2>Personal Saving</h2>
      <p class="meta">Monthly · SAAR · Billions of Dollars</p>
      <Plot height={220} marginLeft={64} marginRight={10} x={{ type: 'time' }} y={{ label: '$B', grid: true }}>
        <Frame />
        <RuleY data={[0]} />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={psave} x="date" y="value" stroke="#457b9d" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={psave} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip" style:transform={tipTransform(datum)}>
                  <span class="tip-label">Personal Saving</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">${datum.value.toLocaleString('en-US', { maximumFractionDigits: 0 })}B</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

    <!-- Personal Savings Rate -->
    <div class="card">
      <h2>Personal Saving Rate</h2>
      <p class="meta">Monthly · Seasonally Adjusted · Percent of Disposable Income</p>
      <Plot height={220} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: '%', grid: true }}>
        <Frame />
        <RuleY data={[0]} />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={psavert} x="date" y="value" stroke="#6a4c93" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={psavert} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                <div class="tip" style:transform={tipTransform(datum)}>
                  <span class="tip-label">Personal Saving Rate</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  <span class="tip-val">{datum.value.toFixed(1)}%</span>
                </div>
              {/if}
            {/snippet}
          </HTMLTooltip>
        {/snippet}
      </Plot>
    </div>

  </section>

  <!-- ── Inflation Expectations ────────────────────────────────── -->
  <h3 class="section-label">Inflation Expectations</h3>
  <section class="grid">

    <!-- Inflation Expectations: Survey vs Market -->
    <div class="card wide">
      <h2>Inflation Expectations</h2>
      <p class="meta">
        <span class="legend-swatch" style="background:#e63946"></span> U. Michigan 1-Year (survey, monthly, NSA) &nbsp;
        <span class="legend-swatch" style="background:#457b9d"></span> 5-Year Breakeven (market-based, daily) &nbsp;
        <span class="legend-swatch dashed" style="border-color:#74b3ce"></span> 10-Year Breakeven (market-based, daily)
      </p>
      <Plot height={280} marginLeft={44} marginRight={10} x={{ type: 'time' }} y={{ label: '%', grid: true }}>
        <Frame />
        <RuleY data={[0]} />
        <RuleY data={[2]} stroke="#bbb" strokeDasharray="4,3" />
        <Rect data={recessions} x1="start" x2="end" fill="#888" fillOpacity={0.08} stroke="none" />
        <Line data={t10yie} x="date" y="value" stroke="#74b3ce" strokeWidth={1.5} strokeDasharray="5,3" />
        <Line data={t5yie} x="date" y="value" stroke="#457b9d" strokeWidth={1.5} />
        <Line data={mich} x="date" y="value" stroke="#e63946" strokeWidth={1.5} />
        {#snippet overlay()}
          <HTMLTooltip data={inflExpML.all} x="date" y="value">
            {#snippet children({ datum })}
              {#if datum}
                {@const v = inflExpML.byDate.get(datum.date.getTime())}
                <div class="tip" style:transform={tipTransform(datum)}>
                  <span class="tip-label">Inflation Expectations</span>
                  <span class="tip-date">{fmt(datum.date)}</span>
                  {#if v}
                    {#if v.mich != null}<span class="tip-edu-row"><span style="color:#e63946">●</span> UMich 1Y &nbsp;<b>{v.mich?.toFixed(1)}%</b></span>{/if}
                    {#if v.b5y != null}<span class="tip-edu-row"><span style="color:#457b9d">●</span> 5Y Breakeven <b>{v.b5y?.toFixed(2)}%</b></span>{/if}
                    {#if v.b10y != null}<span class="tip-edu-row"><span style="color:#74b3ce">●</span> 10Y Breakeven <b>{v.b10y?.toFixed(2)}%</b></span>{/if}
                  {/if}
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

  :global(.tip-edu-row) {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    font-size: 0.8rem;
    font-variant-numeric: tabular-nums;
  }
</style>
