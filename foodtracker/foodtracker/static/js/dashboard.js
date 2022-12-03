var  counter = 0

function add_counter(){
    if (counter+1 > (chart_data["carbs"]["date"].length/slice_count*(-1))){
        console.log("limit reached")
        return
    }
    counter+=1
    if (counter == 0){
        carbs_chart.data.labels = chart_data["carbs"]["date"].slice(slice_count,)
        carbs_chart.data.datasets[0].data = chart_data["carbs"]["value"].slice(slice_count,)

        proteins_chart.data.labels = chart_data["proteins"]["date"].slice(slice_count,)
        proteins_chart.data.datasets[0].data = chart_data["proteins"]["value"].slice(slice_count,)
        
        cal_chart.data.labels = chart_data["calories"]["date"].slice(slice_count,)
        cal_chart.data.datasets[0].data = chart_data["carbs"]["value"].slice(slice_count,)
        
        fats_chart.data.labels = chart_data["fats"]["date"].slice(slice_count,)
        fats_chart.data.datasets[0].data = chart_data["fats"]["value"].slice(slice_count,)
    }
    else{
        start = slice_count*(counter+1)
        if (start <= (chart_data["carbs"]["date"].length)*(-1)){
            start = 0
        }
        carbs_chart.data.labels = chart_data["carbs"]["date"].slice(start, slice_count*counter)
        carbs_chart.data.datasets[0].data = chart_data["carbs"]["value"].slice(start, slice_count*counter)

        proteins_chart.data.labels = chart_data["proteins"]["date"].slice(start, slice_count*counter)
        proteins_chart.data.datasets[0].data = chart_data["proteins"]["value"].slice(start, slice_count*counter)

        fats_chart.data.labels = chart_data["fats"]["date"].slice(start, slice_count*counter)
        fats_chart.data.datasets[0].data = chart_data["fats"]["value"].slice(start, slice_count*counter)

        cal_chart.data.labels = chart_data["calories"]["date"].slice(start, slice_count*counter)
        cal_chart.data.datasets[0].data = chart_data["calories"]["value"].slice(start, slice_count*counter)
    }
    console.log(counter)
    carbs_chart.update()
    cal_chart.update()
    fats_chart.update()
    proteins_chart.update()

}

function sub_counter(){
    counter-=1
    if (counter < 0){
        counter = 0
    }
    if (counter == 0){
        carbs_chart.data.labels = chart_data["carbs"]["date"].slice(slice_count,)
        carbs_chart.data.datasets[0].data = chart_data["carbs"]["value"].slice(slice_count,)

        proteins_chart.data.labels = chart_data["proteins"]["date"].slice(slice_count,)
        proteins_chart.data.datasets[0].data = chart_data["proteins"]["value"].slice(slice_count,)

        fats_chart.data.labels = chart_data["fats"]["date"].slice(slice_count,)
        fats_chart.data.datasets[0].data = chart_data["fats"]["value"].slice(slice_count,)

        cal_chart.data.labels = chart_data["calories"]["date"].slice(slice_count,)
        cal_chart.data.datasets[0].data = chart_data["calories"]["value"].slice(slice_count,)
    }
    else{
        start = slice_count*(counter+1)
        if (start <= (chart_data["carbs"]["date"].length)*(-1)){
            start = 0
        }
        carbs_chart.data.labels = chart_data["carbs"]["date"].slice(start, slice_count*counter)
        carbs_chart.data.datasets[0].data = chart_data["carbs"]["value"].slice(start, slice_count*counter)

        proteins_chart.data.labels = chart_data["proteins"]["date"].slice(start, slice_count*counter)
        proteins_chart.data.datasets[0].data = chart_data["proteins"]["value"].slice(start, slice_count*counter)

        fats_chart.data.labels = chart_data["fats"]["date"].slice(start, slice_count*counter)
        fats_chart.data.datasets[0].data = chart_data["fats"]["value"].slice(start, slice_count*counter)

        cal_chart.data.labels = chart_data["calories"]["date"].slice(start, slice_count*counter)
        cal_chart.data.datasets[0].data = chart_data["calories"]["value"].slice(start, slice_count*counter)
    }
    console.log(counter)
    
    carbs_chart.update()
    cal_chart.update()
    fats_chart.update()
    proteins_chart.update()

}