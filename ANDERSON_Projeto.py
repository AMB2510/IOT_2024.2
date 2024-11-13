#Bibliotecas utilizadas
from sense_hat import SenseHat
import time
import thingspeak

# Item 2 -  Crie um código onde os valores de medição sejam apresentados na placa 
sense = SenseHat()
sense.clear()

# Definição das cores
BLUE   = (0, 0, 255)
GREEN  = (0, 255, 0)
RED    = (255, 0, 0)
YELLOW = (255, 255, 0)

# Credenciais do canal ThingSpeak
IOT_ID  = "2731766"
IOT_KEY = "IM1WR9S1MW5YM8BZ"
IOT_CHN = thingspeak.Channel(IOT_ID, IOT_KEY)

# Função para obter os dados do SenseHAT
def obter_dados_sensores():
    temperatura = sense.get_temperature()
    umidade     = sense.get_humidity()
    pressao     = sense.get_pressure()

    # Simulação do valor da qualidade do ar
    qualidade_ar = 38

    return temperatura, umidade, pressao, qualidade_ar

# Função para publicar dados no ThingSpeak
def publicar_thingspeak(temperatura, umidade, pressao, qualidade_ar):
    payload = {'field1': temperatura, 'field2': umidade, 'field3': pressao, 'field4': qualidade_ar}
    
        if (IOT_CHN.update(payload)):
            print("Dados enviados para ThingSpeak com sucesso!")
        else:
            print("Erro ao enviar dados para o ThingSpeak!")
	print("-" * 65)
	time.sleep(1)


# Função para exibir a mensagem no SenseHat
def exibir_mensagem(temperatura, umidade, pressao, qualidade_ar):
    # Item 3 - Apresente o nome do seu projeto na cor azul no display do SenseHat
    sense.show_message("ANDERSON_2161392313034", text_colour=BLUE)
    time.sleep(1)
    

    # Item 4 - Informação na matriz de leds com as condições do tempo
    # Alerta das condições climáticas
    if (20 <= temperatura <= 30 and 40 <= umidade <= 70 and 1014 <= pressao <= 1025 and qualidade_ar <= 40:
        # Condição normal
        cor_status = GREEN
        status = "NORMAL"

    elif (12 <= temperatura < 20 or 30 < temperatura <= 36 or 21 <= umidade < 40 or 980 <= pressao < 1014 or 1025 < pressao <= 1030 or 40 < qualidade_ar <= 80):
        # Alerta de Atenção
        cor_status = YELLOW
        status = "ATENCAO"

    else:
        # Alerta de Perigo
        cor_status = RED
        status = "PERIGO"
    
    # Exibe as condições
    sense.show_message(status, text_colour = cor_status)
    sense.show_message(f"\nT: {temperatura:.1f}°C\nU: {umidade:.1f}%\nP: {pressao:.1f}hPa\nQA: {qualidade_ar}", text_colour = cor_status)
    
# Loop principal
while True:
    temperatura, umidade, pressao, qualidade_ar = obter_dados_sensores()
    print(f"Temperatura: {temperatura:.1f}°C, Umidade: {umidade:.1f}%, Pressao: {pressao:.1f} hPa, Qualidade do Ar: {qualidade_ar}")

    # Publicação dos dados no ThingSpeak
    publicar_thingspeak(temperatura, umidade, pressao, qualidade_ar)

    # Exibição das condições no SenseHat
    exibir_mensagem(temperatura, umidade, pressao, qualidade_ar)
    time.sleep(3)
