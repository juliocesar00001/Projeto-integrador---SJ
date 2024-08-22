document.addEventListener('DOMContentLoaded', function() {
    let btn = document.querySelector('.fa-eye');

    if (btn) { // Verifica se o elemento existe antes de adicionar o event listener
        btn.addEventListener('click', () => {
            let inputSenha = document.querySelector('#senha');
            
            if (inputSenha.getAttribute('type') === 'password') {
                inputSenha.setAttribute('type', 'text');
            } else {
                inputSenha.setAttribute('type', 'password');
            }
        });
    }
    
    // Tornar a função entrar global para ser acessível pelo atributo onclick
    window.entrar = function() {
        let usuario = document.querySelector('#usuario').value;
        let userLabel = document.querySelector('#userLabel');
        
        let senha = document.querySelector('#senha').value;
        let senhaLabel = document.querySelector('#senhaLabel');
        
        let msgError = document.querySelector('#msgError');
        let listaUser = JSON.parse(localStorage.getItem('listaUser')) || [];
        
        let userValid = {
            nome: null,
            user: null,
            senha: null,
        };
        
        listaUser.forEach((item) => {
            if (usuario === item.userCad && senha === item.senhaCad) {
                userValid = {
                    nome: item.nomeCad,
                    user: item.userCad,
                    senha: item.senhaCad
                };
            }
        });
        
        if (usuario === userValid.user && senha === userValid.senha) {
            // Remove redirecionamento e manipulação de localStorage
        } else {
            userLabel.style.color = 'red';
            userLabel.innerHTML = 'CPF';
            usuario.style.borderColor = 'red';
            senhaLabel.style.color = 'red';
            senhaLabel.innerHTML = 'Senha';
            senha.style.borderColor = 'red';
            msgError.style.display = 'block';
            msgError.innerHTML = 'Usuário ou senha incorretos';
            usuario.focus();
        }
    };
});
