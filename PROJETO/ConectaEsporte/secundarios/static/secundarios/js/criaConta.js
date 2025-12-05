document.addEventListener('DOMContentLoaded', function () {
    const geoCheckbox = document.getElementById('geo-consent');
    const latInput = document.getElementById('latitude');
    const lngInput = document.getElementById('longitude');
    const errorEl = document.getElementById('error-message');
    const form = document.getElementById('signup-form');

    const usernameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmInput = document.getElementById('confirm-password');

    function showMessage(msg, isError = true) {
        errorEl.textContent = msg || '';
        errorEl.style.color = isError ? 'red' : 'green';
    }

    function clearCoords() {
        if (latInput) latInput.value = '';
        if (lngInput) lngInput.value = '';
    }

    function requestGeolocation() {
        showMessage('');
        if (!navigator.geolocation) {
            showMessage('Geolocalização não disponível neste navegador.');
            if (geoCheckbox) geoCheckbox.checked = false;
            clearCoords();
            blockSubmit();
            return;
        }

        navigator.geolocation.getCurrentPosition(
            (pos) => {
                if (latInput) latInput.value = pos.coords.latitude;
                if (lngInput) lngInput.value = pos.coords.longitude;
            },
            (err) => {
                if (geoCheckbox) geoCheckbox.checked = false;
                clearCoords();
                if (err.code === err.PERMISSION_DENIED) {
                    showMessage('Permissão de localização negada.');
                } else {
                    showMessage('Erro ao obter localização: ' + (err.message || ''));
                }
            },
            { enableHighAccuracy: true, timeout: 10000 }
        );
    }

    if (geoCheckbox) {
        geoCheckbox.addEventListener('change', function () {
            if (this.checked) requestGeolocation();
            else {
                clearCoords();
                showMessage('');
            }
        });
    }

    form.addEventListener('submit', function (e) {

        function blockSubmit() {
            e.preventDefault();
        }

        // validações básicas
        const username = (usernameInput && usernameInput.value || '').trim();
        const email = (emailInput && emailInput.value || '').trim();
        const password = (passwordInput && passwordInput.value || '');
        const confirm = (confirmInput && confirmInput.value || '');

        if (!username) { showMessage('Preencha o nome de usuário.'); usernameInput.focus(); return; }
        if (!email) { showMessage('Preencha o e-mail.'); emailInput.focus(); return; }

        // validação de formato de e-mail (simples)
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            showMessage('E-mail inválido. Insira um endereço de e-mail válido.'); 
            emailInput.focus();
            blockSubmit();
            return;
        }

        if (!password) { showMessage('Preencha a senha.'); passwordInput.focus(); return; }
        if (password !== confirm) { showMessage('As senhas não coincidem.'); confirmInput.focus(); return; }

        if (geoCheckbox && geoCheckbox.checked && (!latInput.value || !lngInput.value)) {
            showMessage('Aguardando localização ou permissões. Desmarque a opção ou tente novamente.');
            return;
        }

    if (confirmInput) {
        confirmInput.addEventListener('input', function () {
            if (errorEl.textContent && passwordInput.value === confirmInput.value) showMessage('', false);
        });
    }
});});