const holidaySymbols = ["❄️", "❄️", "❄️", "🎄", "🎁", "🎅"];

for(i=0; i<300; i++) {
  // Random rotation
  var randomRotation = Math.floor(Math.random() * 360);
  // Random width & height between 0 and viewport
  var randomWidth = Math.floor(Math.random() * Math.max(document.documentElement.clientWidth, window.innerWidth || 0));
  var randomHeight =  Math.floor(Math.random() * Math.max(document.documentElement.clientHeight, window.innerHeight || 0));

  // Random animation-delay
  var randomAnimationDelay = Math.floor(Math.random() * 150);
  console.log(randomAnimationDelay);

  // Random colors
  var colors = ['#0CD977', '#FF1C1C', '#FF93DE', '#5767ED', '#FFC61C', '#8497B0'];
  var randomColor = colors[Math.floor(Math.random() * colors.length)];

  //edit end point confetti rain
  const content =  document.getElementsByTagName("body")[0];
  const windowHeight = window.innerHeight;
  const pageHeight = Math.max(content.offsetHeight, windowHeight);
  const height = pageHeight + 1000;


  // Create confetti piece
  var rain = document.createElement('div');
  rain.style.setProperty('--margin-end', `${height}px`);
  rain.className = 'rain';
  rain.style.top=randomHeight + 'px';
  rain.style.left=randomWidth + 'px';
  rain.style.backgroundColor=randomColor;
  rain.style.transform='skew(15deg) rotate(' + randomRotation + 'deg)';
  rain.style.animation = `confettiRain ${height/50}s infinite`;
  rain.style.animationDelay=randomAnimationDelay + 's';
  //document.getElementById("makeItRain").appendChild(rain);


   // Create snowflake piece
  var snowflakeSymbol = "❄️"; // Snowflake symbol
  var snowflake = document.createElement('div');
  snowflake.style.setProperty('--margin-end', `${height}px`);
  snowflake.className = 'snowflake';
  snowflake.style.top = randomHeight + 'px';
  snowflake.style.left = randomWidth + 'px';
  snowflake.innerHTML = snowflakeSymbol;
  snowflake.style.animation = `snowFall ${height / 10}s infinite, snowSwing ${Math.random() * 4 + 2}s alternate infinite`;
  snowflake.style.animationDelay = randomAnimationDelay + 's';
  //document.getElementById("makeItRain").appendChild(snowflake);

    // Create holiday-themed piece
  var randomSymbol = holidaySymbols[Math.floor(Math.random() * holidaySymbols.length)];
  var holidayElement = document.createElement('div');
  holidayElement.style.setProperty('--margin-end', `${height}px`);
  holidayElement.className = 'holidayElement';
  holidayElement.style.top = randomHeight + 'px';
  holidayElement.style.left = randomWidth + 'px';
  holidayElement.innerHTML = randomSymbol;
  holidayElement.style.animation = `christmasFall ${height / 20}s infinite, christmasSwing ${Math.random() * 4 + 2}s alternate infinite`;
  holidayElement.style.animationDelay = randomAnimationDelay + 's';
  holidayElement.style.fontSize = '2rem';
  document.getElementById("makeItRain").appendChild(holidayElement);
}