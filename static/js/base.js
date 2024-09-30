document.addEventListener("DOMContentLoaded", function() {
    // Select the messages div
    const messagesDiv = document.getElementById('messages');
  
    if (messagesDiv) {
      // Set a timeout to start fading after 3 seconds (3000 ms)
      setTimeout(function() {
        // Apply a CSS transition to fade out the messages
        messagesDiv.style.transition = "opacity 1s ease";
        messagesDiv.style.opacity = "0";
  
        // After the transition, remove the element from the DOM
        setTimeout(function() {
          messagesDiv.remove();
        }, 2000); // Wait for the fade out transition to complete
      }, 3000); // 3 seconds before fade out starts
    }
  });
  