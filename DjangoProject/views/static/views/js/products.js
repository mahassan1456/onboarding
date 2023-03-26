function filterAlltoSpecific(event) {
    console.log("TETTTTTTTTTTT")
  // POST request must account for the CSRF TOKEN to Prevent Cross-Site-Request-Forgery
  var outercont = document.getElementById('outer-cont-holder');
  var csrf_token = document.querySelector("input[name=csrfmiddlewaretoken]").value;
  var leftbutton = document.getElementById('leftbuttonfilter');
  var rightbutton = document.getElementById('rightbuttonfilter');
  var filterValue = event.target.value
  var json_obj = {};
  json_obj['filter'] = filterValue
  var callbackURL = "/pproducts/products/allorcurrent/"
  
  $.ajax({
      type: 'POST',
      headers: { "X-CSRFToken": csrf_token },
      dataType: "json",
      data: json_obj,
      url: callbackURL,
      // Receiving JSON Response Back from DB
      success: function(response) {
        if (response) {
            buildProductCards(response,outercont);
        }
        event.target.style.backgroundColor = '#0fa942';
        if (filterValue.includes('all') ) {
            rightbutton.style.backgroundColor = '';
        } else  {
            leftbutton.style.backgroundColor = '';
        }
        // if (filterValue == 'all') {
        //     event.target.style.backgroundColor = 'green';
        // } else {
        //     event.target.style.backgroundColor = 'green';
        // }
        // Write Javascript function here
      },
      error: function() {
      console.log('error')
    }
  })
}

  function resetDropDown(selectBox,label,dataset=[]) {
    var filterBox = document.getElementById('filterbox')
    filterBox.style.display = 'none'
    selectBox.innerHTML = "";
    var option = document.createElement('option');
    option.value = "";
    option.selected = true;
    option.textContent = `Please Select a ${label}`
    selectBox.appendChild(option)
    if (label == 'Specialty') {
        var option1 = document.createElement('option');
        option1.value = 'all';
        option.textContent = 'All';
        option.selected = false;
        selectBox.appendChild(option1)
    }
    
   
  }

  function resetDropDown1(selectBox,label,dataset=[]) {
    var filterBox = document.getElementById('filterbox')
    filterBox.style.display = 'none'
    selectBox.innerHTML = "";
    var option = document.createElement('option');
    option.value = "";
    option.selected = true;
    option.textContent = `Please Select a ${label}`
    selectBox.appendChild(option)

    // if (label == 'Specialty') {
    //     console.log("testing")
    // }


  }

  function populateDropDownSpecialty(event) {
  // POST request must account for the CSRF TOKEN to Prevent Cross-Site-Request-Forgery
    var csrf_token = document.querySelector("input[name=csrfmiddlewaretoken]").value;
    var physicianValue = event.target.value;
    var specialtySelect = document.getElementById('selectboxspecialty');
    // if (!physicianValue) {
    //     console.log("right here")
    //     resetDropDown(specialtySelect,'Specialty')
    //     return

    // }
    var json_obj = {}
    json_obj['physicians'] = physicianValue
    console.log("from populateDropDownSpecialty", json_obj)
    var callbackURL = "{% url 'pproducts:buildSpecialties' %}"
    $.ajax({
        type: 'POST',
        headers: { "X-CSRFToken": csrf_token },
        dataType: "json",
        data: json_obj,
        url: callbackURL,
        // Receiving JSON Response Back from DB
        success: function(response) {

            if (response.dataset) {
                console.log(response)
                var dataset = response.dataset;
                rebuildSelections(dataset,'selectboxspecialty','Specialty')
                // resetDropDown(specialtySelect,'Specialty');
                // console.log('specialtyyyyyfchk',dataset)
                // for (let i = 0;i < dataset.length; i++) {

                //     var HTML = `<option value=${dataset[i][1]} name="specialty"> ${dataset[i][1]}</option>`
                //     specialtySelect.insertAdjacentHTML('beforeend', HTML)

                // }

            }


            // Write Javascript function here
        },
        error: function() {
        console.log('error')
        }
    })
    }
  function rebuildPhysicians(dataset,id='',label='',flag=false) {
    var select = document.getElementById("select-physician-id");
    select.innerHTML = "";
    var option = document.createElement('option');
    option.value = "";
    option.selected = true;
    option.textContent = 'Please Select a Physician'
    select.appendChild(option)
    var option2 = document.createElement('option');
    option2.value = "all";
    option2.selected = false;
    option2.textContent = "All"
    select.appendChild(option2)
    
    for (var i = 0; i < dataset.length; i++) {
        var HTML = `<option value=${dataset[i][0]} id="nametitle-physician" name="physician"> ${dataset[i][1]}  ${dataset[i][2]}</option>`
        select.insertAdjacentHTML('beforeend', HTML)
    }
  }
  function rebuildSelections(dataset,id='',label='',flag=false) {
    var select = document.getElementById(id);
    select.innerHTML = "";
    var option = document.createElement('option');
    option.value = "";
    option.selected = true;
    option.textContent = `Please Select a ${label}`
    select.appendChild(option)
    var option2 = document.createElement('option');
    option2.value = "all";
    option2.selected = false;
    option2.textContent = "All"
    select.appendChild(option2)
    if (label == 'Physician') {
    for (var i = 0; i < dataset.length; i++) {
        var HTML = `<option value=${dataset[i][0]} id="nametitle-physician" name="physician"> ${dataset[i][1]}  ${dataset[i][2]}</option>`
        select.insertAdjacentHTML('beforeend', HTML)
    }
   } else {
    for (var i = 0; i < dataset.length; i++) {
        var HTML = `<option value=${dataset[i][1]} id="nametitle-physician" name="physician"> ${dataset[i][1]} </option>`
        select.insertAdjacentHTML('beforeend', HTML)
    }
   }
  }

  function rebuildSpecialties(event) {
    return
  }

  function populateDropDownPhysician(event) {

        var outercont = document.getElementById('outer-cont-holder');
        var facility_id = event.target.value
        console.log(event.target)
        console.log('facility_id',facility_id)
        var selectPhysician = document.getElementById("select-physician-id");
        var selectBoxSpecialty = document.getElementById('selectboxspecialty')
        var facilitySpecialty = document.getElementById('select-hospital-id')
        var selectPhysicianValue = selectPhysician.value
        outercont.innerHTML = ""
        // resetDropDown(selectPhysician,'Physician')
        // resetDropDown(selectBoxSpecialty,'Specialty')

        
        // if (!facility_id) {
        //     outercont.innerHTML = ""
        //     resetDropDown(selectPhysician,'Physician')
        //     resetDropDown(selectBoxSpecialty,'Specialty')
        //     return;
        // } else if (selectPhysician.value || selectBoxSpecialty.value ) {
        //     console.log()
        // }
        console.log(facility_id)
        var csrf_token = document.querySelector("input[name=csrfmiddlewaretoken]").value;
        var json_obj = {}
        json_obj['facility'] = facility_id;
        json_obj['specialty'] = selectBoxSpecialty.value
        json_obj['physician'] = selectPhysician.value
        var callbackURL = "/pproducts/filter/hospital/"
        $.ajax({
            type: 'POST',
            headers: { "X-CSRFToken": csrf_token },
            dataType: "json",
            data: json_obj,
            url: callbackURL,
            // Receiving JSON Response Back from DB
            success: function(response) {
                console.log(response)

                if (response.dataset) {
                    console.log(response.dataset)
                    var dataset = response.dataset
                    var outerContainer = document.getElementById("select-box-child2");
                    // var select = document.getElementById("select-physician-id");
                    // select.innerHTML = "";
                    // var option = document.createElement('option');
                    // option.value = "";
                    // option.selected = true;
                    // option.textContent = 'Please Select a Physician'
                    // select.appendChild(option)
                    // ddddd
                    // resetDropDown(selectPhysician,'Physician')
                    // rebuildPhysicians(dataset)
                    rebuildSelections(dataset,'select-physician-id','Physician')
                    // for (var i = 0; i < dataset.length; i++) {
                    //     var HTML = `<option value=${dataset[i][0]} id="nametitle-physician" name="physician"> ${dataset[i][1]}  ${dataset[i][2]}</option>`
                    //     selectPhysician.insertAdjacentHTML('beforeend', HTML)
                    // }
                    
                    console.log("finished populating physicians")
 
                
                // NEW ADDED
                console.log("started here")
                console.log('facility_id',facility_id,"selectphysician",selectPhysician,"response specialty",response.specialties)
                if ( (!facility_id || !selectPhysicianValue) && response.specialties) {
                    console.log("came inside")
                    var datasetS = response.specialties
                    rebuildSelections(datasetS,'selectboxspecialty','Specialty')
                    // resetDropDown(selectBoxSpecialty,'Specialty')
                    // for (var i = 0; i < datasetS.length; i++) {
                    //     var HTML = `<option value=${datasetS[i][1]} id="nametitle-physician" name="physician"> ${datasetS[i][1]}</option>`
                    //     selectBoxSpecialty.insertAdjacentHTML('beforeend', HTML)

                    // }
                } else if (facility_id && selectBoxSpecialty.value == 'all') {
                    buildProductCards(response,outercont)
                }
              }
                // Write Javascript function here
            },
            error: function() {
            console.log('error')
            }
        })
        return
  }
  function buildProductCards(response,outercont,f='') {
        console.log("buildproductcards",response)
        var dataset = response.dataset;
        if (!dataset) {
        outercont.innerHTML = "";
            return
        }
        var sspecialty = response.specialty
        var pphysician = response.physician
        var physician_id = response.physician_id
        // if (sspecialty && pphysician) {
        //     console.log("specialty TRUE physician TRUE")
        // }
        // else if (pphysician && !sspecialty) {
        //     console.log("physician TRUE specialty FALSE")
        // 
        // else if (!pphysician && sspecialty) {
        //     console.log("physician TRUE specialty FALSE")
        // }
        var subheading = document.getElementById('productTitleTag')
        subheading.textContent = sspecialty;
        outercont.innerHTML = ""
        console.log("dataset length",dataset.length)
        for (let i = 0; i < dataset.length; i++) {
        
        var addProductsURL = '/pproducts/addproducts/physician/' + dataset[i][0]['id'] + '/?specialty=' + dataset[i][2]
        var card = document.createElement('div')
        card.classList.add('card')
        var card_header = document.createElement('div')
        card_header.classList.add('card-header')
        
        var html = `<img src='${dataset[i][1]}' alt='rover'/ width=100 height=100>`
        card_header.insertAdjacentHTML('beforeend', html);
        var card_body = document.createElement('div');
        card_body.classList.add('card-body');
        
        html = `
        <span class="tag tag-teal" class="tagselection">${dataset[i][2]}</span>
            
        <h4>
            ${dataset[i][0]['name']}
        </h4>
        <p>
            ${dataset[i][0]['description']}
        </p>
        <div class="outer-container-button">
          <a id="link2addprod" href="${addProductsURL}"><button id="more_details">Add Product</button></a>
        </div>
        `
        card_body.insertAdjacentHTML('beforeend', html)
        card.appendChild(card_header)
        card.appendChild(card_body)
        outercont.appendChild(card);
        var filterBox = document.getElementById('filterbox')
        var leftbutton = document.getElementById('leftbuttonfilter')
        var rightbutton = document.getElementById('rightbuttonfilter')
        leftbutton.value = `all-${sspecialty}-${physician_id}`
        rightbutton.value = `current-${sspecialty}-${physician_id}`
        filterBox.style.display = 'block';
        


        if (response.superuser) {
            console.log("testing to see it it makes it")
            var editURL = '/pproducts/product/edit/' + dataset[i][0]['id'] + `/?specialty=${dataset[i][2]}` 
            var tagLabel = card_body.firstElementChild
            var link = `<span><a class="editproductlink" href="${editURL}"> Edit Product </a></span>`
            tagLabel.insertAdjacentHTML('afterend', link)
            var editspecialtylink = document.getElementById("editspecialtyview")
        //     if (response.specialtyid) {
        //     if (editspecialtylink) {
        //     editspecialtylink.href = `/pproducts/products/tags/${response.specialtyid}/`
        //     } else {
        //     var titleBox = document.getElementById("titleBox")
        //     var anchor = document.createElement("a")
        //     var HREF = `/pproducts/products/tags/${response.specialtyid}/`
        //     var HTML = `<a  id="editspecialtyview" href="${HREF}" id="addTags"> Edit Specialty + </a>`
        //     titleBox.insertAdjacentHTML("beforeend", HTML)
        //     }
        //     console.log("testing to see it it makes it2")
        //    } else {
        //         if (editspecialtylink) {
        //             editspecialtylink.remove()
        //         }
        //     }



          } 
        }
        
}

