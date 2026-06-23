(() => {
    'use strict';

    document.addEventListener("DOMContentLoaded", function() {
        // Validação dinâmica de Café
        const usoCafe = document.getElementById("uso_regular_cafe");
        const divCafe = document.getElementById("div_frequencia_cafe");
        const inputCafe = document.getElementById("frequencia_por_dia");

        function toggleCafe() {
            if (usoCafe && usoCafe.checked) {
                divCafe.classList.remove("d-none");
                inputCafe.setAttribute("required", "required");
            } else if (usoCafe) {
                divCafe.classList.add("d-none");
                inputCafe.removeAttribute("required");
                inputCafe.value = "";
            }
        }
        if (usoCafe) {
            usoCafe.addEventListener("change", toggleCafe);
            toggleCafe();
        }

        // Validação dinâmica de Abuso de Substância
        const abusoSubstancia = document.getElementById("abuso_substancia");
        const divSubstancia = document.getElementById("div_qual_substancia");
        const inputSubstancia = document.getElementById("qual_substancia");

        function toggleSubstancia() {
            if (abusoSubstancia && abusoSubstancia.checked) {
                divSubstancia.classList.remove("d-none");
                inputSubstancia.setAttribute("required", "required");
            } else if (abusoSubstancia) {
                divSubstancia.classList.add("d-none");
                inputSubstancia.removeAttribute("required");
                inputSubstancia.value = "";
            }
        }
        if (abusoSubstancia) {
            abusoSubstancia.addEventListener("change", toggleSubstancia);
            toggleSubstancia();
        }

        // Validação dinâmica de Familiar com Parkinson
        const familiarDp = document.getElementById("familiar_com_dp");
        const divFamiliarDp = document.getElementById("div_qual_familiar_dp");
        const inputFamiliarDp = document.getElementById("qual_familiar_dp");

        function toggleFamiliarDp() {
            if (familiarDp && familiarDp.value === "sim") {
                divFamiliarDp.classList.remove("d-none");
                inputFamiliarDp.setAttribute("required", "required");
            } else if (familiarDp) {
                divFamiliarDp.classList.add("d-none");
                inputFamiliarDp.removeAttribute("required");
                inputFamiliarDp.value = "";
            }
        }
        if (familiarDp) {
            familiarDp.addEventListener("change", toggleFamiliarDp);
            toggleFamiliarDp();
        }

        // Validação dinâmica de Familiar com Tremor
        const familiarTremor = document.getElementById("familiar_com_tremor");
        const divFamiliarTremor = document.getElementById("div_qual_familiar_tremor");
        const inputFamiliarTremor = document.getElementById("qual_familiar_tremor");

        function toggleFamiliarTremor() {
            if (familiarTremor && familiarTremor.value === "sim") {
                divFamiliarTremor.classList.remove("d-none");
                inputFamiliarTremor.setAttribute("required", "required");
            } else if (familiarTremor) {
                divFamiliarTremor.classList.add("d-none");
                inputFamiliarTremor.removeAttribute("required");
                inputFamiliarTremor.value = "";
            }
        }
        if (familiarTremor) {
            familiarTremor.addEventListener("change", toggleFamiliarTremor);
            toggleFamiliarTremor();
        }
    });
})();
