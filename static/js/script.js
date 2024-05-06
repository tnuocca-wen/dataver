var maltarea = document.getElementById("textarea1");
var engtarea = document.getElementById("textarea2");

var current;

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
    engtarea.value = data.english;}
    current = data.pk
    if(data.status && data.status == 100){appendAlert(data.message, 'success')}
  })
  .catch(error => {
    // Handle any errors
    console.error('Error fetching data:', error);
  });
}

document.getElementById("btn1").addEventListener("click", (e) => {
  e.preventDefault();
  if (current){
  formData = new FormData();
  formData.append('pk', current);
  formData.append('rating', true);
  fetch(yonURL, {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": csrf_token,
    },
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
    fetchTextPairs();
  })
  .catch(error => {
    // Handle any errors
    console.error('Error fetching data:', error);
  });
}
else{
  appendAlert("Data Unavailable", 'danger');
}
});


document.getElementById("btn2").addEventListener("click", (e) => {
  e.preventDefault();
  if (current){
  formData = new FormData();
  formData.append('pk', current);
  formData.append('rating', false);
  fetch(yonURL, {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": csrf_token,
    },
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
    fetchTextPairs();
  })
  .catch(error => {
    // Handle any errors
    console.error('Error fetching data:', error);
  });
}
else{
  appendAlert("Data Unavailable", 'danger');
}
});


document.getElementById("dataUploadBtn").addEventListener("click", (e) => {
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
      console.log("Success:", data);
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


btn_container = document.querySelector(".edit-icon");
maltarea.addEventListener('mouseover', () => {
  btn_container.style.visibility = "visible";
});

btn_container.addEventListener('mouseover', () => {
  btn_container.style.visibility = "visible";
});

maltarea.addEventListener('mouseout', () => {
  btn_container.style.visibility = "hidden";
});


const editBtn = document.getElementById("editButton");
const checkBtn = document.getElementById("checkButton");

checkBtn.addEventListener("click", () => {
  checkBtn.style.display = 'none';
  editBtn.style.display = 'block';    
  edit = maltarea.value;
  console.log(edit);
  formData = new FormData();
  formData.append("pk", current);
  formData.append("edit", edit);
  console.log(formData);
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
      console.log("Success:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
  maltarea.setAttribute('readonly', true);
});


editBtn.addEventListener("click", () => {
  console.log("button triggered");
  editBtn.style.display = 'none';
  checkBtn.style.display = 'block';
  maltarea.removeAttribute('readonly');
  maltarea.focus();
});

const edit_container = document.querySelector(".box1-container > div");
var fo = true;
edit_container.addEventListener("mouseover", () => {
  fo = false;
});

edit_container.addEventListener("mouseout", () => {
  fo = true;
});

maltarea.addEventListener("focus", () => {
  if (fo == true){
  maltarea.setAttribute('readonly', true);
  checkBtn.style.display = 'none';
  editBtn.style.display = 'block';}
});




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