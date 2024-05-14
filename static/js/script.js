var maltarea = document.getElementById("textarea1");
var engtarea = document.getElementById("textarea2");

var current;
var cmv, cev;

document.addEventListener('DOMContentLoaded', function() {
  fetchTextPairs();
});

function fetchTextPairs(){
  fetch(textURL, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrf_token,
    },
  })
  .then(response => response.json())
  .then(data => {
    if(data.malayalam && data.english){
    maltarea.value = data.malayalam;
    engtarea.value = data.english;
    cmv = data.malayalam;
    cev = data.english;}
    current = data.pk
    if(data.status && data.status == 100){appendAlert(data.message, 'success')}
  })
  .catch(error => {
    // Handle any errors
    console.error('Error fetching data:', error);
  });
}

yesBtn = document.getElementById("btn1");
noBtn = document.getElementById("btn2");

yesBtn.addEventListener("click", (e) => {
  e.preventDefault();
  if (current){
  formData = new FormData();
  formData.append('pk', current);
  formData.append('rating', true);
  yesornoEvent(yesBtn, noBtn, formData);
  data_check_and_save();
  }
  else{
    appendAlert("Data Unavailable", 'danger');
  }
});


noBtn.addEventListener("click", (e) => {
  e.preventDefault();
  if (current){
  formData = new FormData();
  formData.append('pk', current);
  formData.append('rating', false);
  yesornoEvent(yesBtn, noBtn, formData);
  data_check_and_save();
  }
  else{
    appendAlert("Data Unavailable", 'danger');
  }
});


function data_check_and_save() {
  if (maltarea.value != cmv) {
    cBtnevents(mcheckBtn, meditBtn, maltarea, 0);
  }
  if (engtarea.value != cev) {
    cBtnevents(echeckBtn, eeditBtn, engtarea, 1);
  }
}

function yesornoEvent(btn1, btn2, formData) {
  btn1.disabled = true;
  btn2.disabled = true;
  if (current){
  fetch(yonURL, {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": csrf_token,
    },
  })
  .then(response => response.json())
  .then(data => {
    
    fetchTextPairs();
    btn1.disabled = false;
    btn2.disabled = false;
  })
  .catch(error => {
    // Handle any errors
    console.error('Error fetching data:', error);
  });
}
}

if (document.getElementById("dataUploadBtn")){
duBtn = document.getElementById("dataUploadBtn");}

if (duBtn = document.getElementById("dataUploadBtn")) {
  duBtn.addEventListener("click", (e) => {
    const dataInput = document.getElementById('dataInput');
    const file = dataInput.files[0];
    const formData = new FormData();
    formData.append('file', file);
    fetch(uploadURL, {
      method: "POST",
      body: formData,
      headers: {
        // "X-CSRFToken": csrf_token,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Success:");
        if (data.status == 400) {
          appendAlert(data.message, "danger")
        }
        else if(data.status == 200){
          appendAlert(data.message, "success")
          if (!maltarea.value){
          fetchTextPairs();}
        }
      })
      .catch((error) => {
        // Handle error
        console.error("Error:", error);
      });
  });
}

btn_container1 = document.getElementById("btn-con1");
maltarea.addEventListener('mouseover', () => {
  btn_container1.style.visibility = "visible";
});

btn_container1.addEventListener('mouseover', () => {
  btn_container1.style.visibility = "visible";
});

maltarea.addEventListener('mouseout', () => {
  btn_container1.style.visibility = "hidden";
});

btn_container2 = document.getElementById("btn-con2");
engtarea.addEventListener('mouseover', () => {
  btn_container2.style.visibility = "visible";
});

btn_container2.addEventListener('mouseover', () => {
  btn_container2.style.visibility = "visible";
});

engtarea.addEventListener('mouseout', () => {
  btn_container2.style.visibility = "hidden";
});



const meditBtn = document.getElementById("maleditButton");
const mcheckBtn = document.getElementById("malcheckButton");
const eeditBtn = document.getElementById("engeditButton");
const echeckBtn = document.getElementById("engcheckButton");
const edit_container1 = document.getElementById("maltextdiv");
const edit_container2 = document.getElementById("engtextdiv");


mcheckBtn.addEventListener("click", () => {
  cBtnevents(mcheckBtn, meditBtn, maltarea, 0);
});


meditBtn.addEventListener("click", () => {
  eBtnevents(meditBtn, mcheckBtn, maltarea);
});


echeckBtn.addEventListener("click", () => {
  cBtnevents(echeckBtn, eeditBtn, engtarea, 1);
});


eeditBtn.addEventListener("click", () => {
  eBtnevents(eeditBtn, echeckBtn, engtarea);
});

var mfo = true;
edit_container1.addEventListener("mouseover", () => {
  mfo = false;
});

edit_container1.addEventListener("mouseout", () => {
  mfo = true;
});

maltarea.addEventListener("focusout", () => {
  if (mfo == true){
  maltarea.setAttribute('readonly', true);
  mcheckBtn.style.display = 'none';
  meditBtn.style.display = 'block';
  maltarea.style.cursor = 'default';}
});


var efo = true;
edit_container2.addEventListener("mouseover", () => {
  efo = false;
});

edit_container2.addEventListener("mouseout", () => {
  efo = true;
});

engtarea.addEventListener("focusout", () => {
  if (efo == true){
  engtarea.setAttribute('readonly', true);
  echeckBtn.style.display = 'none';
  eeditBtn.style.display = 'block';
  engtarea.style.cursor = 'default';}
});


function cBtnevents(btn1, btn2, tarea, eom){
  btn1.style.display = 'none';
  btn2.style.display = 'block';
  tarea.style.cursor = 'default'; 
  edit = tarea.value;
  formData = new FormData();
  formData.append("pk", current);
  formData.append("edit", edit);
  formData.append("eom", eom);
  
  fetch(editURL, {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": csrf_token,
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log("Success");
      if (tarea.id == "textarea1"){
        cmv = tarea.value;
        
      }
      else if(tarea.id = "textarea2") {
        cev = tarea.value;
        
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
  tarea.setAttribute('readonly', true);
}

function eBtnevents(btn1, btn2, tarea){
  btn1.style.display = 'none';
  btn2.style.display = 'block';
  tarea.style.cursor = 'auto';
  tarea.removeAttribute('readonly');
  tarea.focus();
}

const alertPlaceholder = document.getElementById('alertPlaceholder');
const appendAlert = (message, type) => {
  const wrapper = document.createElement('div')
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('')

  alertPlaceholder.append(wrapper)

  setTimeout(function() {
    alertPlaceholder.removeChild(wrapper)
}, 5000);
}