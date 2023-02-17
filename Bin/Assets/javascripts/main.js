const clearoutput = () =>{
    document.getElementById("output").innerHTML = ""
}

const createOutput = (text) =>{
    let output = document.createElement('small');
    output.className = "d-block";
    output.textContent = text;
    return(output);
}

const StartChart = () => {
    let accessionnum = document.getElementById("accessionnum").value
    let organismname = document.getElementById("organismname").value
    let locustags = document.getElementById("locustags").value

    const ws = new WebSocket("ws://localhost:3000/ws");
    let output = document.getElementById("output");

    
    ws.onopen = (event) => {
        document.getElementById("run").disabled = true
        document.getElementById("clear").disabled = true
        document.getElementById("output").nextElementSibling.firstElementChild.disabled = true 
        ws.send(JSON.stringify({
            accessionnum : accessionnum,
            organismname : organismname,
            locustags : locustags
        }))
    }

    ws.onmessage = (event) => {
        var responce = JSON.parse(event.data);
        if (responce.includes("\n")){
            console.log(responce);
            output.appendChild(createOutput(` >${responce}`));
            output.appendChild(createOutput(``));
        }
        else
            output.lastElementChild.innerHTML = `>${responce}`
    };
    ws.onerror = (event) => {
        output.appendChild(createOutput(` >> face some error to download the sequence of ${accessionnum}`));
        output.lastElementChild.classList.add("text-danger")
    }
    ws.onclose = (event) => {

        output.appendChild(createOutput(` >> hit the download link to download ${accessionnum} sequence`));
        output.lastElementChild.classList.add("text-primary")
        document.getElementById("download").className = "btn btn-outline-primary";
        document.getElementById("download").setAttribute("href", `/download/${accessionnum}`)
        document.getElementById("run").disabled = false
        document.getElementById("clear").disabled = false
        document.getElementById("download").disable = false
        document.getElementById("output").nextElementSibling.firstElementChild.disabled = false 
    }
}

const viewData = () => {
    let accessionnum = document.getElementById("accessionnum").value
    let organismname = document.getElementById("organismname").value
    let locustags = document.getElementById("locustags").value

    console.log(accessionnum, organismname, locustags);
    clearoutput()
    let output = document.getElementById("output");
    output.appendChild(createOutput(` >> Accession ID : ${accessionnum}`));
    output.appendChild(createOutput(` >> Strain name : ${organismname}`));
    output.appendChild(createOutput(` >> E-path locus tags : [${locustags.split(",")[ 0 ]}, ${locustags.split(",")[ 1 ]}...${locustags.split(",")[ locustags.split(",").length -1 ]}]`));
    output.appendChild(createOutput(``));

    document.getElementById("accessionnum").readOnly = true;
    document.getElementById("organismname").readOnly = true;
    document.getElementById("locustags").readOnly = true;

    document.getElementById("submit").className = "d-none";
    document.getElementById("clear").className = "btn btn-outline-danger";
    document.getElementById("run").className = "btn btn-outline-success";
}

const clearData = ()=>{
    document.getElementById("accessionnum").value = ""
    document.getElementById("organismname").value = ""
    document.getElementById("locustags").value = ""

    document.getElementById("accessionnum").readOnly = false;
    document.getElementById("organismname").readOnly = false;
    document.getElementById("locustags").readOnly = false;

    document.getElementById("submit").className = "btn btn-outline-secondary";
    document.getElementById("clear").className = "d-none";
    document.getElementById("run").className = "d-none";
    document.getElementById("download").setAttribute("href", `/download`)
    document.getElementById("download").className = "d-none";
}