const christmasSymbols = ["❄️", "❄️", "❄️", "🎄", "🎁", "🎅"]; // add in emojies after every Advent
const easterSymbols = ["🐰", "🗿", "🐥", "🐣"];
const breastCancerSymbols = ["🎀", "🌸", "💗"];
const halloweenSymbols = ["🎃", "🎃", "🎃", "🕷️", "👻", "🪦", "⚰️", "🕸️", "🦇"];
const paulImages = ["../../static/images/holiday_images/paul.png", "../../static/images/holiday_images/paul_tullebilde.png"];
const mustacheNovemberImages = ["../../static/images/holiday_images/bart1.png",
  "../../static/images/holiday_images/bart2.png", "../../static/images/holiday_images/bart3.png",
  "../../static/images/holiday_images/bart4.png", "../../static/images/holiday_images/bart5.png",
  "../../static/images/holiday_images/bart6.png"];

function selectSymbols(choose_your_holiday) {
  if (choose_your_holiday === "christmas") {
    return christmasSymbols;
  } else if (choose_your_holiday === "easter") {
    return easterSymbols;
  } else if (choose_your_holiday === "breast cancer") {
    return breastCancerSymbols
  } else if (choose_your_holiday === "halloween") {
    return halloweenSymbols
  } else if (choose_your_holiday === "pauloween") {
    return paulImages
  } else if (choose_your_holiday === "mustache") {
    return mustacheNovemberImages
  }
  return []; // Return an empty array if the holiday is not recognized
}

const chosenHoliday = "mustache"; // Change this to select the holiday you want
const selectedSymbols = selectSymbols(chosenHoliday);

for(i=0; i<300; i++) {
  // Random width & height between 0 and viewport
  var randomWidth = Math.floor(Math.random() * Math.max(document.documentElement.clientWidth, window.innerWidth || 0));
  var randomHeight =  Math.floor(Math.random() * Math.max(document.documentElement.clientHeight, window.innerHeight || 0));

  // Random animation-delay
  var randomAnimationDelay = Math.floor(Math.random() * 150);
  console.log(randomAnimationDelay);

  //edit end point rain
  const content =  document.getElementsByTagName("body")[0];
  const windowHeight = window.innerHeight;
  const pageHeight = Math.max(content.offsetHeight, windowHeight);
  const height = pageHeight + 1000;

    // Create general rain piece
  var randomSymbol = selectedSymbols[Math.floor(Math.random() * selectedSymbols.length)];
  if (randomSymbol.includes(".png")) { // Check if the symbol is an image URL
    var imageElement = document.createElement('img');
    imageElement.src = randomSymbol;
    imageElement.style.setProperty('--margin-end', `${height}px`);
    imageElement.className = 'element';
    imageElement.style.top = randomHeight + 'px';
    imageElement.style.left = randomWidth + 'px';
    imageElement.style.animation = `fall ${height / 20}s infinite, swing ${Math.random() * 4 + 2}s alternate infinite`;
    imageElement.style.animationDelay = randomAnimationDelay + 's';
    // Adjust the image size as needed
    imageElement.style.width = '4rem';
    imageElement.style.height = '3rem';
    document.getElementById("makeItRain").appendChild(imageElement);
  } else {
    var element = document.createElement('div');
    element.style.setProperty('--margin-end', `${height}px`);
    element.className = 'element';
    element.style.top = randomHeight + 'px';
    element.style.left = randomWidth + 'px';
    element.innerHTML = randomSymbol;
    element.style.animation = `fall ${height / 20}s infinite, swing ${Math.random() * 4 + 2}s alternate infinite`;
    element.style.animationDelay = randomAnimationDelay + 's';
    element.style.fontSize = '2rem';
    document.getElementById("makeItRain").appendChild(element);
  }
}