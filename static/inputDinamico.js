function exibeCampos() {
    var divCampos = document.getElementById("campos");
    divCampos.classList.toggle("oculto");
  }

document.getElementById("toggleButton").addEventListener("change", exibeCampos);

