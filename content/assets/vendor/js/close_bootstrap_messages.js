
// After 3 seconds, hide the success message
setTimeout(function() {
    var successMessages = document.getElementsByClassName('alert');
  
    for (var i = 0; i < successMessages.length; i++) {
      successMessages[i].style.display = 'none';
    }
  }, 3000);