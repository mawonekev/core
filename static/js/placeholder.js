/**
 * placeholder.js — Image placeholder & error handling utilities
 *
 * Provides:
 *  - imgPlaceholder(label)  → data URI of an SVG "no image" boilerplate with grid pattern
 *  - initImageErrorHandling() → attaches global onerror to all <img> elements
 *  - skeletonImg()          → returns HTML string for a skeleton loader image cell
 */

/** Build a compact SVG data-URI placeholder with a grid/tile pattern and optional label */
export function imgPlaceholder(label = '') {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
    <defs>
      <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
        <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#D6C4A0" stroke-width="0.5" opacity="0.6"/>
      </pattern>
      <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#F5E6C8;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#EDD9A3;stop-opacity:1" />
      </linearGradient>
    </defs>
    <!-- Background -->
    <rect width="400" height="300" fill="url(#bg)"/>
    <!-- Grid overlay -->
    <rect width="400" height="300" fill="url(#grid)"/>
    <!-- Border -->
    <rect width="400" height="300" fill="none" stroke="#C8903A" stroke-width="1" opacity="0.3"/>
    <!-- Camera icon group (centered) -->
    <g transform="translate(176, 110)" opacity="0.4">
      <!-- Camera body -->
      <rect x="0" y="10" width="48" height="34" rx="5" fill="#8B5E3C"/>
      <!-- Lens outer -->
      <circle cx="24" cy="27" r="11" fill="#6B4A2C"/>
      <!-- Lens inner -->
      <circle cx="24" cy="27" r="7" fill="#8B5E3C" opacity="0.7"/>
      <!-- Lens highlight -->
      <circle cx="24" cy="27" r="4" fill="#C8903A" opacity="0.5"/>
      <!-- Flash bump -->
      <rect x="6" y="5" width="10" height="7" rx="2" fill="#8B5E3C"/>
      <!-- Shutter button -->
      <circle cx="38" cy="14" r="3" fill="#8B5E3C"/>
    </g>
    ${label ? `<!-- Label --><text x="200" y="220" text-anchor="middle" font-family="DM Sans, sans-serif" font-size="13" fill="#8B5E3C" opacity="0.7">${label}</text>` : ''}
    <!-- "No image" text -->
    <text x="200" y="${label ? '240' : '230'}" text-anchor="middle" font-family="DM Sans, sans-serif" font-size="12" fill="#8B5E3C" opacity="0.5">Image not available</text>
  </svg>`;
  return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
}

/**
 * Returns a wider/shorter placeholder for hero-style containers
 * (1200×500, widescreen ratio)
 */
export function heroBannerPlaceholder(label = '') {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 500" width="1200" height="500">
    <defs>
      <pattern id="topo" width="40" height="40" patternUnits="userSpaceOnUse">
        <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#C8903A" stroke-width="0.4" opacity="0.25"/>
        <circle cx="20" cy="20" r="8" fill="none" stroke="#C8903A" stroke-width="0.3" opacity="0.2"/>
      </pattern>
      <linearGradient id="heroBg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#1A4731;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#2D6A4F;stop-opacity:1" />
      </linearGradient>
    </defs>
    <rect width="1200" height="500" fill="url(#heroBg)"/>
    <rect width="1200" height="500" fill="url(#topo)"/>
    <!-- Camera icon -->
    <g transform="translate(572, 185)" opacity="0.25">
      <rect x="0" y="12" width="56" height="40" rx="6" fill="white"/>
      <circle cx="28" cy="32" r="13" fill="white" opacity="0.8"/>
      <circle cx="28" cy="32" r="8" fill="#1A4731" opacity="0.6"/>
      <rect x="8" y="5" width="12" height="9" rx="3" fill="white"/>
    </g>
    ${label ? `<text x="600" y="285" text-anchor="middle" font-family="DM Sans, sans-serif" font-size="16" fill="white" opacity="0.5">${label}</text>` : ''}
    <text x="600" y="${label ? '310' : '295'}" text-anchor="middle" font-family="DM Sans, sans-serif" font-size="13" fill="white" opacity="0.35">Image coming soon</text>
  </svg>`;
  return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
}

/** Returns HTML string for a skeleton loader that fills its container */
export function skeletonImgHTML(classes = '') {
  return `<div class="skeleton-img ${classes}" aria-hidden="true" role="presentation"></div>`;
}

/**
 * Attach onerror handler to all current and future img elements.
 * Broken images are swapped for the SVG placeholder.
 * Call once on DOMContentLoaded.
 */
export function initImageErrorHandling() {
  // Handle already-present images
  document.querySelectorAll('img[data-fallback="placeholder"]').forEach(attachFallback);

  // Use MutationObserver for dynamically-added images
  const mo = new MutationObserver(mutations => {
    mutations.forEach(m => m.addedNodes.forEach(node => {
      if (node.nodeType !== 1) return;
      if (node.tagName === 'IMG') attachFallback(node);
      node.querySelectorAll?.('img').forEach(attachFallback);
    }));
  });
  mo.observe(document.body, { childList: true, subtree: true });
}

function attachFallback(img) {
  if (img._placeholderAttached) return;
  img._placeholderAttached = true;
  img.addEventListener('error', () => {
    if (img.src !== imgPlaceholder()) {
      img.src = imgPlaceholder(img.alt || '');
      img.classList.add('img-error');
    }
  }, { once: true });
}

/**
 * Returns a graceful "failed to load" section for data errors (weather, API, etc.)
 * Drops into any container via innerHTML.
 */
export function errorStateHTML({ icon = 'wifi-off', title = 'Failed to load', message = 'Something went wrong. Please try again.', retryId = '', retryText = 'Try Again' } = {}) {
  return `
    <div class="flex flex-col items-center justify-center py-16 px-6 text-center gap-4">
      <div class="w-16 h-16 rounded-full bg-tz-sand flex items-center justify-center">
        <i data-lucide="${icon}" class="w-8 h-8 text-tz-earth" aria-hidden="true"></i>
      </div>
      <div>
        <p class="font-semibold text-tz-dark text-lg">${title}</p>
        <p class="text-tz-muted text-sm mt-1 max-w-xs mx-auto">${message}</p>
      </div>
      ${retryId ? `<button id="${retryId}" class="mt-2 inline-flex items-center gap-2 bg-tz-forest text-white text-sm font-semibold px-5 py-2.5 rounded-full hover:bg-tz-forest/90 transition-colors">
        <i data-lucide="refresh-cw" class="w-4 h-4" aria-hidden="true"></i>${retryText}
      </button>` : ''}
    </div>
  `;
}

/**
 * Returns HTML for an empty-state (no results / coming soon).
 */
export function emptyStateHTML({ icon = 'inbox', title = 'Nothing here yet', message = 'Check back soon.' } = {}) {
  return `
    <div class="flex flex-col items-center justify-center py-16 px-6 text-center gap-4">
      <div class="w-16 h-16 rounded-full bg-tz-sand flex items-center justify-center">
        <i data-lucide="${icon}" class="w-8 h-8 text-tz-savanna" aria-hidden="true"></i>
      </div>
      <div>
        <p class="font-semibold text-tz-dark text-lg">${title}</p>
        <p class="text-tz-muted text-sm mt-1 max-w-xs mx-auto">${message}</p>
      </div>
    </div>
  `;
}