// I can make a function later that just works with the lat drop down box
  function displayProductsPhysicianSpecialty(event) {
    var outercont = document.getElementById('outer-cont-holder');
    var csrf_token = document.querySelector("input[name=csrfmiddlewaretoken]").value;
    var physician_select = document.getElementById('select-physician-id').value;
    var specialty_select = document.getElementById('selectboxspecialty').value;
    
    var hospital_select =  document.getElementById('select-hospital-id').value;
    var filterBox = document.getElementById('filterbox')
    var headerNoProducts = document.getElementById('headerNoProducts')
    console.log(physician_select,'physician select')
    if (!specialty_select) {
        outercont.innerHTML = ""
        filterBox.style.display = 'none';
        headerNoProducts.style.display = 'block';
        return
        // calculates any other combination with specialaty selected
    } else  {
        if (!physician_select || (specialty_select=='all' && physician_select =='all')) {
            console.log("here it landed")
            filterBox.style.display = 'none';
            // if (specialty_select == 'all') {
            //     console.log()
            // }
        } else {
            filterBox.style.display = 'block';
        }
        document.getElementById('headerNoProducts').style.display = 'none';
    } 
    // var physician_value = document.
    var json_obj = {}
    json_obj['specialty'] = specialty_select;
    json_obj['physician'] = physician_select;
    json_obj['facility'] = hospital_select;
    console.log(json_obj)
    var callbackURL = "/pproducts/filterproducts/script/";
        $.ajax({
        type: 'POST',
        headers: { "X-CSRFToken": csrf_token },
        dataType: "json",
        data: json_obj,
        url: callbackURL,
        // Receiving JSON Response Back from DB
        success: function(response) {

            if (response) {
                console.log("IT MADE IT HERE before buildproductcards", response)
                buildProductCards(response,outercont)
            } else {
                outercont.innerHTML = '<h3> There is an Error Processing Your Request. Please try again later </h3>'
            }
            
            // Write Javascript function here
        },
        error: function() {
        console.log('error')
        }
    })
  }
  function displayProducts(event) {
    var outercont = document.getElementById('outer-cont-holder');
    console.log(event.target.value)
    if (event.target.value == "None") {
      var editspecialtylink = document.getElementById("editspecialtyview")
      editspecialtylink.remove()
      outercont.innerHTML = "";
      return
    }
    var token = document.querySelector("input[name=csrfmiddlewaretoken]").value;
    console.log("testing")
    var hiddenfield = document.getElementById('hidden_physician_id');
    if (hiddenfield) {
      hiddenfield_value = hiddenfield.value;
      console.log("hidden field", hiddenfield_value)
    } else {
      hiddenfield_value = 0
    }

    var json_obj = {}
    var specialty_label = event.target.value
    json_obj['specialty'] = event.target.value; 
    json_obj['physician_id'] = hiddenfield_value;
    var callbackURL = "{% url 'pproducts:displayproducts' %}"
    var mediaURL = "{{MEDIA_URL}}" 
    console.log(mediaURL,'media')

    $.ajax({
              type: 'POST',
              headers: { "X-CSRFToken": token },
              dataType: "json",
              data: json_obj,
              url: callbackURL,
              // Receiving JSON Response Back from DB
              success: function(response) {
                console.log(response)
                if (response) {
                  var dataset = response.dataset;
                  if (!dataset) {
                    outercont.innerHTML = "";
                    return
                  }
                  var sspecialty = response.specialty
                  var productdataset = response.products
                 
                  // var subheading = document.getElementById('productTitleTag')
                  // subheading.textContent = sspecialty;
                  outercont.innerHTML = ""
                  for (let i = 0; i < dataset.length; i++) {
                  
                    var addProductsURL = '/pproducts/addproducts/physician/' + dataset[i][0]['id'] + '/?specialty=' + specialty_label 
                    var card = document.createElement('div')
                    card.classList.add('card')
                    var card_header = document.createElement('div')
                    card_header.classList.add('card-header')
                    
                    var html = `<img src='${dataset[i][1]}' alt='rover'/ width=100 height=100>`
                    card_header.insertAdjacentHTML('beforeend', html);
                    var card_body = document.createElement('div');
                    card_body.classList.add('card-body');
                    
                    html = `
                    <span class="tag tag-teal" class="tagselection">${specialty_label}</span>
                     
                    <h4>
                      ${dataset[i][0]['name']}
                    </h4>
                    <p class="card-desc-box">
                        ${dataset[i][0]['description']}
                    </p>
                    <div class="outer-container-button">
                        <button id="more_details"><a id="link2addprod" href="${addProductsURL}">Add Product</a></button>
                    </div>
                    `
                    card_body.insertAdjacentHTML('beforeend', html)
                    card.appendChild(card_header)
                    card.appendChild(card_body)
                    outercont.appendChild(card);

                    if (response.superuser) {
                      console.log("testing to see it it makes it")
                      var editURL = '/pproducts/product/edit/' + dataset[i][0]['id'] + `/?specialty=${sspecialty}` 
                      var tagLabel = card_body.firstElementChild
                      var link = `<span><a class="editproductlink" href="${editURL}"> Edit Product </a></span>`
                      tagLabel.insertAdjacentHTML('afterend', link)
                      var editspecialtylink = document.getElementById("editspecialtyview")

                      if (editspecialtylink) {
                        editspecialtylink.href = `/pproducts/products/tags/${response.specialtyid}/`
                      } else {
                        var titleBox = document.getElementById("titleBox")
                        var anchor = document.createElement("a")
                        var HREF = `/pproducts/products/tags/${response.specialtyid}/`
                        var HTML = `<a  id="editspecialtyview" href="${HREF}" id="addTags"> Edit Specialty + </a>`
                        titleBox.insertAdjacentHTML("beforeend", HTML)
                      }
                     } 
                    }
                   }

              },
              error: function() {
              console.log('error')
            }
        })
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