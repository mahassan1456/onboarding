function dropProducts(event) {
  var ul = event.target.parentElement.nextElementSibling;

  var span = event.target
  if (ul!=null) {
    if (ul.style.display == 'block') {
      console.log('1st')
      span.textContent = "+"
      ul.style.display = 'none';
    } else {
      console.log('2nd')
      span.textContent = "-"
      ul.style.display = 'block';
    }
  }
}
  
function boilerplateJavascript(event) {
  // POST request must account for the CSRF TOKEN to Prevent Cross-Site-Request-Forgery
  var _csrf_token = document.querySelector("input[type=hidden]").value;
  var json_obj = {"Test": 15}
  var callbackURL = "/pproducts/etc/etc/?querystring=ifneeded"
  $.ajax({
      type: 'POST',
      headers: { "X-CSRFToken": csrf_token },
      dataType: "json",
      data: json_obj,
      url: callbackURL,
      // Receiving JSON Response Back from DB
      success: function(response) {
        // Write Javascript function here
      },
      error: function() {
      console.log('error')
    }
  })
}
    
    
    
    
    
    function refreshProducts23(event) {
        
        // In order to submit a POST ajax request the button must be in a form. If the button is not the actual submit button a function
        // must be called on the event to prevent the default behavior of form submission
            event.preventDefault();
            console.log('printme')
            var token = document.querySelector("input[type=hidden]").value;
            var id_select_box8 = document.getElementById("accordion");
            if (event.target.value == 'clear') {
                id_select_box8.innerHTML = ""
                var inputs = document.querySelectorAll("input[type=checkbox]:checked");
                for (let checkbox of inputs) {
                    checkbox.checked = false
                }
                return;
            }
            // var specialty_heading_products = event.target.parentElement.textContent
            var specialty_heading_products = event.target.getAttribute("data-tag")
            console.log('sssssssss',specialty_heading_products)
            if (!event.target.checked) {
                console.log(event.target)
                console.log("what the fuck is going on did u make it here",specialty_heading_products)
                var products_set = document.getElementById(specialty_heading_products)
                products_set.remove()
                return
            } else {

                json_obj = {'lookup':specialty_heading_products}
                // json_obj['lookup'] = specialty_heading_products;
                var callbackURL = '/quickstart/build/products/';
                $.ajax({
                type: 'POST',
                headers: { "X-CSRFToken": token },
                dataType: "json",
                data: json_obj,
                url: callbackURL,
                // Receiving JSON Response Back from DB
                success: function(response) {
                    console.log('response',response)
                    if (response) {
                    
                    var products = response.dataset;
                    var specialty = response.specialty
                    var accordion = document.getElementById('accordion');
                    var li = document.createElement('li');
                    li.id = specialty.toLowerCase()
                    console.log(li.id,'li.id')
                    var HTML_TITLE = `<h4 class="xp23" onclick="dropProducts(event)">${specialty} <span class="plusminus">+</span></h4>`
                    li.insertAdjacentHTML('beforeend', HTML_TITLE)
                    var ul = document.createElement('ul')
                    ul.classList.add("listing")
                    ul.id = `${specialty.toUpperCase()}_show`
                    var media_url = '/media/'
                    console.log(response.dataset,'ddddssss')
                    for (var product of products) {
                        
                        var newURL = `${product[1]}`
                        
                        var product_li = `<li><a href="#" class="rc_product_img"><img src="${newURL}"></a><label>${product[0]}<input type="checkbox" name="${specialty}-" value="${product[0]}" ></label><a href="#"  data-toggle="modal" onclick="buildDetails(event)" data-product="${product[3]}" data-target="#product_detail" class="view_details">  (View Product Details) </a></li>`
                        ul.insertAdjacentHTML('beforeend',product_li)
        
                        }

                        li.appendChild(ul)
                        accordion.appendChild(li)
                    }
                    },
                    error: function() {
                    console.log('error')
              }
            })
           }    
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
  