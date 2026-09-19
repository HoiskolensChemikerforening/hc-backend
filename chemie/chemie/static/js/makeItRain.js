const christmasSymbols = ["❄️", "❄️", "❄️"]; // add in emojis after every Advent "🎄", "🤶", "🎅", "⛄️"
const easterSymbols = ["🐰", "🗿", "🐥", "🐣"];
const breastCancerSymbols = ["🎀", "🌸", "💗"];
const blueCancerSymbols = [ "🙍‍♂️", "💙", "🫐", " 🍆", " "];
const valentinesSymbols = ["❤️", "🌹", "💘", "👼", "💌", "💋", "🏹"];
const halloweenSymbols = ["🎃", "🎃", "🎃", "🕷️", "👻", "🪦", "⚰️", "🕸️", "🦇"];
const webkomSymbols = ["Søk Webkom!", "Søknadsfrist:<br/>27.09.26","Webkom har opptak!", "💻", "🔌", "👩‍💻", "👨‍💻","🍰",,"🎤", "❤️","../../static/images/holiday_images/webkom.png"];
const paulImages = ["../../static/images/holiday_images/paul.png", "../../static/images/holiday_images/paul_tullebilde.png"];
const mustacheNovemberImages = [
  "../../static/images/holiday_images/bart1.png",
  "../../static/images/holiday_images/bart2.png",
  "../../static/images/holiday_images/bart3.png",
  "../../static/images/holiday_images/bart4.png",
  "../../static/images/holiday_images/bart5.png",
  "../../static/images/holiday_images/bart6.png", "💙", "💙", "💙", 
];

const rainSpeed = 20; // Adjust this value to set the rain speed

function selectSymbols(choose_your_holiday) {
  if (choose_your_holiday === "christmas") {
    return christmasSymbols;
  } else if (choose_your_holiday === "easter") {
    return easterSymbols;
  } else if (choose_your_holiday === "breast cancer") {
    return breastCancerSymbols;
    } else if (choose_your_holiday === "blue cancer") {
    return blueCancerSymbols;
  } else if (choose_your_holiday === "halloween") {
    return halloweenSymbols;
  } else if (choose_your_holiday === "pauloween") {
    return paulImages;
  } else if (choose_your_holiday === "mustache") {
    return mustacheNovemberImages;
  } else if (choose_your_holiday === "webkom"){
    return webkomSymbols;
  } else if (choose_your_holiday === "valentines") {
    return valentinesSymbols;
  }
  return [ ]; // Return an empty array if the holiday is not recognized
}

const chosenHoliday = "webkom"; // Change this to select the holiday you want
const selectedSymbols = selectSymbols(chosenHoliday);

const maxElements = 100; // Maximum number of elements

// Image width and hight
const imageWidth = 20 //rem
const imageHeight = 15 //rem

const headerHeight = document.getElementsByTagName("header")[0].offsetHeight;
const mainHeight = document.getElementsByTagName("main")[0].offsetHeight;
const footerHeight = document.getElementsByTagName("footer")[0].offsetHeight;
const totalHeight = headerHeight + mainHeight + footerHeight - convertRemToPixels(imageHeight);

// Container containing the rain
const rainContainer = document.getElementById("makeItRain");

// Swing distance defined in the CSS keyframe
const swingDistance = parseInt(getComputedStyle(rainContainer).getPropertyValue('--swing-distance'));

// Create and animate the initial set of elements
createAndAnimateElements(maxElements);

//Convert rem to px
function convertRemToPixels(rem) {
    return rem * parseFloat(getComputedStyle(document.documentElement).fontSize);
}

function handleResize() {
  const windowHeight = window.innerHeight;
  const content = document.getElementsByTagName("body")[0];
  const pageHeight = Math.max(content.offsetHeight, windowHeight);
  return pageHeight;
}

function calculateSpawnInterval() {
  // const pageHeight = handleResize();
  
  // Gjennomsnittlig tid et element bruker fra topp til bunn i sekunder
  // (Siden koden din bruker: rainSpeed + Math.random() * 5)
  const averageFallTimeSeconds = rainSpeed + 2.5; 
  
  // Konverterer den totale levetiden til millisekunder
  const totalLifeTimeMs = averageFallTimeSeconds * 1000;
  
  // For å ha nøyaktig maxElements på skjermen samtidig,
  // må intervallet være den totale levetiden delt på maks antall elementer
  const optimalInterval = totalLifeTimeMs / maxElements;
  
  // Sikrer at vi ikke crasher nettleseren med et intervall på 0
  return Math.max(10, optimalInterval); 
}

function createAndAnimateElements(maxElements) {
  // Lytt på resize én gang, ikke inne i intervallet
  window.addEventListener('resize', () => {
    height = handleResize();
  });

  // Start en kontinuerlig strøm med en gang
  const rainInterval = setInterval(() => {
    createAndAnimateElement();
    
    // Remove the oldest element when exceeding the maximum
    const elements = document.getElementsByClassName('rainElement');
    if (elements.length >= maxElements) {
      rainContainer.removeChild(elements[0]);
    }
  }, calculateSpawnInterval()); // 40 millisekunder gir rundt 25 nye elementer i sekundet. Juster denne for tetthet!
}


function createAndAnimateElement() {
  // Random width & height between 0 and viewport
  //Image height and swing width have to be subtracted from the width to avoid overflow.
  const randomWidth = Math.floor(Math.random() * (Math.max(document.documentElement.clientWidth, window.innerWidth || 0)-convertRemToPixels(imageWidth)-swingDistance));

  // Calculate the animation duration based on the rain speed
  const animationDuration = rainSpeed + Math.random() * 5; // Lavere tall = raskere fall 

  // Random animation-delay
  //const randomAnimationDelay = Math.random() * 2; // adjust the number to make it longer before the rain starts

  // Create element
  const randomSymbol = selectedSymbols[Math.floor(Math.random() * selectedSymbols.length)];
  if (randomSymbol.includes(".png")) { // Create image element
    var element = document.createElement('img');
    element.src = randomSymbol;
  } else { // Create text element if emojis
    var element = document.createElement('div');
    element.innerHTML = randomSymbol;
  }
  element.style.setProperty("--margin-end", totalHeight + 'px');
  element.className = 'rainElement rainSize';
  element.style.left = randomWidth + 'px';
  element.style.animation = `fall ${animationDuration}s infinite, swing ${Math.random() * 4 + 2}s alternate infinite`;
  //element.style.animationDelay = randomAnimationDelay + 's';
  element.style.animationDelay = '0s';
  element.style.color = 'hsl('+(Math.random()*360|0)+',80%,50%)';
  element.style.fontWeight = "bold";
  element.style.width = "auto";
  element.style.textShadow="-1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;";
  rainContainer.appendChild(element);

}