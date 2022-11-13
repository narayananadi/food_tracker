function depression() {
    var w = document.getElementById("weight").value
    var h = document.getElementById("height").value
    var res = w/(h*h)
    document.getElementById("res").innerHTML="&emsp; &emsp; &emsp; &emsp; &emsp; &nbsp; BMI- "+res.toFixed(2)+" kg/m<sup>2</sup>"
}