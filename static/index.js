
let x = document.querySelectorAll("td.num");



for (let i = 0, len = x.length; i < len; i++) {
    let num = new Number(x[i].innerHTML)
        .toLocaleString('en-US');
    x[i].innerHTML = num;
    x[i].classList.add("currSign");
}

let time = document.querySelectorAll("td.time");
for (let i = 0, len = time.length; i < len; i++) {
    let date = new Date(time[i].innerHTML).toLocaleDateString('en-GB')
    time[i].innerHTML = date;
    
}


// JsBarcode(".barcode", {
//     width: 1
//   });
// let barcode = document.querySelectorAll("#barcode")
// for (let i = 0; len = barcode.length; i++)
// {
//     let code = JsBarcode("#barcode", barcode[1].innerHTML);
// }

