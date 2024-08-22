document.addEventListener("DOMContentLoaded", function() {
    fetch("/session-user")
        .then(response => response.json())
        .then(data => {
            if (data.logged_in) {
                document.getElementById("logado").innerText = `Olá! ${data.fun_name}.`;
            } else {
                alert("Você precisa estar logado para acessar essa página");
                // Adiciona um atraso de 3 segundos (3000 milissegundos) antes de redirecionar
                setTimeout(function() {
                    window.location.href = loginUrl;
                }, 3000);
            }
        });
});

function sair() {
    fetch("/logout", { method: "POST" })
        .then(() => {
            window.location.href = loginUrl;
        });
}
