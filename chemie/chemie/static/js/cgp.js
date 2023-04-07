
console.log("start")
for(i=0; i<300; i++) {
  // Random rotation
  var randomRotation = Math.floor(Math.random() * 360);
  // Random width & height between 0 and viewport
  var randomWidth = Math.floor(Math.random() * Math.max(document.documentElement.clientWidth, window.innerWidth || 0));
  var randomHeight =  Math.floor(Math.random() * Math.max(document.documentElement.clientHeight, window.innerHeight || 0));

  // Random animation-delay
  var randomAnimationDelay = Math.floor(Math.random() * 50);
  console.log(randomAnimationDelay)

  // Random colors
  var colors = ['#0CD977', '#FF1C1C', '#FF93DE', '#5767ED', '#FFC61C', '#8497B0']
  var randomColor = colors[Math.floor(Math.random() * colors.length)];

  //edit end point confetti rain
  const content =  document.getElementById("contentbox")
  const height = Math.max(content.offsetHeight, window.innerHeight) +50


  // Create confetti piece
  var confetti = document.createElement('div');
  confetti.style.setProperty('--margin-end', `${height}px`);
  confetti.className = 'confetti';
  confetti.style.top=randomHeight + 'px';
  confetti.style.left=randomWidth + 'px';
  confetti.style.backgroundColor=randomColor;
  confetti.style.transform='skew(15deg) rotate(' + randomRotation + 'deg)';
  confetti.style.animation = `confettiRain ${height/75}s infinite`;
  confetti.style.animationDelay=randomAnimationDelay + 's';
  document.getElementById("confetti-wrapper").appendChild(confetti);
}
