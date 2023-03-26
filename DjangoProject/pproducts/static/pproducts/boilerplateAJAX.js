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