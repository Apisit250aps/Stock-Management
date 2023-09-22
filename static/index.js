function timeFormat(datetime) {
    const time = new Date(datetime).toLocaleTimeString("en-US", { hour12: false });
    const date = new Date(datetime).toLocaleDateString("en-GB");
    return `${date} - ${time}`;
}


let x = document.querySelectorAll("td.num");
for (let i = 0, len = x.length; i < len; i++) {
    let num = new Number(x[i].innerHTML)
        .toLocaleString('en-US');
    x[i].innerHTML = num;
    x[i].classList.add("currSign");
}

let time = document.querySelectorAll("time");
for (let i = 0, len = time.length; i < len; i++) {
    let date = timeFormat(time[i].innerHTML)
    time[i].innerHTML = date;
    console.log(date)
}


// JsBarcode(".barcode", {
//     width: 1
//   });
// let barcode = document.querySelectorAll("#barcode")
// for (let i = 0; len = barcode.length; i++)
// {
//     let code = JsBarcode("#barcode", barcode[1].innerHTML);
// }

