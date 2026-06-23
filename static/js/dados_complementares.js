(() => {
    'use strict';

    document.addEventListener("DOMContentLoaded", function() {
        const phoneInput = document.getElementById("telefone");
        
        function formatPhone(value) {
            let digits = value.replace(/\D/g, "");
            if (digits.length > 11) {
                digits = digits.substring(0, 11);
            }
            let formatted = digits;
            if (digits.length > 2) {
                formatted = digits.substring(0, 2) + "-" + digits.substring(2);
            }
            return formatted;
        }

        if (phoneInput) {
            phoneInput.addEventListener("input", function(e) {
                e.target.value = formatPhone(e.target.value);
            });
        }
    });
})();
