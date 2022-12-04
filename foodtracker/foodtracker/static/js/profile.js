function depression() {
    var w = document.getElementById("weight").innerHTML
    var h = document.getElementById("height").innerHTML.toString()
    if (!h.includes(".")) {
        var h1=Number.parseInt(h)
        var v=h1/100
    }
    console.log(v);
    var res = w/(v*v)
    // console.log(res);
    document.getElementById("res").innerHTML=res.toFixed(2)+" kg/m<sup>2</sup>"
}

function bmicheck() {
    var w = Number.parseFloat(document.getElementById("weight").value)
    var h = Number.parseFloat(document.getElementById("height").value)
    var res = w/(h*h)
    document.getElementById("res").innerHTML=res.toFixed(2)+" kg/m<sup>2</sup>"
}