/**
 * Adesivo com canto descolando.
 * Geometria: o canto inferior direito é dobrado ao longo de uma diagonal. A parte dobrada (a "aba")
 * é o triângulo refletido, que mostra o verso do papel; sob ela cai uma sombra suave sobre a imagem.
 * A dobra vai de `rest` (repouso) a `hover` (passar o mouse) em 500 ms com ease-out de 4ª potência,
 * e, com data-scroll-peel, acompanha a posição do cartão na tela.
 */
const NS = 'http://www.w3.org/2000/svg';
let uid = 0;

const clamp = (v: number, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const easeOutQuart = (t: number) => 1 - Math.pow(1 - t, 4);

class Peel {
  private el: HTMLElement;
  private vbW = 600;
  private vbH: number;
  private r = 18;                  // raio dos cantos
  private rest: number;
  private hover: number;
  private scrollMax: number;
  private dur = 500;
  private cur: number;
  private from: number;
  private to: number;
  private t0 = 0;
  private raf = 0;
  private hovering = false;
  private visible = true;
  private scrollPeel: boolean;
  private paths!: { base: SVGPathElement; clip: SVGPathElement; flap: SVGPathElement; shadow: SVGPathElement };

  constructor(el: HTMLElement) {
    this.el = el;
    const img = el.querySelector('img');
    const [aw, ah] = (el.dataset.aspect ?? '3/2').split('/').map(Number);
    this.vbH = this.vbW * (ah / aw);
    this.rest = Number(el.dataset.foldRest ?? 8);
    this.hover = Number(el.dataset.foldHover ?? 55);
    this.scrollMax = Number(el.dataset.foldScroll ?? 40);
    this.scrollPeel = 'scrollPeel' in el.dataset;
    this.cur = this.from = this.to = this.rest;
    this.build(img?.currentSrc || img?.src || '');
    if (img) img.style.display = 'none';
    this.bind();
    this.render(this.cur);
    new IntersectionObserver((es) => es.forEach((e) => (this.visible = e.isIntersecting)), { rootMargin: '120px' }).observe(el);
    if (this.scrollPeel) addEventListener('scroll', () => this.onScroll(), { passive: true });
    this.onScroll();
  }

  private build(src: string) {
    const id = `pl${uid++}`;
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', `0 0 ${this.vbW} ${this.vbH}`);
    svg.setAttribute('aria-hidden', 'true');
    svg.innerHTML = `
      <defs>
        <clipPath id="${id}-c"><path /></clipPath>
        <linearGradient id="${id}-g" x1="1" y1="1" x2="0" y2="0">
          <stop offset="0" stop-color="#ffffff"/><stop offset="0.55" stop-color="#e3e7f2"/><stop offset="1" stop-color="#b9c0d4"/>
        </linearGradient>
        <filter id="${id}-b" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter>
      </defs>
      <path class="base" fill="#ffffff" style="filter:drop-shadow(0 6px 0 rgba(6,8,20,.9))"/>
      <image href="${src}" x="0" y="0" width="${this.vbW}" height="${this.vbH}" preserveAspectRatio="xMidYMid slice" clip-path="url(#${id}-c)"/>
      <g clip-path="url(#${id}-c)"><path class="shadow" fill="rgba(6,8,20,.38)" filter="url(#${id}-b)"/></g>
      <path class="flap" fill="url(#${id}-g)" stroke="url(#${id}-g)" stroke-width="2" stroke-linejoin="round"/>`;
    this.el.appendChild(svg);
    this.paths = {
      base: svg.querySelector('.base')!,
      clip: svg.querySelector(`#${id}-c path`)!,
      flap: svg.querySelector('.flap')!,
      shadow: svg.querySelector('.shadow')!,
    };
  }

  private render(f: number) {
    const W = this.vbW, H = this.vbH, r = this.r;
    const body =
      `M${r},0 H${W - r} A${r},${r} 0 0 1 ${W},${r} V${H - f} L${W - f},${H} H${r} A${r},${r} 0 0 1 0,${H - r} V${r} A${r},${r} 0 0 1 ${r},0 Z`;
    this.paths.base.setAttribute('d', body);
    this.paths.clip.setAttribute('d', body);
    // aba: canto (W,H) refletido na diagonal => (W-f, H-f)
    this.paths.flap.setAttribute('d', `M${W},${H - f} L${W - f},${H} L${W - f},${H - f} Z`);
    const o = 7;
    this.paths.shadow.setAttribute('d', `M${W},${H - f + o} L${W - f + o},${H} L${W - f - o},${H - f - o} Z`);
  }

  private scrollFold() {
    const rc = this.el.getBoundingClientRect();
    const vh = innerHeight;
    const p = clamp((vh * 0.98 - rc.top) / (vh * 0.55));
    return this.rest + (this.scrollMax - this.rest) * easeOutQuart(p);
  }

  private onScroll() {
    if (!this.scrollPeel || !this.visible || this.hovering || this.raf) return;
    const f = this.scrollFold();
    if (Math.abs(f - this.cur) > 0.01) { this.cur = this.from = this.to = f; this.render(f); }
  }

  private animateTo(v: number) {
    if (v === this.to) return;
    this.to = v; this.from = this.cur; this.t0 = performance.now();
    if (!this.raf) this.raf = requestAnimationFrame((t) => this.tick(t));
  }

  private tick(t: number) {
    const k = clamp((t - this.t0) / this.dur);
    this.cur = this.from + (this.to - this.from) * easeOutQuart(k);
    this.render(this.cur);
    this.raf = k < 1 ? requestAnimationFrame((n) => this.tick(n)) : 0;
  }

  private bind() {
    const on = () => { this.hovering = true; this.animateTo(this.hover); };
    const off = () => { this.hovering = false; this.animateTo(this.scrollPeel ? this.scrollFold() : this.rest); };
    const host = (this.el.closest('a') as HTMLElement | null) ?? this.el;
    host.addEventListener('mouseenter', on);
    host.addEventListener('mouseleave', off);
    host.addEventListener('focusin', on);
    host.addEventListener('focusout', off);
    host.addEventListener('touchstart', on, { passive: true });
    host.addEventListener('touchend', off);
    host.addEventListener('touchcancel', off);
  }
}

export function initPeel(reduce: boolean) {
  document.querySelectorAll<HTMLElement>('[data-peel]').forEach((el) => {
    if (reduce) { el.dataset.reduce = ''; return; }   // sem movimento: fica a foto simples
    new Peel(el);
  });
}
