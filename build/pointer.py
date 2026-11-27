"""The board pointer (27 November 2026): for a teacher projecting the site, a bright ring where the mouse is, or where a
finger or pen touches the screen, so the room can follow what is being pointed at, buttons or not.

Off by default, switched on with the Pointer button (in the header, and in each deck's controls) or the P key, and
remembered on that device: on a laptop or iPad used for projecting it stays on, and anyone else reading the site never
sees it. The ring passes every click and tap through to the page. A mouse moves it all the time; a touch shows it,
follows the finger, and fades a moment after the finger lifts. In a deck, while it is on, a tap points instead of
moving the slide on; the arrows, keys and buttons still move it."""

BUTTON = '<button type="button" class="ptr-btn" data-ptr aria-pressed="false" title="Pointer for the board (P)" hidden>Pointer</button>'
DECK_BUTTON = '<button data-ptr aria-pressed="false" title="Pointer for the board (P)" aria-label="Pointer for the board">&#9678;</button>'

SCRIPT = """<style>
#lm-ptr{position:fixed;left:0;top:0;width:66px;height:66px;margin:-33px 0 0 -33px;border-radius:50%;box-sizing:border-box;
 border:6px solid #ff4d1a;background:rgba(255,77,26,.16);box-shadow:0 0 0 3px rgba(255,255,255,.95),0 0 22px 4px rgba(255,77,26,.55);
 pointer-events:none;z-index:2147483647;opacity:0;transition:opacity .3s ease}
#lm-ptr.on{opacity:1}
#lm-ptr.press{animation:lm-ptr-press .35s ease-out}
@keyframes lm-ptr-press{0%{scale:1}40%{scale:1.35}100%{scale:1}}
@media (prefers-reduced-motion:reduce){#lm-ptr.press{animation:none}}
html.ptr-on [data-ptr]{background:#ff4d1a!important;color:#fff!important;border-color:#ff4d1a!important}
</style>
<script>(() => {
  const root = document.documentElement, KEY = 'lm-pointer';
  let on = false; try { on = localStorage.getItem(KEY) === 'on'; } catch (e) {}
  const ring = document.createElement('div'); ring.id = 'lm-ptr'; ring.setAttribute('aria-hidden', 'true');
  let fade = null;
  const place = (x, y) => { ring.style.transform = 'translate(' + x + 'px,' + y + 'px)'; };
  const show = () => { clearTimeout(fade); ring.classList.add('on'); };
  const hideSoon = ms => { clearTimeout(fade); fade = setTimeout(() => ring.classList.remove('on'), ms); };
  function set(v) {
    on = v; root.classList.toggle('ptr-on', on);
    document.querySelectorAll('[data-ptr]').forEach(b => { b.hidden = false; b.setAttribute('aria-pressed', on); });
    if (!on) ring.classList.remove('on');
    try { localStorage.setItem(KEY, on ? 'on' : 'off'); } catch (e) {}
  }
  function ready() {
    document.body.appendChild(ring); set(on);
    document.addEventListener('click', e => { const b = e.target.closest('[data-ptr]'); if (b) { e.stopPropagation(); set(!on); } }, true);
  }
  if (document.body) ready(); else document.addEventListener('DOMContentLoaded', ready);
  addEventListener('pointermove', e => { if (!on) return; place(e.clientX, e.clientY); if (e.pointerType === 'mouse') show(); }, { passive: true });
  addEventListener('pointerdown', e => { if (!on) return; place(e.clientX, e.clientY); show();
    ring.classList.remove('press'); void ring.offsetWidth; ring.classList.add('press'); }, { passive: true });
  addEventListener('pointerup', e => { if (on && e.pointerType !== 'mouse') hideSoon(1500); }, { passive: true });
  addEventListener('pointercancel', e => { if (on && e.pointerType !== 'mouse') hideSoon(1500); }, { passive: true });
  // a finger that scrolls the page: the browser stops sending pointer events, so follow the touch itself
  addEventListener('touchmove', e => { if (!on) return; const t = e.touches[0]; if (t) { place(t.clientX, t.clientY); show(); } }, { passive: true });
  // in a deck a tap or a swipe moves the slide on; while the pointer is on, a tap points instead (the arrows, the
  // keys and the deck's own buttons still move it)
  const deck = () => document.getElementById('controls') && document.getElementById('stage');
  const free = e => e.target.closest && e.target.closest('#controls, a, button, input, label, [data-ptr]');
  addEventListener('click', e => { if (on && deck() && !free(e)) e.stopPropagation(); }, true);
  addEventListener('touchend', e => { if (!on) return; hideSoon(1500); if (deck() && !free(e)) e.stopPropagation(); }, { capture: true, passive: true });
  document.addEventListener('mouseleave', () => { if (on) ring.classList.remove('on'); });
  addEventListener('keydown', e => {
    if ((e.key === 'p' || e.key === 'P') && !e.metaKey && !e.ctrlKey && !e.altKey && !e.target.closest('input, textarea, select, [contenteditable]')) set(!on);
  });
})();</script>"""
