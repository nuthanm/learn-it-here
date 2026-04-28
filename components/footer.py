import streamlit as st
import streamlit.components.v1 as components


def _footer_html() -> str:
    """In-flow footer — minimal muted text."""
    return """
<div class="kfp-footer">
  <span>© 2026 Learn It Here</span>
  <span>Built with Streamlit</span>
</div>
"""


def scroll_nav_html() -> str:
    """Return a full HTML document for components.html(height=0).

    Creates scroll-to-top / scroll-to-bottom buttons directly in the parent
    Streamlit page via ``window.parent.document`` so that ``position:fixed``
    is anchored to the viewport and the panda-theme CSS classes apply.
    Also creates mobile menu scroll arrows for horizontal radio strips.
    """
    return """<!DOCTYPE html>
<html>
<head>
<style>html,body{margin:0;padding:0;height:0;overflow:hidden;background:transparent}</style>
</head>
<body>
<script>
(function(){
  var pdoc = window.parent ? window.parent.document : document;
  var pwin = window.parent ? window.parent : window;

  /* ── Scroll-to-top / scroll-to-bottom buttons ── */
  function getOrCreate(id, content, bottom) {
    var btn = pdoc.getElementById(id);
    if (!btn) {
      btn = pdoc.createElement('button');
      btn.id = id;
      btn.type = 'button';
      btn.className = 'scroll-nav-btn';
      btn.title = id === 'snb-top' ? 'Scroll to top' : 'Scroll to bottom';
      btn.setAttribute('aria-label', btn.title);
      btn.innerHTML = content;
      btn.style.bottom = bottom;
      pdoc.body.appendChild(btn);
    }
    return btn;
  }

  var topBtn = getOrCreate('snb-top', '&#8679;', '5.6rem');
  var botBtn = getOrCreate('snb-bot', '&#8681;', '3.1rem');

  function findScrollEl() {
    var candidates = [
      pdoc.querySelector('[data-testid="stMain"]'),
      pdoc.querySelector('section.stMain'),
      pdoc.querySelector('section.main')
    ];
    for (var i = 0; i < candidates.length; i++) {
      var el = candidates[i];
      if (el && el.scrollHeight > el.clientHeight + 10) return el;
    }
    /* Return first existing candidate even if not yet scrollable */
    for (var j = 0; j < candidates.length; j++) {
      if (candidates[j]) return candidates[j];
    }
    return pdoc.documentElement;
  }

  function getScrollTop(el) {
    return el === pdoc.documentElement
      ? (pwin.pageYOffset || pwin.scrollY || el.scrollTop || 0)
      : (el.scrollTop || 0);
  }

  function getClientHeight(el) {
    return el === pdoc.documentElement
      ? (pwin.innerHeight || el.clientHeight || 0)
      : (el.clientHeight || 0);
  }

  function update() {
    var el = findScrollEl();
    var st = getScrollTop(el);
    var sh = el.scrollHeight || 0;
    var ch = getClientHeight(el);
    topBtn.classList.toggle('snb-visible', st > 80);
    botBtn.classList.toggle('snb-visible', st + ch < sh - 80);
  }

  function scrollPage(top) {
    var el = findScrollEl();
    var opts = {top: top, behavior: 'smooth'};
    if (el === pdoc.documentElement) {
      try { pwin.scrollTo(opts); } catch(e) { pdoc.documentElement.scrollTop = top; pdoc.body.scrollTop = top; }
    } else {
      try { el.scrollTo(opts); } catch(e) { el.scrollTop = top; }
    }
  }

  /* Replace buttons with fresh clones to clear any stale listeners */
  function refreshBtn(old) {
    var fresh = old.cloneNode(true);
    if (old.parentNode) {
      try { old.parentNode.replaceChild(fresh, old); } catch(e) { /* node removed by React re-render */ }
    }
    return fresh;
  }
  topBtn = refreshBtn(topBtn);
  botBtn = refreshBtn(botBtn);

  topBtn.addEventListener('click', function() { scrollPage(0); });
  botBtn.addEventListener('click', function() {
    var el = findScrollEl();
    scrollPage(el.scrollHeight - getClientHeight(el));
  });

  /* Attach scroll listeners broadly to catch all possible containers */
  var _listeningEls = {};
  function attachScrollListeners() {
    var el = findScrollEl();
    var elId = el.getAttribute('data-testid') || el.tagName || 'root';
    if (!_listeningEls[elId]) {
      el.addEventListener('scroll', update, {passive: true});
      _listeningEls[elId] = true;
    }
  }
  attachScrollListeners();
  pwin.addEventListener('scroll', update, {passive: true});
  update();

  /* Re-check periodically in case content loads late */
  var _retries = 0;
  var _interval = setInterval(function() {
    attachScrollListeners();
    update();
    _retries++;
    if (_retries > 15) clearInterval(_interval);
  }, 1000);

  /* Also watch for DOM changes */
  var _snbDebounce;
  var _snbObserver = new MutationObserver(function() {
    clearTimeout(_snbDebounce);
    _snbDebounce = setTimeout(function() {
      attachScrollListeners();
      update();
    }, 300);
  });
  _snbObserver.observe(pdoc.body, { childList: true, subtree: true });

  /* ── Mobile menu scroll arrows ── */
  function setupMenuArrows() {
    if (pwin.innerWidth > 768) return;
    var radioContainers = pdoc.querySelectorAll('div[data-testid="stRadio"]');
    radioContainers.forEach(function(radio) {
      var stripDiv = radio.querySelector(':scope > div:last-child');
      if (!stripDiv || stripDiv.dataset.arrowsSetup) return;
      stripDiv.dataset.arrowsSetup = '1';

      var wrapper = radio;
      wrapper.style.position = 'relative';

      function makeArrow(dir) {
        var a = pdoc.createElement('button');
        a.type = 'button';
        a.className = 'menu-scroll-arrow menu-scroll-' + dir;
        a.innerHTML = dir === 'left' ? '&#8249;' : '&#8250;';
        a.setAttribute('aria-label', 'Scroll menu ' + dir);
        a.style.display = 'none';
        wrapper.appendChild(a);
        return a;
      }

      var arrowL = makeArrow('left');
      var arrowR = makeArrow('right');

      function updateArrows() {
        var sl = stripDiv.scrollLeft;
        var sw = stripDiv.scrollWidth;
        var cw = stripDiv.clientWidth;
        if (sw <= cw + 5) {
          arrowL.style.display = 'none';
          arrowR.style.display = 'none';
          return;
        }
        arrowL.style.display = sl > 5 ? 'flex' : 'none';
        arrowR.style.display = sl + cw < sw - 5 ? 'flex' : 'none';
      }

      arrowL.addEventListener('click', function(e) {
        e.preventDefault(); e.stopPropagation();
        stripDiv.scrollBy({ left: -140, behavior: 'smooth' });
      });
      arrowR.addEventListener('click', function(e) {
        e.preventDefault(); e.stopPropagation();
        stripDiv.scrollBy({ left: 140, behavior: 'smooth' });
      });

      stripDiv.addEventListener('scroll', updateArrows, { passive: true });
      updateArrows();
      setTimeout(updateArrows, 500);
    });
  }

  setupMenuArrows();
  var _maDebounce;
  var _maObserver = new MutationObserver(function() {
    clearTimeout(_maDebounce);
    _maDebounce = setTimeout(setupMenuArrows, 300);
  });
  _maObserver.observe(pdoc.body, { childList: true, subtree: true });

  /* Re-run on resize so arrows appear when switching to mobile resolution */
  var _maResizeDebounce;
  pwin.addEventListener('resize', function() {
    clearTimeout(_maResizeDebounce);
    _maResizeDebounce = setTimeout(function() {
      /* Reset arrows setup flags so they can be re-created */
      var radios = pdoc.querySelectorAll('div[data-testid="stRadio"]');
      radios.forEach(function(radio) {
        var stripDiv = radio.querySelector(':scope > div:last-child');
        if (stripDiv) {
          /* Remove existing arrows if switching to desktop */
          if (pwin.innerWidth > 768) {
            radio.querySelectorAll('.menu-scroll-arrow').forEach(function(a) { a.remove(); });
            delete stripDiv.dataset.arrowsSetup;
          } else {
            /* If switching to mobile and not yet set up */
            if (!stripDiv.dataset.arrowsSetup) {
              setupMenuArrows();
            }
          }
        }
      });
      if (pwin.innerWidth <= 768) setupMenuArrows();
    }, 250);
  });

})();
</script>
</body>
</html>
"""


