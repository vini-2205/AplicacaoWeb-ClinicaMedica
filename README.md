# README

## Equipe `SomosOs<br>` - CEFET-MG
- Lara Gama Santos: Front 
- Pedro Vitor Melo Bitencourt: Back 
- Vinícius Ferreira Pinheiro: Back 

## Instruções para inicialização
Além das bibliotecas usadas, deve-se instalar o 'flask'
Para executar, digite no terminal aberto no mesmo diretorio que o 'app.py': flask run. Após isso, segure Ctrl e clique no ip mostrado no terminal. Para ver as páginas, digite após o ip '/' e o nome do html

## Compressão de PDF
Ao anexar um arquivo (na página de cadastro de área) e enviar o cadastro de uma área, o sistema salva o pdf neste diretório com o nome do pdf, junto com um pdf com o mesmo nome, porém com sufixo '-comp'. Dependendo do tamanho do arquivo, pode demorar um pouco para comprimir o arquivo e salvá-lo no diretório

## Salvar PDF
Os pdfs anexados pelo página "cadastroArea" são armazenados neste diretório, já que os pdfs anexados pelo página de cadastro são armazenados na pasta "public/insercao/candidato"

## Banco de Dados
O dump do banco de dados está neste diretório: "dump-hackathon-2023080"

## Rotas
/ -> Pagina normal
/reports
/login
/register
/visualizarCandidatos
/visualizarReports
/cadastroArea
/solicitacoes
/visualizarRequisicoes
/visualizarAreas
/area/<codArea>
/portalInterno
