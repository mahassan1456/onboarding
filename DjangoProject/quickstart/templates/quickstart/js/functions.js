




function populateName(event) {
    var value = event.target.value 
    var hospitalName = document.getElementById('hospitalNameBox')
    if (value) {
        hospitalName.style.display = 'none'
        hospitalName.previousElementSibling.style.display = 'none';
    } else {
      hospitalName.style.display = 'block'
      hospitalName.previousElementSibling.style.display = 'block';
    }
  }

  function populateSelections(event) {
    var value = event.target.value;
    var hospital_label = document.getElementById('hospitalModelLabel');
    var hospital_model_field = document.getElementById('hospitalModelField');
    var hospital_name_box = document.getElementById('hospitalNameBox');
    var hospital_name_box_label = document.getElementById('hospitalNameBoxLabel')
    var hospitalInvite = document.getElementById('hospitalInvite')
    var hospitalInviteLabel = document.getElementById('hospitalInviteLabel')
    var newHospitalZip = document.getElementById('newHospitalZip')
    var newHospitalZipLabel = document.getElementById('newHospitalZipLabel')

    if (value == 'new') {

      hospital_name_box.style.display = "block";
      hospital_name_box_label.style.display = 'block'
      newHospitalZip.style.display = 'block'
      newHospitalZipLabel.style.display = 'block'
      hospital_label.style.display = 'none';
      hospital_model_field.style.display = 'none';
      hospitalInvite.style.display = 'none';
      hospitalInviteLabel.style.display = 'none';
    } else if (value == 'onboarded') {
      hospital_label.style.display = 'block';
      hospital_model_field.style.display = 'block';
      hospital_name_box.style.display = "none";
      hospital_name_box_label.style.display = 'none'
      newHospitalZip.style.display = 'none'
      newHospitalZipLabel.style.display = 'none'
      hospitalInvite.style.display = 'none';
      hospitalInviteLabel.style.display = 'none';
    } else {
      hospitalInvite.style.display = 'block';
      hospitalInviteLabel.style.display = 'block';
      hospital_name_box.style.display = "none";
      hospital_name_box_label.style.display = 'none'
      newHospitalZip.style.display = 'none'
      newHospitalZipLabel.style.display = 'none'
      hospital_label.style.display = 'none';
      hospital_model_field.style.display = 'none';
    }
  }