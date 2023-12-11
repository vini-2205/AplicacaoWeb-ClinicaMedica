// caminho para onde as imagens estão hospedadas
const servidorDasImagens = '../static/imgs/',
  // array com o nome das 5 imagens da galeria
  nomesDasImagens = [
    'galeria1.jpg',
    'galeria2.jpg',
    'galeria3.jpg',
    'galeria4.jpg'
  ];

let indiceDaFotoAtual = 0;

function mudarImg(sentido){
  indiceDaFotoAtual += sentido;
  if(indiceDaFotoAtual === -1){ //imagens em carrossel
    indiceDaFotoAtual = 4
  } else if(indiceDaFotoAtual === 5){
    indiceDaFotoAtual = 0;
  }
  let img = document.querySelector('#slide');
  img.src = servidorDasImagens + nomesDasImagens[indiceDaFotoAtual]; //altera imagem
}

let btnProximo = document.querySelector('#proximo');
let btnAnterior = document.querySelector('#anterior');

btnProximo.addEventListener('click', function(){
  mudarImg(1)});
btnAnterior.addEventListener('click', function(){
  mudarImg(-1)});