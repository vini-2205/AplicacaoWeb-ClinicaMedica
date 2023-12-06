function AdicionaDependente() {
    var novosInputs = document.createElement('div');
	novosInputs.innerHTML = '<label for="nome-dep">Nome Completo do Dependente*:</label><br>' +
                            '<input type="text" name="nome-dep" placeholder="Digite o nome completo" ><br>'+
                            '<p><label for="cpf-dep">Número do CPF*:</label>'+
                            '<input type="text" name="cpf-dep" pattern="[0-9]{11}"  inputmode="numeric" placeholder="Ex: 99999999999" ></p>'+
                            '<p><label for="sexo-dep">Sexo*:</label>'+
                            '<select name="sexo-dep" placeholder="Escolher..." ><option value="" disabled selected>Escolher...</option><option value="masculino">Masculino</option><option value="feminino">Feminino</option><option value="outro">Outro</option></select></p>  '+
                            '<p><label for="data-nascimento-dep">Data de Nascimento*:</label>'+
                            '<input type="date" name="data-nascimento-dep" ></p>'+
                            '<label for="parentesco-dep">Grau de parentesco*:</label><br>'+
                            '<input type="text" name="parentesco-dep" placeholder="Digite o parentesco com o dependente" ><br><br>'+
                            '<hr width="100%" noshade>';
	document.getElementById("novo-dep").appendChild(novosInputs);
}

function InformacoesConhecido() {
    var novosInputs = document.createElement('div');
	novosInputs.innerHTML = '<br><label for="nome-con">Nome Completo do Parente ou Amigo*:</label><br>' +
                            '<input type="text" name="nome-con" placeholder="Digite o nome completo" ><br>'+
                            '<p><label for="funcao-con">Função*:</label>'+
                            '<input type="text" name="funcao-con" placeholder="Digite o cargo" ></p>'+
                            '<label for="cidade-con">Cidade*:</label><br>'+
                            '<input type="text" name="cidade-con" placeholder="Digite a cidade"></p>'+
                            '<hr width="100%" noshade>';
	document.getElementById("campos").appendChild(novosInputs);
}
