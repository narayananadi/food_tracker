function depression() {
    var w = document.getElementById("weight").innerHTML
    var h = document.getElementById("height").innerHTML
    var res = w/(h*h)
    document.getElementById("res").innerHTML=res.toFixed(2)+" kg/m<sup>2</sup>"
}