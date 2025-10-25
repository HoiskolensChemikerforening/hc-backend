document.addEventListener("DOMContentLoaded", function() {
  const Shades = [
    "#218fbeff", "#0227bdff", "#0288D1", "#039BE5", 
    "#0c126fff", "#29B6F6", "#1c337dff", "#5175daff", "#01579B"
  ];

  const header = document.querySelector(".top-nav");
  const footer = document.querySelector("footer") || document.querySelector(".page-footer");
  const themeMeta = document.querySelector('meta[name="theme-color"]');
  const msNavMeta = document.querySelector('meta[name="msapplication-navbutton-color"]');
  const appleMeta = document.querySelector('meta[name="apple-mobile-web-app-status-bar-style"]');

  // Velger en tilfeldig farge
  const random = Shades[Math.floor(Math.random() * Shades.length)];

  if (header) header.style.backgroundColor = random;
  if (footer) footer.style.backgroundColor = random;
  if (themeMeta) themeMeta.setAttribute("content", random);
  if (msNavMeta) msNavMeta.setAttribute("content", random);
  if (appleMeta) appleMeta.setAttribute("content", random);
});
