function placeitem(event) {
    var box = document.getElementById("id_select_box8");
    var p = document.createElement("p");
    p.textContent = "what the fuck";
    box.appendChild(p);
    console.log(box)
  }
  
  function collapseexpand() {
    window.addEventListener('DOMContentLoaded', (event) => {
   
    var lis = document.querySelectorAll(".expandbox");
    var bl = document.querySelectorAll(".tt12 > .xp24");
      
      for (let i = 0; i < lis.length; i++) {
        lis[i].addEventListener('click', (event) => {
            
          if (bl[i].style.display === 'none') {
            bl[i].style.display = 'block';
            lis[i].firstElementChild.nextElementSibling.textContent = "-";
          } else {
            bl[i].style.display = 'none';
            lis[i].firstElementChild.nextElementSibling.textContent = "+";
          }
        });
      }
  });
  }
  
  function choose_search(event) {
  
    var specialty = document.getElementById("specialty_select")
    var tags = document.getElementById("tags_select")
   
    specialty.style.display = 'none';
    tags.style.display = 'block';
  }
  
  function addon(event) {
  
  var search_type = document.getElementById("search_type").value;
  
  if (search_type == 'specialty') {
  
      var select = document.getElementById("id_select_box1");
      select.parentNode.lastChild
      var result = [...select.options].filter( (opt) => opt.selected).map(opt => opt.value);
      var box2 = document.getElementById("id_select_box7");
  
  if (document.querySelectorAll("#id_select_box7 > option").length > 0) {
    var orig_result = document.querySelectorAll("#id_select_box7 > option");
    var new_result = [...orig_result].map( opt => opt.value);
  
  
  for (let i = 0; i < result.length; i++) {
      
      if (new_result && !new_result.includes(result[i])) {
        var opt = document.createElement("p");
        opt.textContent = result[i];
        box2.appendChild(opt);
      }
    }
  } else {
  
        for (let i = 0; i < result.length; i++) {
  
          var opt = document.createElement("option");
          opt.textContent = result[i];
          box2.appendChild(opt);
        }
    }
  } else if (search_type == 'tags') {
  
      var select = document.getElementById("id_select_box2");
      var result = [...select.options].filter( (opt) => opt.selected).map(opt => opt.value);
      var box2 = document.getElementById("id_select_box8");
  
      if (document.querySelectorAll("#id_select_box8 > option").length > 0) {
        var orig_result = document.querySelectorAll("#id_select_box8 > option");
        var new_result = [...orig_result].map( opt => opt.value);
  
      for (let i = 0; i < result.length; i++) {
          
          if (new_result && !new_result.includes(result[i])) {
            var opt = document.createElement("option");
            opt.textContent = result[i];
            box2.appendChild(opt);
          }
    }
  
    } else {
  
          for (let i = 0; i < result.length; i++) {
  
            var opt = document.createElement("option");
            opt.textContent = result[i];
            box2.appendChild(opt);
  
         }
      }
  }
  }
    function remove(event) {
      
      var select = document.getElementById("id_select_box1");
      var result = [...select.options].filter( (opt) => opt.selected);
      result.forEach( element => element.remove());
        
    }
  
    function pleasework() {
    var lis = document.querySelectorAll(".expandbox");
    var bl = document.querySelectorAll(".tt12 > .xp24");
      
      for (let i = 0; i < lis.length; i++) {
        lis[i].addEventListener('click', (event) => {
            
  
          if (bl[i].style.display === 'none') {
            bl[i].style.display = 'block';
            lis[i].firstElementChild.nextElementSibling.textContent = "-";
          } else {
            bl[i].style.display = 'none';
            lis[i].firstElementChild.nextElementSibling.textContent = "+";
          }
        });
      }
  }
    function dd(event) {
      
          event.preventDefault();
          var token = document.querySelector("input[type=hidden]").value;
          var checkboxes = document.querySelectorAll('input[type=checkbox]:checked');
          var json_obj = {};
          var callbackURL = `{% url 'pproducts:rfsh_products' %}`;
          if (checkboxes.length > 0) {
            for (let i = 0; i < checkboxes.length; i++) {
              var label = checkboxes[i].parentNode.textContent.replace(/[\n\r]+|[\s]{2,}/g, ' ').trim();
              var val = checkboxes[i].value;
              json_obj[label] = checkboxes[i].value;
            }
            $.ajax({
              type: 'POST',
              headers: { "X-CSRFToken": token },
              dataType: "json",
              data: json_obj,
              url: callbackURL,
              success: function(response) {
                
                if (response) {
                  alert("OK 200");
                  var list2 = response.dataset
                  for (var x in list2) {
                    var record = list2[x];
                //     create outer container tt12
                    var tt12 = document.createElement('div');
                //     create expand box
                    var expand_box = document.createElement('div');
                    var p = document.createElement('p');
                    p.textContent = x;
                    expand_box.addEventListener("click", function(event) {
                      var evt = event.target.parentNode.lastChild
                    })
                    var exp_icon = document.createElement('span');
                    exp_icon.textContent = "+";
                    // create classes for expand box
                    tt12.classList.add("tt12");
                    expand_box.classList.add("expandbox")
                    p.classList.add("xp23")
                    expand_box.append(p,exp_icon);
                //    create sibling
                    var sole_div = document.createElement('div')
                    // add first 2 children before the products
                    tt12.appendChild(expand_box);
                    tt12.appendChild(sole_div);
                    var fieldset = document.createElement('fieldset');
                    fieldset.classList.add("xp24")
                    for (let q = 0; q < list2[x].length; q++) {
                        var outer_div = document.createElement('div');
                        var inner_div = document.createElement('div');
                        var br = document.createElement('br');
                        var label = document.createElement('label');
                        label.textContent = `Name: ${record[q].name} Description: ${record[q].description}`;
                        outer_div.classList.add("qp");
                        inner_div.appendChild(label)
                        outer_div.appendChild(inner_div);
                        var checkbox = document.createElement('input');
                        checkbox.type = "checkbox";
                        outer_div.appendChild(checkbox)
                        fieldset.append(outer_div, br);
                      
                    }
                    tt12.appendChild(fieldset);
                    var cont = document.getElementById("id_select_box8");
                    cont.appendChild(tt12);
                  }
                  pleasework();
                }
              },
              error: function(xhr) {
               alert("error")
              }
            })
          }
        }
// used to loop through and add event handlesr

        function addEventsDropDown() {
          var lis = document.querySelectorAll(".expandbox");
          var bl = document.querySelectorAll("#id_select_box8  .xp24");
            
            for (let i = 0; i < lis.length; i++) {
              lis[i].addEventListener('click', (event) => {
                  
        
                if (bl[i].style.display === 'none') {
                  bl[i].style.display = 'block';
                  lis[i].firstElementChild.nextElementSibling.textContent = "_";
                } else {
                  bl[i].style.display = 'none';
                  lis[i].firstElementChild.nextElementSibling.textContent = "+";
                }
              });
            }
          }