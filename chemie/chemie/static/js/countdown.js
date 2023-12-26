dayjs.extend(dayjs_plugin_duration);

function dayCountdown(element,targetString){
    const targetDate = dayjs(targetString);

    setInterval(()=>{
        const now = dayjs();
        const duration = dayjs.duration(targetDate.diff(now));

        if (duration.asMillisecond <= 0) return;
        element.querySelector(".days__until").textContent = duration.asDays().toFixed(0).toString().padStart(2,"0")

    },50)



}

dayCountdown(document.getElementById("Countdown"),"2024-03-04")