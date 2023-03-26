function addEventsDropDown(event) {
    var fieldset = event.target.parentNode.nextElementSibling.nextElementSibling;
    var collapseIcon = event.target.parentNode.lastElementChild;
    if (fieldset.style.display === 'none') {
      fieldset.style.display = 'block';
      collapseIcon.textContent = "_";
    } else {
      fieldset.style.display = 'none';
      collapseIcon.textContent = "+";
    }   
    }
  
  function existingSelections(existingFieldSets) {
      var obj = {}
      for (var i = 0; i < existingFieldSets.length; i++) {
        var specialty = existingFieldSets[i].name
        console.log(existingFieldSets[i].querySelectorAll('input[type=checkbox]:checked').length)
        var specialtyProductsLength = existingFieldSets[i].querySelectorAll('input[type=checkbox]:checked');
  
        if (specialtyProductsLength.length > 0) {
          console.log(specialtyProductsLength[0].value);
          var arr = Array.from(specialtyProductsLength, (x) => 'current-' + x.value );
          console.log(arr);
          obj[specialty] = arr;
        } 
      }
      return obj
        
  }
          function refreshProducts2(event) {
        
        // In order to submit a POST ajax request the button must be in a form. If the button is not the actual submit button a function
        // must be called on the event to prevent the default behavior of form submission   
            event.preventDefault();
            var id_select_box8 = document.getElementById("id_select_box8");
            if (event.target.value == 'clear') {
              console.log("what the fuck")
              id_select_box8.innerHTML = ""
              var inputs = document.querySelectorAll("input[type=checkbox]:checked");
            
              for (let checkbox of inputs) {
                checkbox.checked = false
              }
              return;
            }
            var token = document.querySelector("input[type=hidden]").value;
            // var checkboxes = document.querySelectorAll('input[type=checkbox]:checked');
            // remove maybe
            var id_select_box2 = document.getElementById("id_select_box2");
            // if issues changes below id_select_box2 to document
            var checkboxes = id_select_box2.querySelectorAll('input[type=checkbox]:checked');
            // remove maybe
          
            var xp23 = document.getElementsByClassName('xp23');
            xp23 = Array.from(xp23, (x) => x.textContent.toLowerCase())
            var newSelections = Array.from(checkboxes, (x) => x.parentElement.textContent.replace(/[\n\r]+|[\s]{2,}/g, ' ').trim().toLowerCase())
            var json_obj = {};
            var callbackURL = '/pproducts/refresh/';
             if (checkboxes.length > 0) {
  
            var commonElements = xp23.filter(val => newSelections.includes(val))
          
           
            if (xp23.length == 0 || commonElements.length == 0) {
              
              id_select_box8.innerHTML = "";
              json_obj['lookup'] = newSelections;
  
            } else {
              var difference = newSelections.filter(val => !xp23.includes(val))
              json_obj['lookup'] = difference; 
                if (commonElements.length != xp23.length ) {
                  var removal = xp23.filter(val => !newSelections.includes(val))
              
                
                  for (var i = 0; i < removal.length; i++) {
                        var removedElement = document.getElementById(removal[i].toLowerCase())
                        var fieldsetremoved = removedElement.parentElement.parentElement
                        fieldsetremoved.remove()
                  }
              }
            }
              $.ajax({
                type: 'POST',
                headers: { "X-CSRFToken": token },
                dataType: "json",
                data: json_obj,
                url: callbackURL,
                // Receiving JSON Response Back from DB
                success: function(response) {
  
                  if (response) {
                    
                    var products = response.dataset
                    for (var specialty in products) {
                      var parentContainer = document.createElement('div')
                      id_select_box8.appendChild(parentContainer)
                      idselecttext = `<div class="expandbox">
                                          <p class="xp23" id="${specialty.toLowerCase()}">${specialty.toUpperCase()}</p>
                                          <span class="collapse-icon" onclick="addEventsDropDown(event)">+</span>
                                       </div>
                                       <div></div>
                                       <fieldset class="xp24" style="display:none;" name="xp12"></fieldset>`
                        parentContainer.insertAdjacentHTML('beforeend', idselecttext)
                        var fieldset = parentContainer.lastElementChild;
                        
                        for (var product in products[specialty]) {
                            var prod = products[specialty][product]
                            var productURL = '/pproducts/addproducts/physician/' +  prod.id + '/?specialty=' + specialty        
                            fieldsettext =
                            `<div class="qp">
                                <div>
                                    <label for=${specialty+prod.id}> <h6 style="display:inline;"><span class="bullet">&#x2022;</span><strong> Name: </strong></h6><a style="color:blue;" href="${productURL}"> ${prod.name}</a> </label>
                                    <div class="description">
                                      <br>
                                      <span class="description-product"> <h6 style="display:inline;"><strong> Description: </strong> </h6> ${prod.description} </span>
                                    </div>
                                    <a class"additionalInfo" style="color:blue;" onclick="additionalInfo(event)">&nbsp| More </a>
                                </div>
                                <input id=${specialty+prod.id} value=${prod.id} type="checkbox" name=prod-${specialty}>
                            </div>
                            <br>`
                          fieldset.insertAdjacentHTML('beforeend',fieldsettext)
                          }
                        }
                    }
                 },
                 error: function() {
                  console.log('error')
                }
              })
            } else {
              id_select_box8.innerHTML = "";
            }
          }
  function populateExistingProducts(event) {
    return
  }
  function additionalInfo() {
    var element = event.target;
    
    if (element.previousElementSibling.style.display == 'inline') {
      element.previousElementSibling.style.display = 'none';
      element.textContent = " | More";
    } else {
      element.previousElementSibling.style.display = 'inline';
      element.textContent = " | Less";
    }
  }
  
  // function editornew(event) {
  //   var editflag = "{{edit}}"
   
  //   if (editflag == 'True') {
  //     populateExistingProducts()
  //   } else {
  //     refreshProducts()
  //     console.log("false")
  //   }
  // }
  // editornew()
  
  function refreshProducts(event) {
        
        // In order to submit a POST ajax request the button must be in a form. If the button is not the actual submit button a function
        // must be called on the event to prevent the default behavior of form submission   
            // event.preventDefault();
            
            // var token = document.querySelector("input[type=hidden]").value;
            // var checkboxes = document.querySelectorAll('input[type=checkbox]:checked');
            // var id_select_box8 = document.getElementById("id_select_box8");
            // var json_obj = {};
            // var callbackURL = `{% url 'pproducts:rfsh_products' %}`;
            event.preventDefault();
  
            if (event.target.value == 'C')
            
            var id_select_box8 = document.getElementById("id_select_box8");
            var token = document.querySelector("input[type=hidden]").value;
            // var checkboxes = document.querySelectorAll('input[type=checkbox]:checked');
            var id_select_box2 = document.getElementById("id_select_box2");
            // if issues changes below id_select_box2 to document
            var checkboxes = id_select_box2.querySelectorAll('input[type=checkbox]:checked');
            
            var xp23 = document.getElementsByClassName('xp23');
            xp23 = Array.from(xp23, (x) => x.textContent.toLowerCase())
            var newSelections = Array.from(checkboxes, (x) => x.parentElement.textContent.replace(/[\n\r]+|[\s]{2,}/g, ' ').trim().toLowerCase())
            console.log(xp23)
            console.log(newSelections)
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
                // Receiving JSON Response Back from DB
                success: function(response) {
                  
                  if (response) {
                    
                    var products = response.dataset
          
                    id_select_box8.innerHTML = "";
                    for (var specialty in products) {
                      
                      id_select_box8.innerHTML = id_select_box8.innerHTML + 
                      `<div class="expandbox">
                            <p class="xp23">${specialty.toUpperCase()}</p>
                            <span class="collapse-icon" onclick="addEventsDropDown(event)">+</span>
                       </div>
                       <div></div>
                       <fieldset class="xp24" style="display:none;" name="xp12"></fieldset>`
                       var fieldset = id_select_box8.lastElementChild;
                       
                        for (var product in products[specialty]) {
                            var prod = products[specialty][product]
                            fieldset.innerHTML = fieldset.innerHTML +
                            `<div class="qp">
                                <div>
                                    <label for=${specialty+prod.id}> <h6 style="display:inline;"><span class="bullet">&#x2022;</span><strong> Name: </strong></h6> ${prod.name} </label>
                                    <div class="description">
                                      <br>
                                      <span class="description-product"> <h6 style="display:inline;"><strong> Description: </strong> </h6> ${prod.description} </span>
                                    </div>
                                    <a class"additionalInfo" style="color:blue;" onclick="additionalInfo(event)">&nbsp| More </a>
                                </div>
                                <input id=${specialty+prod.id} value=${prod.id} type="checkbox" name=prod-${specialty}>
                            </div>
                            <br>`
                          }
                        }
                    }
                 },
                error: function(xhr) {
                 alert("error")
                }
              })
            } else {
              id_select_box8.innerHTML = "";
            }
          }