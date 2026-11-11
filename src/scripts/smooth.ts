import Lenis from 'lenis';

/** Rolagem suave (Lenis, lerp 0.1) sem GSAP, para páginas que não usam ScrollTrigger. Desligada em "reduzir movimento". */
export function initSmooth() {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const lenis = new Lenis({ lerp: 0.1 });
  const raf = (t: number) => { lenis.raf(t); requestAnimationFrame(raf); };
  requestAnimationFrame(raf);
}
