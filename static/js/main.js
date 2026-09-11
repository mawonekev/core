/**
 * main.js — Xenohuru Django shared JS
 * Replaces PWA scripts.js; no ES module imports needed.
 */
document.addEventListener('DOMContentLoaded', () => {

  /* ─── Lucide Icons ─── */
  if (typeof lucide !== 'undefined') lucide.createIcons();

  /* ─── AOS ─── */
  if (typeof AOS !== 'undefined') {
    AOS.init({ duration: 700, easing: 'ease-out-cubic', once: true, offset: 60 });
  }

  /* ─── Preloader ─── */
  const preloader = document.querySelector('.preloader');
  if (preloader) {
    const hide = () => preloader.classList.add('hidden');
    if (document.readyState === 'complete') hide();
    else { window.addEventListener('load', hide); setTimeout(hide, 3000); }
  }

  /* ─── Navbar scroll glassmorphism ─── */
  const mainNav = document.getElementById('main-nav');
  if (mainNav) {
    const onScroll = () => {
      const s = window.scrollY > 60;
      mainNav.classList.toggle('navbar-scrolled', s);
      mainNav.querySelectorAll('.nav-link:not(.active-nav)').forEach(l => {
        l.classList.toggle('text-white/80', !s);
        l.classList.toggle('text-tz-dark/70', s);
      });
      mainNav.querySelectorAll('.nav-link.active-nav').forEach(l => {
        l.classList.toggle('text-white/90', !s);
        l.classList.toggle('text-tz-savanna', s);
      });
      const hb = document.getElementById('mobile-toggle');
      if (hb) { hb.classList.toggle('text-white', !s); hb.classList.toggle('text-tz-dark', s); }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ─── Mobile drawer ─── */
  const mobileToggle  = document.getElementById('mobile-toggle');
  const mobileClose   = document.getElementById('mobile-close');
  const mobileDrawer  = document.getElementById('mobile-drawer');
  const mobileOverlay = document.getElementById('mobile-overlay');

  function openMenu() {
    mobileDrawer?.classList.add('active');
    mobileOverlay?.classList.add('active');
    mobileToggle?.setAttribute('aria-expanded', 'true');
    mobileDrawer?.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }
  function closeMenu() {
    mobileDrawer?.classList.remove('active');
    mobileOverlay?.classList.remove('active');
    mobileToggle?.setAttribute('aria-expanded', 'false');
    mobileDrawer?.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }
  mobileToggle?.addEventListener('click', openMenu);
  mobileClose?.addEventListener('click', closeMenu);
  mobileOverlay?.addEventListener('click', closeMenu);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });

  /* ─── Live EAT clock ─── */
  function updateTime() {
    const now = new Date().toLocaleTimeString('en-GB', { timeZone: 'Africa/Dar_es_Salaam', hour12: false });
    document.getElementById('nav-time') && (document.getElementById('nav-time').textContent = now);
    document.getElementById('footer-time') && (document.getElementById('footer-time').textContent = now + ' EAT');
  }
  updateTime();
  setInterval(updateTime, 1000);

  /* ─── Footer year ─── */
  const yr = document.getElementById('current-year');
  if (yr) yr.textContent = new Date().getFullYear();

  /* ─── Back to top ─── */
  const btt = document.getElementById('back-to-top');
  if (btt) {
    window.addEventListener('scroll', () => btt.classList.toggle('visible', window.scrollY > 400), { passive: true });
    btt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  /* ─── Image error fallback ─── */
  document.querySelectorAll('img[data-src-fallback]').forEach(img => {
    img.addEventListener('error', function () {
      this.src = this.dataset.srcFallback || '';
      this.classList.add('img-error');
    });
  });

  /* ─── Image reveal on scroll ─── */
  document.querySelectorAll('.reveal-image').forEach(el => {
    const ro = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('revealed'); ro.unobserve(e.target); } });
    }, { threshold: 0.2 });
    ro.observe(el);
  });

  /* ─── Rotating Swahili quotes ─── */
  const rq = document.getElementById('rotating-quote');
  if (rq) {
    const QS = [
      '"Safari njema" — Have a good journey',
      '"Hakuna Matata" — No worries',
      '"Karibu Tanzania" — Welcome to Tanzania',
      '"Asante sana" — Thank you very much',
      '"Jambo!" — Hello!',
      '"Twende safari" — Let us go on a journey',
    ];
    let qi = 0;
    rq.style.transition = 'opacity 0.4s ease';
    setInterval(() => {
      qi = (qi + 1) % QS.length;
      rq.style.opacity = '0';
      setTimeout(() => { rq.textContent = QS[qi]; rq.style.opacity = '1'; }, 400);
    }, 5000);
  }

  /* ─── Animated stat counters ─── */
  document.querySelectorAll('[data-count]').forEach(el => {
    const target = parseInt(el.dataset.count, 10);
    const duration = 1800;
    const step = target / (duration / 16);
    let current = 0;
    const ro = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) {
        const timer = setInterval(() => {
          current = Math.min(current + step, target);
          el.textContent = Math.floor(current).toLocaleString() + (el.dataset.suffix || '');
          if (current >= target) clearInterval(timer);
        }, 16);
        ro.unobserve(el);
      }
    });
    ro.observe(el);
  });

  /* ─── Google Translate EN/SW ─── */
  if (!document.getElementById('google_translate_element')) {
    const div = document.createElement('div');
    div.id = 'google_translate_element';
    div.style.display = 'none';
    document.body.appendChild(div);
  }
  window.googleTranslateElementInit = function () {
    if (typeof google === 'undefined' || !google.translate) return;
    new google.translate.TranslateElement(
      { pageLanguage: 'en', includedLanguages: 'en,sw', autoDisplay: false },
      'google_translate_element'
    );
  };
  if (!document.querySelector('script[src*="translate.google.com"]')) {
    const s = document.createElement('script');
    s.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    s.async = true;
    document.head.appendChild(s);
  }
  const savedLang = localStorage.getItem('tz-lang') || 'en';
  document.querySelectorAll('#lang-switcher').forEach(sel => {
    sel.value = savedLang;
    sel.addEventListener('change', e => {
      const v = e.target.value;
      const cv = v === 'sw' ? '/en/sw' : '/en/en';
      document.cookie = `googtrans=${cv}; path=/`;
      localStorage.setItem('tz-lang', v);
      window.location.reload();
    });
  });

});
