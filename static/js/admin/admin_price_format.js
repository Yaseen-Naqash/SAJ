// admin_price_format.js





// IT ADDS COMMA FOR ANY INPUT CHARFILED WITH NAME price

// test
document.addEventListener('DOMContentLoaded', () => {
    console.log('JavaScript start Loading...');
    
});




document.addEventListener('DOMContentLoaded', function() {
    // Select input fields with "comma-add" class for comma-separated formatting
    var textInput = document.querySelector('.comma-add'); 

    function formatInput(event) {
        var input = event.target; 
        var value = input.value;
        
        var removeChar = value.replace(/[^0-9.]/g, '');
        
        var parts = removeChar.split('.');
        if (parts.length > 2) {
            removeChar = parts[0] + '.' + parts.slice(1).join('');
        }
        
        parts = removeChar.split('.');
        var integerPart = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        var decimalPart = parts[1] ? '.' + parts[1] : '';
        
        input.value = integerPart + decimalPart;
    }

    if (textInput) {
        textInput.addEventListener('input', formatInput);
    }

})
