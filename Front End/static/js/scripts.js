function toggleButtons(element) {
    // Get the buttons for the clicked element
    var buttons = element.nextElementSibling;

    // If the buttons are currently displayed, hide them
    if (buttons.style.display === "block") {
        buttons.style.display = "none";
    } 
    // If the buttons are currently hidden, first hide all other buttons, then display these ones
    else {
        // First, hide all buttons
        var allButtons = document.querySelectorAll('.buttons');
        for (let i = 0; i < allButtons.length; i++) {
            allButtons[i].style.display = "none";
        }

        // Then, display the buttons for the clicked element
        buttons.style.display = "block";
    }
}