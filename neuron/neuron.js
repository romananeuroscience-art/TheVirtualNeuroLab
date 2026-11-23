/* Neuron basics: two simulated neurons that run in the browser.
   HH  = Hodgkin & Huxley (1952) squid giant axon, in the standard modern form (rest -65 mV, 6.3 °C).
   LIF = the leaky integrate-and-fire neuron the lab's fly brain uses (Shiu et al. 2024 settings).
   Everything here is computed live; no number on the page is typed in by hand. */
window.NeuronSim = (() => {
  const DT = 0.01;                       // ms, small enough for stable Euler steps of HH
  const safe = (x, y) => Math.abs(x) < 1e-7 ? y : x / (1 - Math.exp(-x / y));
  function rates(V) {
    return {
      an: 0.01 * safe(V + 55, 10), bn: 0.125 * Math.exp(-(V + 65) / 80),
      am: 0.1 * safe(V + 40, 10),  bm: 4 * Math.exp(-(V + 65) / 18),
      ah: 0.07 * Math.exp(-(V + 65) / 20), bh: 1 / (1 + Math.exp(-(V + 35) / 10)),
    };
  }
  const HH = { gNa: 120, gK: 36, gL: 0.3, ENa: 50, EK: -77, EL: -54.387, C: 1 };

  /* stim(t) -> injected current (µA/cm²); syn: list of {t, kind:'E'|'I'} synaptic events.
     Returns sampled traces every 0.1 ms. */
  function runHH({ T = 60, stim = () => 0, syn = [], gE = 0.08, gI = 1.0 } = {}) {
    let V = -65, r = rates(V);
    let n = r.an / (r.an + r.bn), m = r.am / (r.am + r.bm), h = r.ah / (r.ah + r.bh);
    let ge = 0, gi = 0, k = 0;
    const ev = [...syn].sort((a, b) => a.t - b.t);
    const out = { t: [], v: [], na: [], k: [], spikes: [] };
    let up = false;
    const steps = Math.round(T / DT);
    for (let i = 0; i <= steps; i++) {
      const t = i * DT;
      while (k < ev.length && ev[k].t <= t) { if (ev[k].kind === 'E') ge += gE; else gi += gI; k++; }
      r = rates(V);
      const INa = HH.gNa * m ** 3 * h * (V - HH.ENa), IK = HH.gK * n ** 4 * (V - HH.EK), IL = HH.gL * (V - HH.EL);
      const Isyn = ge * (0 - V) + gi * (-80 - V);
      if (i % 10 === 0) { out.t.push(t); out.v.push(V); out.na.push(m ** 3 * h); out.k.push(n ** 4); }
      V += DT * (stim(t) + Isyn - INa - IK - IL) / HH.C;
      n += DT * (r.an * (1 - n) - r.bn * n); m += DT * (r.am * (1 - m) - r.bm * m); h += DT * (r.ah * (1 - h) - r.bh * h);
      ge *= Math.exp(-DT / 2); gi *= Math.exp(-DT / 4);
      if (V > 0 && !up) { out.spikes.push(t); up = true; }
      if (V < -20) up = false;
    }
    return out;
  }

  /* LIF with the fly model's numbers: rest = reset = -52 mV, threshold -45 mV, membrane 20 ms,
     refractory 2.2 ms. Input is the same stimulus, scaled (R = 20) so a pulse that fires the HH neuron
     is in the same range; the scale is illustrative, not a measured value. */
  const LIF = { v0: -52, vth: -45, vreset: -52, tau: 20, rfc: 2.2, R: 20 };
  function runLIF({ T = 60, stim = () => 0 } = {}) {
    let V = LIF.v0, ref = 0;
    const out = { t: [], v: [], spikes: [] };
    const steps = Math.round(T / DT);
    for (let i = 0; i <= steps; i++) {
      const t = i * DT;
      if (i % 10 === 0) { out.t.push(t); out.v.push(V); }
      if (ref > 0) { ref -= DT; V = LIF.vreset; continue; }
      V += DT * (LIF.v0 - V + LIF.R * stim(t)) / LIF.tau;
      if (V > LIF.vth) { out.spikes.push(t); V = LIF.vreset; ref = LIF.rfc; }
    }
    return out;
  }

  /* ---------- plotting ---------- */
  const css = (el, name) => getComputedStyle(el).getPropertyValue(name).trim();
  function plot(canvas, { series = [], tMax = 60, vMin = -90, vMax = 50, lines = [], marks = [], label = 'Voltage (mV)', progress = 1, yTicks } = {}) {
    const dpr = window.devicePixelRatio || 1;
    const w = canvas.clientWidth, h = canvas.clientHeight;
    if (canvas.width !== Math.round(w * dpr)) { canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr); }
    const g = canvas.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, w, h);
    const ink = css(canvas, '--ink'), muted = css(canvas, '--muted'), line = css(canvas, '--line');
    const L = 46, R = 10, Tp = 10, B = 30, pw = w - L - R, ph = h - Tp - B;
    const X = t => L + (t / tMax) * pw, Y = v => Tp + (1 - (v - vMin) / (vMax - vMin)) * ph;
    g.font = '11px Inter, system-ui, sans-serif'; g.fillStyle = muted; g.strokeStyle = line; g.lineWidth = 1;
    const yt = yTicks || [-80, -60, -40, -20, 0, 20, 40].filter(v => v >= vMin && v <= vMax);
    g.textAlign = 'right'; g.textBaseline = 'middle';
    for (const v of yt) { g.beginPath(); g.moveTo(L, Y(v)); g.lineTo(L + pw, Y(v)); g.stroke(); g.fillText(String(v), L - 6, Y(v)); }
    g.textAlign = 'center'; g.textBaseline = 'top';
    const step = tMax <= 60 ? 10 : 20;
    for (let t = 0; t <= tMax + 1e-9; t += step) g.fillText(String(t), X(t), Tp + ph + 6);
    g.fillText('Time (ms)', L + pw / 2, Tp + ph + 18 > h - 12 ? h - 12 : Tp + ph + 18);
    g.save(); g.translate(11, Tp + ph / 2); g.rotate(-Math.PI / 2); g.textBaseline = 'middle'; g.fillText(label, 0, 0); g.restore();
    for (const ln of lines) {                     // dashed reference lines (e.g. threshold)
      g.setLineDash([5, 4]); g.strokeStyle = ln.color || muted; g.beginPath(); g.moveTo(L, Y(ln.v)); g.lineTo(L + pw, Y(ln.v)); g.stroke();
      g.setLineDash([]); g.fillStyle = ln.color || muted; g.textAlign = 'left'; g.textBaseline = 'bottom'; g.fillText(ln.text, L + 4, Y(ln.v) - 2);
    }
    for (const mk of marks) {                     // input markers along the bottom
      g.fillStyle = mk.color; g.beginPath(); const x = X(mk.t), y = Tp + ph - 2;
      g.moveTo(x, y - 9); g.lineTo(x - 5, y); g.lineTo(x + 5, y); g.closePath(); g.fill();
    }
    for (const s of series) {
      const n = Math.max(2, Math.floor(s.t.length * progress));
      g.strokeStyle = s.color || ink; g.lineWidth = s.width || 2; g.beginPath();
      for (let i = 0; i < n; i++) { const x = X(s.t[i]), y = Y(Math.max(vMin, Math.min(vMax, s.v[i]))); i ? g.lineTo(x, y) : g.moveTo(x, y); }
      g.stroke();
      if (s.spikeMarks) {                         // LIF: a spike is an event, drawn as a tick
        for (const st of s.spikeMarks) if (st <= s.t[n - 1]) {
          g.strokeStyle = s.color; g.lineWidth = 2; g.beginPath(); g.moveTo(X(st), Y(s.spikeFrom)); g.lineTo(X(st), Y(Math.min(vMax, s.spikeTo))); g.stroke();
        }
      }
    }
  }
  function animate(draw, ms = 1400) {
    const reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) return draw(1);
    const t0 = performance.now();
    const f = now => { const p = Math.min(1, (now - t0) / ms); draw(p); if (p < 1) requestAnimationFrame(f); };
    requestAnimationFrame(f);
  }
  return { runHH, runLIF, plot, animate, LIF, HH, css };
})();
