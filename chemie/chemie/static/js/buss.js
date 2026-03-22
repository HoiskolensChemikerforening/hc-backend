
async function loadBoard(div_ID, Busstop_ID){
    const res = await fetch("https://api.entur.io/journey-planner/v3/graphql",{
        method:"POST",
        headers:{
        "Content-Type":"application/json",
        "ET-Client-Name":"my-atb-board"
        },
        body: JSON.stringify({
            query: `
            {
                quay(id: "${Busstop_ID}") {
                    estimatedCalls(numberOfDepartures: 8) {
                        expectedDepartureTime
                        destinationDisplay { frontText }
                        serviceJourney {
                            line { publicCode }
                        }
                    }
                }
            }
            `
        })
        })

    const json = await res.json()

    const board = document.getElementById(div_ID)
    board.innerHTML=""

    const departures = json.data.quay.estimatedCalls

    departures.forEach(bus=>{

        const departure = new Date(bus.expectedDepartureTime)
        const now = new Date()

        const minutes = Math.round((departure-now)/60000)

        const arrivalTime = departure.toLocaleTimeString("no-NO", {
            hour: "2-digit",
            minute: "2-digit"
        })

        const row = document.createElement("div")
        row.className="row"

        row.innerHTML = `
        <div class="card medium">
            <div class="card-image">
                <h4 class="card title"> Mot Sentrum </h4>
                <div class="line">${bus.serviceJourney.line.publicCode}</div>
                <div class="dest">${bus.destinationDisplay.frontText}</div>
                <div class="time">${minutes <= 0 ? "NÅ" : minutes+" min"}</div>
                <div class="arrival">${arrivalTime}</div>
            </div>
        </div>
        `

        board.appendChild(row)
    })

}

setInterval(() => {
    loadBoard("HH_MS", HESTEHAGEN_MS)
    loadBoard("HH_FS", HESTEHAGEN_FS)
    loadBoard("GLOS_FS", GLOSHAUGEN_FS)
    loadBoard("GLOS_MS", GLOSHAUGEN_MS)
    loadBoard("HSR_FS", HOISKOLERINGEN_FS)
    loadBoard("HSR_MS", HOISKOLERINGEN_MS)
}, 30000)

