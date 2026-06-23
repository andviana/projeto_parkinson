(() => {
    'use strict';

    document.addEventListener('DOMContentLoaded', () => {
        const loadingOverlay = document.getElementById('global-loading-overlay');

        // Interceptar a submissão de todos os formulários da aplicação
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', (event) => {
                // Usamos setTimeout para rodar após todas as validações síncronas/customizadas do navegador
                setTimeout(() => {
                    // Se o envio foi cancelado por validação ou preventDefault, não ativa o loading
                    if (event.defaultPrevented) {
                        return;
                    }

                    // Impede envios múltiplos se o form já estiver em estado submetido
                    if (form.dataset.submitted === 'true') {
                        event.preventDefault();
                        return;
                    }

                    form.dataset.submitted = 'true';

                    // Desabilita botões de submit para evitar novos cliques
                    form.querySelectorAll('button[type="submit"], input[type="submit"]').forEach(btn => {
                        btn.disabled = true;
                    });

                    // Exibe o overlay de loading global
                    if (loadingOverlay) {
                        loadingOverlay.style.display = 'flex';
                    }
                }, 0);
            });
        });

        // Se o usuário navegar de volta usando o histórico do navegador (bfcache),
        // o evento pageshow é disparado. Precisamos ocultar o loading e re-habilitar botões.
        window.addEventListener('pageshow', (event) => {
            if (loadingOverlay) {
                loadingOverlay.style.display = 'none';
            }
            
            document.querySelectorAll('form').forEach(form => {
                form.removeAttribute('data-submitted');
                form.querySelectorAll('button[type="submit"], input[type="submit"]').forEach(btn => {
                    btn.disabled = false;
                });
            });
        });

        // Intercepta formulários que exigem confirmação (ex: deletar usuário/paciente)
        document.querySelectorAll('form.js-confirm-submit').forEach(form => {
            form.addEventListener('submit', (event) => {
                const message = form.getAttribute('data-confirm-message') || 'Confirma a operação?';
                if (!confirm(message)) {
                    event.preventDefault();
                    // Oculta o loading se o outro listener já o ativou
                    if (loadingOverlay) {
                        loadingOverlay.style.display = 'none';
                    }
                    // Reabilita os botões de envio
                    form.removeAttribute('data-submitted');
                    form.querySelectorAll('button[type="submit"], input[type="submit"]').forEach(btn => {
                        btn.disabled = false;
                    });
                }
            });
        });
    });
})();

