document.addEventListener("DOMContentLoaded", function() {
  // Velg tilfeldig side der knappen skal vises
  const allowedPages = ['/kalender/', '/arrangementer/', '/forside', '/s/om', '/', '/bokskap/', '/undergrupper/', '/utleie/sportskom/'];
  const randomPage = allowedPages[Math.floor(Math.random() * allowedPages.length)];
  
  // Vis bare knappen hvis vi er på den valgte siden
  if (!window.location.pathname.includes(randomPage)) {
    return;
  }

  const Shades = [
    "#11ff00ff", "#0227bdff", "#00a6ffff", "#dde503ff",
    "#0011ffff", "#00ff6eff", "#ef4ff7ff", "#81D4FA", "#ff0a0aff"
  ];

  const header = document.querySelector(".top-nav");
  const footer = document.querySelector("footer") || document.querySelector(".page-footer");
  const themeMeta = document.querySelector('meta[name="theme-color"]');
  const msNavMeta = document.querySelector('meta[name="msapplication-navbutton-color"]');
  const appleMeta = document.querySelector('meta[name="apple-mobile-web-app-status-bar-style"]');

  const originalHeaderColor = header ? getComputedStyle(header).backgroundColor : null;
  const originalFooterColor = footer ? getComputedStyle(footer).backgroundColor : null;
  const originalThemeColor = themeMeta ? themeMeta.getAttribute("content") : null;
  const originalMsColor = msNavMeta ? msNavMeta.getAttribute("content") : null;
  const originalAppleColor = appleMeta ? appleMeta.getAttribute("content") : null;

  function updateColor() {
    const random = Shades[Math.floor(Math.random() * Shades.length)];
    if (header) header.style.backgroundColor = random;
    if (footer) footer.style.backgroundColor = random;
    if (themeMeta) themeMeta.setAttribute("content", random);
    if (msNavMeta) msNavMeta.setAttribute("content", random);
    if (appleMeta) appleMeta.setAttribute("content", random);
  }

  function resetColor() {
    if (header) header.style.backgroundColor = originalHeaderColor;
    if (footer) footer.style.backgroundColor = originalFooterColor;
    if (themeMeta) themeMeta.setAttribute("content", originalThemeColor);
    if (msNavMeta) msNavMeta.setAttribute("content", originalMsColor);
    if (appleMeta) appleMeta.setAttribute("content", originalAppleColor);
  }

  // Lag sticky knapp inne i header
  const fabDiv = document.createElement("div");
  fabDiv.style.position = "absolute"; // absolute i header fungerer best
  fabDiv.style.top = "24px";
  fabDiv.style.right = "24px";
  fabDiv.style.zIndex = "1000";

    const fabLink = document.createElement("a");
    fabLink.className = "btn-floating btn-large red"; 
    fabLink.innerHTML = '<i class="material-icons">celebration</i>';
    fabLink.style.boxShadow = "none";
      fabLink.href = "javascript:void(0)";
      fabLink.setAttribute('role', 'button');
      fabLink.setAttribute('tabindex', '0');
      fabLink.style.cursor = 'pointer';


  fabDiv.appendChild(fabLink);
  if (header) header.appendChild(fabDiv);

  // Event listener with confirmation
  function startRandomHeader(e) {
      if (e && typeof e.preventDefault === 'function') e.preventDefault();
      console.log('random_header_click: clicked');
      if (!confirm("Epiplepsi? Dette er en advarsel.")) {
        console.log('random_header_click: cancelled');
        return;
      }
      console.log('random_header_click: confirmed');
      const interval = setInterval(updateColor, 1);
      setTimeout(() => {
        clearInterval(interval);
        resetColor();
      }, 5000);
    }

    fabLink.addEventListener("click", startRandomHeader);
    fabLink.addEventListener("keydown", function(e) {
      if (e.key === 'Enter' || e.key === ' ') startRandomHeader(e);
  });
});
