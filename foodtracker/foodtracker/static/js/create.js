var field_count = 0
console.log("js activated")
var checklist = []
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
        if (checklist.includes(val.value) == false){
            checklist.push(val.value)
            var to_insert = document.getElementById("insert_fields")
            to_insert.innerHTML = to_insert.innerHTML + "<input name='input_field_"+field_count+"' value='"+id+"' type='hidden'></input>"
            to_insert.innerHTML = to_insert.innerHTML + "<label>"+name+"</label>"
            to_insert.innerHTML = to_insert.innerHTML + "<input type='number' name='count_field_"+field_count+"' value=1></input>"
            to_insert.innerHTML = to_insert.innerHTML + " <button type='button' style='background-color: forestgreen; color: white' onclick=\"add_it('count_field_"+field_count+"')\">+</button>"
            to_insert.innerHTML = to_insert.innerHTML + " <button type='button' style='background-color: orange; color: white' onclick=\"sub_it('count_field_"+field_count+"')\">-</button>"
            to_insert.innerHTML = to_insert.innerHTML + " <button type='button' style='background-color: crimson; color: white' onclick=\"del_it('count_field_"+field_count+"')\">Delete</button>"
            to_insert.innerHTML = to_insert.innerHTML + "<br>"
            field_count +=1
        }else{
            var warn = document.getElementById("warning")
            warn.innerHTML = "*"+name+" Already Added in checkout list!"
            console.log("bhag chutiye")
        }
}