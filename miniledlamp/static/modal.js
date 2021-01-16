function initModal(modalId, modalOpenButtonId, modalCloseClass) {
  // Get the modal
  let modal = document.getElementById(modalId);

  // Get the button that opens the modal
  let btn = document.getElementById(modalOpenButtonId);

  // Get the <span> element that closes the modal
  let span = document.getElementsByClassName(modalCloseClass)[0];

  // When the user clicks on the button, open the modal
  btn.onclick = function() {
    modal.style.display = "block";
  }

  // When the user clicks on <span> (x), close the modal
  span.onclick = function() {
    modal.style.display = "none";
  }

  // When the user clicks anywhere outside of the modal, close it
  window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
  }
}
