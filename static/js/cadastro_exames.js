(() => {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        // Auxiliar para preencher data de hoje para todas as linhas
        const btnDataHoje = document.getElementById('btn-data-hoje');
        if (btnDataHoje) {
            btnDataHoje.addEventListener('click', function() {
                const today = new Date();
                const yyyy = today.getFullYear();
                const mm = String(today.getMonth() + 1).padStart(2, '0');
                const dd = String(today.getDate()).padStart(2, '0');
                const todayStr = `${yyyy}-${mm}-${dd}`;
                
                const dates = document.querySelectorAll('.exam-date');
                dates.forEach(function(d) {
                    d.value = todayStr;
                });
            });
        }

        const form = document.getElementById('form-cadastro-exames');
        const exams = ['gds', 'moca', 'spdds', 'updrs_i', 'updrs_ii', 'updrs_iii', 'updrs_iv', 'hoehn_yahr', 'beck'];

        function showValidationAlert(message) {
            const alertHtml = `
                <div class="alert alert-danger alert-dismissible fade show border-0 shadow-sm mb-4" role="alert">
                    <i class="bi bi-exclamation-triangle-fill me-2"></i> ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `;
            const container = document.querySelector('.content-body');
            if (container) {
                // Remover alerta anterior se houver
                const oldAlert = container.querySelector('.alert-danger');
                if (oldAlert) {
                    oldAlert.remove();
                }
                container.insertAdjacentHTML('afterbegin', alertHtml);
                // Scroll to top to see the alert
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        }

        if (form) {
            form.addEventListener('submit', function(event) {
                let isValid = true;
                let hasAtLeastOne = false;
                
                // Limpar estados invalidos anteriores
                document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));

                exams.forEach(function(exam) {
                    const dateInput = document.getElementById(exam + '_date');
                    const scoreInput = document.getElementById(exam + '_score');

                    if (dateInput && scoreInput) {
                        const hasDate = dateInput.value !== '';
                        const hasScore = scoreInput.value !== '';

                        // Se um está preenchido e o outro vazio, aciona a regra
                        if (hasDate && !hasScore) {
                            isValid = false;
                            scoreInput.classList.add('is-invalid');
                        } else if (!hasDate && hasScore) {
                            isValid = false;
                            dateInput.classList.add('is-invalid');
                        }

                        if (hasDate && hasScore) {
                            hasAtLeastOne = true;
                        }
                    }
                });

                // Caso a validação de preenchimento mútuo falhe
                if (!isValid) {
                    event.preventDefault();
                    showValidationAlert('Erro de Validação: Para salvar um exame, você deve preencher tanto a Data do Exame quanto a Nota Final.');
                    return;
                }

                // Caso nenhum exame esteja preenchido
                if (!hasAtLeastOne) {
                    event.preventDefault();
                    showValidationAlert('Atenção: Nenhum exame foi preenchido. Lance pelo menos uma avaliação para poder salvar.');
                    return;
                }
            });
        }
    });
})();
