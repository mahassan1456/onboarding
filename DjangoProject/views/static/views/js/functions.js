

function getPhysicians(event) {
    var csrf_token = document.querySelector("input[name=csrfmiddlewaretoken]").value;
    var hospital_id = event.target.value;
    var physicians_main_list = document.getElementById('physician_main_list');
    var json_obj = {}
    json_obj['hospital_id'] = hospital_id;
    var callbackURL = '/views/filter/physician/listview/'
        $.ajax({
            type: 'POST',
            headers: { "X-CSRFToken": csrf_token },
            dataType: "json",
            data: json_obj,
            url: callbackURL,
            // Receiving JSON Response Back from DB
            success: function(response) {
                console.log(response)
                console.log('wtf')
                if (response.dataset) {
                    physicians_main_list.innerHTML = ""
                    var dataset = response.dataset
                    console.log(response.dataset)
                    for (let physician of dataset) { 
                        var HTML = `
                        <tr>
                            <td><img src="${physician[1]}" class="physician_sm_pic"></td>
                            <td>${physician[3]}</td>
                            <td>${physician[0]['name']}</td>
                            <td>Not Provided</td>
                            <td>${physician[2]}</td>
                            <td class="text-center"><a href="#">View All</a></td>
                            <td class="text-center"><a href="#" class=" "><i class="fa-solid fa-pen-to-square"></i></a></td>
                            <td class="text-center"><a href="#" class=" "><i class="fa-solid fa-trash-can"></i></a></td>
                        </tr>`

                        physicians_main_list.insertAdjacentHTML('beforeend',HTML)
                
                        }
                    return;
                }
                // Write Javascript function here
            },
            error: function() {
            console.log('error')
            }
        })
        return
}