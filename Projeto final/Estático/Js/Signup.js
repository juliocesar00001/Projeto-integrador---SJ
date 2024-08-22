document.addEventListener('DOMContentLoaded', () => {
  const nome = document.querySelector('#nome');
  const labelNome = document.querySelector('#labelNome');
  let validNome = false;

  const cpf = document.querySelector('#usuario'); // Alterado para #usuario pois parece ser o campo de CPF
  const labelCPF = document.querySelector('#labelUsuario'); // Alterado para #labelUsuario
  let validCPF = false;

  const telefone = document.querySelector('#telefone');
  const labelTelefone = document.querySelector('#labelTelefone');
  let validTelefone = false;

  const senha = document.querySelector('#senha');
  const labelSenha = document.querySelector('#labelSenha');
  let validSenha = false;

  const confirmSenha = document.querySelector('#confirmSenha');
  const labelConfirmSenha = document.querySelector('#labelConfirmSenha');
  let validConfirmSenha = false;

  const msgError = document.querySelector('#msgError');
  const msgSuccess = document.querySelector('#msgSuccess');

  nome.addEventListener('keyup', () => {
      if (nome.value.length <= 2) {
          labelNome.style.color = 'red';
          labelNome.innerHTML = 'Nome *Insira no mínimo 3 caracteres';
          nome.style.borderColor = 'red';
          validNome = false;
      } else {
          labelNome.style.color = 'green';
          labelNome.innerHTML = 'Nome';
          nome.style.borderColor = 'green';
          validNome = true;
      }
  });

  cpf.addEventListener('keyup', () => {
      cpf.value = cpf.value.replace(/\D/g, '');
      if (cpf.value.length < 11) {
          labelCPF.style.color = 'red';
          labelCPF.innerHTML = 'CPF *Insira no mínimo 11 caracteres';
          cpf.style.borderColor = 'red';
          validCPF = false;
      } else {
          labelCPF.style.color = 'green';
          labelCPF.innerHTML = 'CPF';
          cpf.style.borderColor = 'green';
          validCPF = true;
      }
  });

  telefone.addEventListener('input', () => {
      telefone.value = telefone.value.replace(/\D/g, '');
      if (telefone.value.length < 11) {
          labelTelefone.style.color = 'red';
          labelTelefone.innerHTML = 'Telefone *Insira DDD + Telefone';
          telefone.style.borderColor = 'red';
          validTelefone = false;
      } else {
          labelTelefone.style.color = 'green';
          labelTelefone.innerHTML = 'Telefone';
          telefone.style.borderColor = 'green';
          validTelefone = true;
      }
  });

  senha.addEventListener('keyup', () => {
      if (senha.value.length <= 5) {
          labelSenha.style.color = 'red';
          labelSenha.innerHTML = 'Senha *Insira no mínimo 6 caracteres';
          senha.style.borderColor = 'red';
          validSenha = false;
      } else {
          labelSenha.style.color = 'green';
          labelSenha.innerHTML = 'Senha';
          senha.style.borderColor = 'green';
          validSenha = true;
      }
  });

  confirmSenha.addEventListener('keyup', () => {
      if (senha.value !== confirmSenha.value) {
          labelConfirmSenha.style.color = 'red';
          labelConfirmSenha.innerHTML = 'Confirmar Senha *As senhas não conferem';
          confirmSenha.style.borderColor = 'red';
          validConfirmSenha = false;
      } else {
          labelConfirmSenha.style.color = 'green';
          labelConfirmSenha.innerHTML = 'Confirmar Senha';
          confirmSenha.style.borderColor = 'green';
          validConfirmSenha = true;
      }
  });

  function cadastrar() {
      if (validNome && validCPF && validTelefone && validSenha && validConfirmSenha) {
          msgSuccess.style.display = 'block';
          msgSuccess.innerHTML = '<strong>Cadastrando usuário...</strong>';
          msgError.style.display = 'none';
          msgError.innerHTML = '';

          // Envia o formulário ao backend
          setTimeout(() => {
              document.getElementById('formCadastro').submit();
          }, 1000);

      } else {
          msgError.style.display = 'block';
          msgError.innerHTML = '<strong>Preencha todos os campos corretamente antes de cadastrar</strong>';
          msgSuccess.innerHTML = '';
          msgSuccess.style.display = 'none';
      }
  }

  document.querySelector('#verSenha').addEventListener('click', () => {
      senha.type = senha.type === 'password' ? 'text' : 'password';
  });

  document.querySelector('#verConfirmSenha').addEventListener('click', () => {
      confirmSenha.type = confirmSenha.type === 'password' ? 'text' : 'password';
  });

  document.querySelector('button[type="submit"]').addEventListener('click', (event) => {
      event.preventDefault();
      cadastrar();
  });
});
