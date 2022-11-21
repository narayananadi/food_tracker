var field_count = 0
console.log("js activated")

function depression() {
    var w = document.getElementById("weight").innerHTML
    var h = document.getElementById("height").innerHTML
    var res = w/(h*h)
    document.getElementById("res").innerHTML="&emsp; &emsp; &emsp; &emsp; &emsp; &nbsp; BMI- "+res.toFixed(2)+" kg/m<sup>2</sup>"
}

function add_it(id){
    var increase = document.querySelector('input[name='+id+']')
    var value = parseInt(increase.value) 
    if (value < 10){
        increase.value = value + 1
    }   
}

function sub_it(id){
    var increase = document.querySelector('input[name='+id+']')
    var value = parseInt(increase.value) 
    if (value > 0){
        increase.value = value - 1
    }  
}

function del_it(id){
    var increase = document.querySelector('input[name='+id+']')
    var value = parseInt(increase.value) 
    if (value > 0){
        increase.value = value - 1
    }  
}
function add_field(val){
    var id = val.value.split("_")[0]
    var name = val.value.split("_")[1]
    var to_insert = document.getElementById("insert_fields")
    to_insert.innerHTML = to_insert.innerHTML + "<input name='input_field_"+field_count+"' value='"+id+"' type='hidden'></input>"
    to_insert.innerHTML = to_insert.innerHTML + "<label>"+name+"</label>"
    to_insert.innerHTML = to_insert.innerHTML + "<input type='number' name='count_field_"+field_count+"' value=1></input>"
    to_insert.innerHTML = to_insert.innerHTML + " <button type='button' onclick=\"add_it('count_field_"+field_count+"')\">add</button>"
    to_insert.innerHTML = to_insert.innerHTML + " <button type='button' onclick=\"sub_it('count_field_"+field_count+"')\">sub</button>"
    to_insert.innerHTML = to_insert.innerHTML + " <button type='button' onclick=\"del_it('count_field_"+field_count+"')\">sub</button>"
    to_insert.innerHTML = to_insert.innerHTML + "<br>"

    field_count +=1
}