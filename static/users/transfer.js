// Get the modal
console.log("HIiii");
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
btn.addEventListener("click", (e) => {
  let amt = document.getElementById('amt').value;
  if (amt <= 0) {
    alert("Invalid entry in Amount field!");
  }
  else {
    modal.style.display = "block";
    let elem = document.getElementsByClassName("hidden");
    elem[1].value = document.getElementById('Acc').value;
    elem[3].value = document.getElementById('amt').value;
  }

})



// When the user clicks on <span> (x), close the modal
span.onclick = function () {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

