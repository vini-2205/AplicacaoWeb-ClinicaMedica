function buscarCEP(event) {
    event.preventDefault();
    var cepDigitado = document.getElementsByName('cep')[0];  // Obtenha o valor do campo, não o elemento

    if (cepDigitado){
        cepDigitado = cepDigitado.value;

        // Realiza uma requisição AJAX para a rota que busca o CEP usando Axios
        axios.post('/api/busca_cep', { cep: cepDigitado })
            .then(function (response) {
                var data = response.data;

                if (data.success) {
                    if (data.success) {
                    // Preenche automaticamente os campos de bairro, logradouro, cidade e estado
                    var bairroInput = document.getElementsByName('bairro')[0];
                    var logradouroInput = document.getElementsByName('logradouro')[0];
                    var cidadeInput = document.getElementsByName('cidade')[0];
                    var estadoInput = document.getElementsByName('estado')[0];

                    if (bairroInput) bairroInput.value = data.bairro;
                    if (logradouroInput) logradouroInput.value = data.logradouro;
                    if (cidadeInput) cidadeInput.value = data.cidade;
                    if (estadoInput) estadoInput.value = data.estado;
                } else {
                    alert('CEP não encontrado');
                }
            }
            })
            .catch(function (error) {
                console.error('Erro na requisição:', error);
            });
    }
    else {
        console.error('Elemento com o nome "cep" não encontrado no DOM.');
    }
}