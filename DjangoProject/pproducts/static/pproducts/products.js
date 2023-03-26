function displayProducts(event) {
    var token = document.querySelector("input[type=hidden]").value;
    var json_obj = {}
    var specialty_label = event.target.value
    json_obj['specialty'] = event.target.value; 
    var callbackURL = "{% url 'pproducts:displayproducts' %}"

    $.ajax({
              type: 'POST',
              headers: { "X-CSRFToken": token },
              dataType: "json",
              data: json_obj,
              url: callbackURL,
              // Receiving JSON Response Back from DB
              success: function(response) {
                
                if (response) {
                 
                  var outercont = document.getElementById('outer-cont-holder');
                  var dataset = response.dataset;
                  
                  outercont.innerHTML = ""
                  for (let i = 0; i < dataset.length; i++) {
                  
                    var URL2 = '/pproducts/addproducts/physician/' + dataset[i]['id'] + '/'
                    console.log(URL2)
                    var card = document.createElement('div')
                    card.classList.add('card')
                    var card_header = document.createElement('div')
                    card_header.classList.add('card-header')
                    var html = "<img src='/media/uploads/abc.jpeg' alt='rover'/>"
                    card_header.insertAdjacentHTML('beforeend', html);
                    var card_body = document.createElement('div');
                    card_body.classList.add('card-body');
                    html = `
                    <span class="tag tag-teal">${specialty_label}</span>
                    <h4>
                      ${dataset[i]['name']}
                    </h4>
                    <p>
                        ${dataset[i]['description']}
                    </p>
                    <div class="outer-container-button">
                        <button id="more_details"><a id="link2addprod" href="${URL2}">Add Product</a></button>
                    </div>
                    `
                    card_body.insertAdjacentHTML('beforeend', html)
                    card.appendChild(card_header)
                    card.appendChild(card_body)
                    outercont.appendChild(card);
                    
                  } 
               
                }

               },
               error: function() {
                console.log('error')
              }
            })
  }