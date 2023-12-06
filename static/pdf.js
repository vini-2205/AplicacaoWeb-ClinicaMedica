document.getElementById('porta').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append('cpf', document.getElementById('cpf').value);
    formData.append('rg', document.getElementById('rg').files[0]);
    formData.append('cpf_file', document.getElementById('cpf_file').files[0]);
    formData.append('curriculo', document.getElementById('curriculo').files[0]);
    formData.append('cnh', document.getElementById('cnh').files[0]);
    formData.append('certificado_reservista', document.getElementById('certificado_reservista').files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Erro:', error);
    });
});