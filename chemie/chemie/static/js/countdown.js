dayjs.extend(dayjs_plugin_duration);

function dayCountdown(element,targetString,eventString){
    const targetDate = dayjs(targetString);

    setInterval(()=>{
        const now = dayjs();
        const duration = dayjs.duration(targetDate.diff(now));

        if (duration.asMilliseconds() <= 0) {
            element.querySelector(".until__text").textContent = ` ${eventString}!!`
            return
        };

        if (duration.asDays()>=1){
            element.querySelector(".days__until").textContent = duration.asDays().toFixed(0).toString().padStart(2,"0")
            element.querySelector(".until__text").textContent = `Dager igjen til ${eventString}`
        };
        if (duration.asDays()<1){
            element.querySelector(".days__until").textContent = duration.asHours().toFixed(0).toString().padStart(2,"0")
            element.querySelector(".until__text").textContent = `Timer igjen til ${eventString}`
        };
        if (duration.asHours()<1){
            element.querySelector(".days__until").textContent = duration.asMinutes().toFixed(0).toString().padStart(2,"0")
            element.querySelector(".until__text").textContent = `Minutter igjen til ${eventString} `
        };

    },50)



}

dayCountdown(document.getElementById("Countdown"),"2023-03-04 12:00","vinterblotet")