const christmasSymbols = ["❄️", "❄️", "❄️"]; // , "🎄", "🎁", "🎅" add in emojis after every Advent
const easterSymbols = ["🐰", "🗿", "🐥", "🐣"];
const breastCancerSymbols = ["🎀", "🌸", "💗"];
const halloweenSymbols = ["🎃", "🎃", "🎃", "🕷️", "👻", "🪦", "⚰️", "🕸️", "🦇"];
const paulImages = ["../../static/images/holiday_images/paul.png", "../../static/images/holiday_images/paul_tullebilde.png"];
const mustacheNovemberImages = [
  "../../static/images/holiday_images/bart1.png",
  "../../static/images/holiday_images/bart2.png",
  "../../static/images/holiday_images/bart3.png",
  "../../static/images/holiday_images/bart4.png",
  "../../static/images/holiday_images/bart5.png",
  "../../static/images/holiday_images/bart6.png"
];

const rainSpeed = 100; // Adjust this value to set the rain speed

function selectSymbols(choose_your_holiday) {
  if (choose_your_holiday === "christmas") {
    return christmasSymbols;
  } else if (choose_your_holiday === "easter") {
    return easterSymbols;
  } else if (choose_your_holiday === "breast cancer") {
    return breastCancerSymbols;
  } else if (choose_your_holiday === "halloween") {
    return halloweenSymbols;
  } else if (choose_your_holiday === "pauloween") {
    return paulImages;
  } else if (choose_your_holiday === "mustache") {
    return mustacheNovemberImages;
  }
  return [ ]; // Return an empty array if the holiday is not recognized
}

const chosenHoliday = "christmas"; // Change this to select the holiday you want
const selectedSymbols = selectSymbols(chosenHoliday);

const maxElements = 150; // Maximum number of elements

const headerHeight = document.getElementsByTagName("header")[0].offsetHeight;
const mainHeight = document.getElementsByTagName("main")[0].offsetHeight;
const totalHeight = headerHeight +mainHeight;

// Image width and hight
const imageWidth = 4 //rem
const imageHeight = 3 //rem

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

function createAndAnimateElements(maxElements) {
  for (let i = 0; i < maxElements; i++) {
    createAndAnimateElement();
  }

  // Continuously create and animate new elements at a set interval
  setInterval(() => {
    // Check for height change on window resize
    window.addEventListener('resize', () => {
      height = handleResize();
    });

    createAndAnimateElement();
  }, 1000); // Adjust the interval as needed
}

function createAndAnimateElement() {
  // Random width & height between 0 and viewport
  //Image height and swing width have to be subtracted from the width to avoid overflow.
  var randomWidth = Math.floor(Math.random() * (Math.max(document.documentElement.clientWidth, window.innerWidth || 0)-convertRemToPixels(imageWidth)-swingDistance));

  // Calculate the animation duration based on the rain speed
  const animationDuration = rainSpeed + Math.random() * 5;

  // Random animation-delay
  var randomAnimationDelay = Math.floor(Math.random() * 40); // adjust the number to make it longer before the rain starts

  // Create element
  var randomSymbol = selectedSymbols[Math.floor(Math.random() * selectedSymbols.length)];
  if (randomSymbol.includes(".png")) { // Create image element
    var imageElement = document.createElement('img');
    imageElement.src = randomSymbol;
    imageElement.style.setProperty("--margin-end", totalHeight + 'px');
    imageElement.className = 'element';
    imageElement.style.left = randomWidth + 'px';
    imageElement.style.animation = `fall ${animationDuration}s infinite, swing ${Math.random() * 4 + 2}s alternate infinite`;
    imageElement.style.animationDelay = randomAnimationDelay + 's';

    // Adjust the image size as needed
    imageElement.style.width = imageWidth+'rem';
    imageElement.style.height = imageHeight+'rem';
    rainContainer.appendChild(imageElement);

  } else { // Create text element if emojis
    var element = document.createElement('div');
    element.style.setProperty("--margin-end", totalHeight + 'px');
    element.className = 'element';
    element.style.left = randomWidth + 'px';
    element.innerHTML = randomSymbol;
    element.style.animation = `fall ${animationDuration}s infinite, swing ${Math.random() * 4 + 2}s alternate infinite`;
    element.style.animationDelay = randomAnimationDelay + 's';
    element.style.fontSize = '2rem';
    rainContainer.appendChild(element);
  }

  // Remove the oldest element when exceeding the maximum
  const elements = document.getElementsByClassName('element');
  if (elements.length > maxElements) {
    rainContainer.removeChild(elements[0]);
  }
}