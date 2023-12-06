import json
from urllib.request import urlopen

def obter_localizacao():
    url = 'http://ipinfo.io/json' # Site para ter o ip da rede

    try:
        response = urlopen(url)
        data = json.load(response) # Obter a localização

        cidade = data["city"]
        estado = data["region"]
        pais = data["country"]
        
        resposta = {"cidade": cidade, "estado": estado, "pais": pais} 

        return resposta;
    except:
        return None # Não foi possível pegar a localização