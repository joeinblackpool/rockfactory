// Motion layer: scroll reveals, scroll-reactive marquee, custom cursor and magnetic buttons.
// Everything is progressive: without JavaScript, or with reduced motion, the page is complete and static.
// SEO-safe by design: no text is added or rewritten, the headline and hero photo never move (they set the page's
// load-speed score), and animations use transform/opacity only, so nothing shifts the layout.
(() => {
  const root = document.documentElement;
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine = matchMedia("(hover: hover) and (pointer: fine)").matches;

  // Marquee before the footer. It drifts on its own and speeds up (or reverses) with scrolling.
  const footer = document.querySelector(".site-footer-mega");
  let track = null;
  if (footer) {
    const strip = document.createElement("div");
    strip.className = "marquee";
    strip.setAttribute("aria-hidden", "true");
    const words = ["Move in", "Plug in", "Start trading", "Blackpool Rock Factory"];
    const run = words.map((w) => `<span data-w="${w}"></span><i></i>`).join("");  // drawn by CSS, so it is not page text
    strip.innerHTML = `<div class="marquee-track">${run.repeat(4)}</div>`;
    footer.before(strip);
    root.classList.add("has-marquee");
    track = strip.firstElementChild;
  }

  if (reduced) return;
  root.classList.add("motion");

  // Scroll reveals. Anything already on screen at load is left alone, so nothing flickers.
  const sel = [".section-head", ".space-card", ".who-card", ".idea-card", ".biz-card", ".unit-card", ".facility", ".feature",
    ".archive-print", ".page-photo", ".photo-gallery img", ".table-wrap", ".faq-list details", ".steps li", ".opening-card",
    ".callout", ".guide-content > h2", ".idea", ".contrast li", ".quick", ".answer-box"].join(",");
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add("in");
      io.unobserve(e.target);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
  const vh = innerHeight;
  document.querySelectorAll(sel).forEach((el) => {
    if (el.getBoundingClientRect().top < vh * 0.92) return;
    const sibs = el.parentElement ? [...el.parentElement.children].filter((c) => c.matches(sel)) : [];
    el.style.setProperty("--d", `${Math.min(sibs.indexOf(el), 5) * 70}ms`);
    el.classList.add("reveal");
    io.observe(el);
  });

  // One animation frame loop: marquee, gentle parallax on big photos.
  let x = 0, last = scrollY, v = 0;
  const par = [...document.querySelectorAll(".archive-floor img, .archive-cut img, .archive-rolling img")];
  const tick = () => {
    const y = scrollY, dy = y - last; last = y;
    v += (dy - v) * 0.12;
    if (track) {
      x -= 0.6 + Math.abs(v) * 0.35;
      const w = track.scrollWidth / 4;
      if (-x >= w) x += w;
      track.style.transform = `translate3d(${x}px,0,0) skewX(${Math.max(-12, Math.min(12, -v * 0.5))}deg)`;
    }
    for (const img of par) {
      const r = img.getBoundingClientRect();
      if (r.bottom < 0 || r.top > innerHeight) continue;
      const p = (r.top + r.height / 2 - innerHeight / 2) / innerHeight;
      img.style.transform = `translate3d(0,${(p * -28).toFixed(1)}px,0) scale(1.08)`;
    }
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);

  if (!fine) return;

  // Custom cursor: a red dot, and a ring that grows over links and says "view" over photographs.
  const dot = document.createElement("div"), ring = document.createElement("div");
  dot.className = "cursor-dot"; ring.className = "cursor-ring";
  ring.innerHTML = "<span></span>";
  document.body.append(ring, dot);
  root.classList.add("has-cursor");
  let mx = innerWidth / 2, my = innerHeight / 2, rx = mx, ry = my;
  addEventListener("pointermove", (e) => {
    mx = e.clientX; my = e.clientY;
    dot.style.transform = `translate3d(${mx}px,${my}px,0)`;
    const t = e.target.closest ? e.target : null;
    const photo = t && t.closest(".archive-print a, .home-unit-photo a, .page-photo a, .photo-gallery a");
    const link = t && t.closest("a, button, summary, label, select, input");
    ring.classList.toggle("is-link", !!link && !photo);
    ring.classList.toggle("is-photo", !!photo);
    ring.firstChild.textContent = photo ? "view" : "";
    dot.classList.toggle("is-hidden", !!photo);
  }, { passive: true });
  addEventListener("pointerdown", () => ring.classList.add("is-down"));
  addEventListener("pointerup", () => ring.classList.remove("is-down"));
  document.addEventListener("pointerleave", () => root.classList.add("cursor-out"));
  document.addEventListener("pointerenter", () => root.classList.remove("cursor-out"));
  const follow = () => {
    rx += (mx - rx) * 0.18; ry += (my - ry) * 0.18;
    ring.style.transform = `translate3d(${rx}px,${ry}px,0)`;
    requestAnimationFrame(follow);
  };
  requestAnimationFrame(follow);

  // Magnetic buttons: they lean towards the pointer a little.
  document.querySelectorAll(".button, .whatsapp-link").forEach((b) => {
    b.addEventListener("pointermove", (e) => {
      const r = b.getBoundingClientRect();
      b.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * 0.18}px, ${(e.clientY - r.top - r.height / 2) * 0.28}px)`;
    });
    b.addEventListener("pointerleave", () => { b.style.transform = ""; });
  });
})();
