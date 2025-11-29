document.addEventListener("DOMContentLoaded", function () {
  const candleConfig = {
    component: "headerCandles",
    version: 1,
    targetSelector: "#hc-header-candles",
    layout: {
      orientation: "row",
      gapPx: 16,
      align: "center"
    },
    candles: [
      { id: "candle-1", label: "Lys 1", order: 1 },
      { id: "candle-2", label: "Lys 2", order: 2 },
      { id: "candle-3", label: "Lys 3", order: 3 },
      { id: "candle-4", label: "Lys 4", order: 4 }
    ],
    style: {
      holderWidthPx: 40,
      holderHeightPx: 8,
      emojiSizePx: 26,
      goldStart: "#c49a3a",
      goldMid:   "#f3d27a",
      goldEnd:   "#8a6512"
    },
    accessibility: {
      role: "group",
      ariaLabel: "Fire adventslys i headeren"
    }
  };

  // Skalering for ulike skjermbredder
  function getScale() {
    const w = window.innerWidth;
    if (w <= 480) return 0.65;
    if (w <= 768) return 0.8;
    if (w <= 1200) return 0.9;
    return 1.0;
  }

  const scale = getScale();
  const isMobile = window.innerWidth <= 480;

  function getAdventSundays(year) {
    const christmas = new Date(year, 11, 25);
    const lastSunday = new Date(christmas);
    const day = lastSunday.getDay(); // 0 = søndag
    const diffToSunday = (day + 7 - 0) % 7;
    lastSunday.setDate(lastSunday.getDate() - diffToSunday);
    lastSunday.setHours(0, 0, 0, 0);

    const adventSundays = [];
    for (let i = 3; i >= 0; i--) {
      const d = new Date(lastSunday);
      d.setDate(d.getDate() - 7 * i);
      d.setHours(0, 0, 0, 0);
      adventSundays.push(d);
    }
    return adventSundays;
  }

  function getAdventLitCount(today = new Date()) {
    const year = today.getFullYear();
    const adventSundays = getAdventSundays(year);

    const t = new Date(today);
    t.setHours(0, 0, 0, 0);

    let count = 0;
    for (const s of adventSundays) {
      if (t >= s) count++;
    }
    if (count < 0) count = 0;
    if (count > 4) count = 4;
    return count;
  }

  function isAdventSunday(today = new Date()) {
    const year = today.getFullYear();
    const adventSundays = getAdventSundays(year);
git 
    const t = new Date(today);
    t.setHours(0, 0, 0, 0);
    const tTime = t.getTime();

    return adventSundays.some((s) => s.getTime() === tTime);
  }

  // antall tente lys
  const litCount = getAdventLitCount();

  const root = document.querySelector(candleConfig.targetSelector);
  if (!root) return;

  const adventPurple = "#3b145c";

  const nav = document.querySelector(".top-nav");
  if (nav) {
    nav.style.position = "relative";
  }

  // header + footer advent-lilla på adventssøndager
  if (isAdventSunday()) {
    if (nav) {
      nav.style.backgroundColor = adventPurple;
    }
    const footer = document.querySelector("footer, .page-footer");
    if (footer) {
      footer.style.backgroundColor = adventPurple;
    }
  }

  root.setAttribute("role", candleConfig.accessibility.role);
  root.setAttribute("aria-label", candleConfig.accessibility.ariaLabel);

  // Layout av containeren
  root.style.display = "flex";
  root.style.flexDirection =
    candleConfig.layout.orientation === "row" ? "row" : "column";
  root.style.alignItems = candleConfig.layout.align;
  root.style.justifyContent = "flex-end";
  root.style.gap = (candleConfig.layout.gapPx * scale) + "px";

  // Plassering: absolutt på desktop, vanlig flow på mobil
  if (isMobile) {
    root.style.position = "static";
    root.style.top = "";
    root.style.right = "";
    root.style.transform = "";
    root.style.marginTop = "4px";
    root.style.alignSelf = "flex-end";
  } else {
    root.style.position = "absolute";
    root.style.top = "75%";
    root.style.right = (32 * scale) + "px";
    root.style.transform = "translateY(-50%)";
    root.style.marginTop = "0";
  }

  // skalerte størrelser
  const holderWidth  = candleConfig.style.holderWidthPx * scale;
  const holderHeight = candleConfig.style.holderHeightPx * scale;
  const emojiSize    = candleConfig.style.emojiSizePx * scale;

  // fast høyde på "flamme-slot" over holderen,
  // slik at holderen alltid står på samme vertikale posisjon
  const flameAreaHeight = emojiSize + (6 * scale);

  // generer lys
  candleConfig.candles
    .slice()
    .sort((a, b) => a.order - b.order)
    .forEach((candle, index) => {
      const candleWrapper = document.createElement("div");
      candleWrapper.style.display = "flex";
      candleWrapper.style.flexDirection = "column";
      candleWrapper.style.alignItems = "center";

      // flamme-slot med fast høyde
      const flameSlot = document.createElement("div");
      flameSlot.style.height = flameAreaHeight + "px";
      flameSlot.style.display = "flex";
      flameSlot.style.alignItems = "flex-end";
      flameSlot.style.justifyContent = "center";

      if (index < litCount) {
        const flame = document.createElement("div");
        flame.textContent = "🕯️";
        flame.style.fontSize = emojiSize + "px";
        flame.style.lineHeight = "1";
        flameSlot.appendChild(flame);
      }
      // hvis ikke tent lys, lar vi flameSlot være tom,
      // men høyden er den samme, så holderen havner på samme posisjon

      candleWrapper.appendChild(flameSlot);

      const plate = document.createElement("div");
      plate.style.width = holderWidth + "px";
      plate.style.height = holderHeight + "px";
      plate.style.borderRadius = "999px";
      plate.style.background =
        "linear-gradient(90deg," +
        candleConfig.style.goldStart + "," +
        candleConfig.style.goldMid + "," +
        candleConfig.style.goldEnd + ")";
      plate.style.boxShadow =
        "0 1px 2px rgba(0,0,0,0.35), 0 0 0 " + (1 * scale) + "px rgba(0,0,0,0.18)";

      candleWrapper.appendChild(plate);
      root.appendChild(candleWrapper);
    });
});