def copy_buttons_html() -> str:
    """Return a full HTML document for components.html(height=0).

    Injects a 'Copy' button into every ``.cmd-block`` and ``.json-block``
    in the parent Streamlit page via ``window.parent.document``. A
    MutationObserver re-runs the injection whenever Streamlit re-renders.
    """
    return """<!DOCTYPE html>
<html>
<head>
<style>html,body{margin:0;padding:0;height:0;overflow:hidden;background:transparent}</style>
</head>
<body>
<script>
(function(){
  var pdoc = window.parent ? window.parent.document : document;

  /* Strip the leading blank line and trailing whitespace that appear when
     <div class="cmd-block"> content starts/ends on its own line in the HTML
     source. Only div elements need this — <pre> blocks are already clean. */
  function trimBlockContent(block) {
    if (block.dataset.contentTrimmed || block.tagName.toLowerCase() !== 'div') return;
    block.dataset.contentTrimmed = '1';
    var fc = block.firstChild;
    if (fc && fc.nodeType === 3 && fc.nodeValue.charAt(0) === '\\n') {
      fc.nodeValue = fc.nodeValue.slice(1);
      if (!fc.nodeValue) { block.removeChild(fc); }
    }
    var lc = block.lastChild;
    if (lc && lc.nodeType === 3) {
      lc.nodeValue = lc.nodeValue.trimEnd ? lc.nodeValue.trimEnd() : lc.nodeValue;
      if (!lc.nodeValue) { block.removeChild(lc); }
    }
  }

  function addCopyButtons() {
    pdoc.querySelectorAll('.cmd-block, .json-block').forEach(function(block) {
      trimBlockContent(block);
      /* Skip blocks that already have a copy button injected. */
      if (block.querySelector('.copy-code-btn')) return;
      var btn = pdoc.createElement('button');
      btn.className = 'copy-code-btn';
      btn.textContent = 'Copy';
      btn.type = 'button';
      btn.setAttribute('aria-label', 'Copy code');
      btn.addEventListener('click', function() {
        /* Clone the block and strip the injected button before reading text. */
        var clone = block.cloneNode(true);
        var btnClone = clone.querySelector('.copy-code-btn');
        if (btnClone) { btnClone.parentNode.removeChild(btnClone); }
        var text = clone.innerText || clone.textContent || '';
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(function() {
            btn.textContent = 'Copied!';
            btn.classList.add('copied');
            setTimeout(function() { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
          }).catch(function() { fallbackCopy(text, btn); });
        } else {
          fallbackCopy(text, btn);
        }
      });
      /* Append the button directly inside the code block.
         The block already has position:relative via CSS so the button
         is positioned with position:absolute at top/right. This avoids
         rearranging React-managed DOM nodes (which caused NotFoundError). */
      block.appendChild(btn);
    });
  }

  function fallbackCopy(text, btn) {
    var ta = pdoc.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;top:-9999px;left:-9999px;opacity:0';
    pdoc.body.appendChild(ta);
    ta.focus();
    ta.select();
    try { pdoc.execCommand('copy'); } catch(e) {}
    pdoc.body.removeChild(ta);
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(function() { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
  }

  addCopyButtons();

  var debounceTimer;
  var observer = new MutationObserver(function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(addCopyButtons, 300); /* 300ms gives React time to finish re-rendering */
  });
  observer.observe(pdoc.body, { childList: true, subtree: true });
})();
</script>
</body>
</html>
"""


# Backwards-compatible aliases — older modules import the underscore names.
_footer_html = footer_html
_scroll_nav_html = scroll_nav_html
_copy_buttons_html = copy_buttons_html
