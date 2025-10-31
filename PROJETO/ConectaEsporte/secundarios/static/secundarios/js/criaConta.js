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
        e.preventDefault();

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
            return;
        }

        if (!password) { showMessage('Preencha a senha.'); passwordInput.focus(); return; }
        if (password !== confirm) { showMessage('As senhas não coincidem.'); confirmInput.focus(); return; }

        if (geoCheckbox && geoCheckbox.checked && (!latInput.value || !lngInput.value)) {
            showMessage('Aguardando localização ou permissões. Desmarque a opção ou tente novamente.');
            return;
        }

        // MOCK: salva usuário no localStorage (NÃO USE em produção para senhas reais)
        const user = {
            username,
            email,
            password, // apenas mock — em produção sempre hash de senha no servidor
            latitude: latInput.value || null,
            longitude: lngInput.value || null,
            createdAt: new Date().toISOString()
        };

        const usersKey = 'mock_users';
        const existing = JSON.parse(localStorage.getItem(usersKey) || '[]');

        // opcional: impedir duplicatas por email/username no mock
        const duplicate = existing.find(u => u.email === email || u.username === username);
        if (duplicate) {
            showMessage('Já existe uma conta com esse e-mail ou nome de usuário.');
            return;
        }

        existing.push(user);
        localStorage.setItem(usersKey, JSON.stringify(existing));

        // sucesso: mostra mensagem e redireciona para a página de login
        showMessage('Conta criada (mock) com sucesso. Redirecionando...', false);
        form.reset();
        clearCoords();

        // espera 1s para o usuário ver a mensagem, depois redireciona
        setTimeout(function () {
            // caminho relativo a partir de HTML/mockup-criacao-conta/src/criaConta.html para HTML/login.html
            window.location.href = '../../login.html';
        }, 1000);
    });

    if (confirmInput) {
        confirmInput.addEventListener('input', function () {
            if (errorEl.textContent && passwordInput.value === confirmInput.value) showMessage('', false);
        });
    }
});