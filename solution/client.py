import requests

url = "http://localhost:8000/"


#POST /guees
nueva_partida = {
    "player" : "Julian"
}
response = requests.post(url=url+"guess", json=nueva_partida)
print(response.text)


# GET /guess
response = requests.get(url=url + "guess")
print(response.text)

#PUT actualizar los intentos de una partida
#agregando_attemp = {
#    "attempt" : "25"
#}
#
#response = requests.request(method="PUT", url=url+"guess/1", json=agregando_attemp)
#print(response.text)



##GET /guess/1
#response = requests.request(method="GET", url=url+"guees/1")
#print(response.text)
#
#GET /guess/?player=Julian
#response = requests.get(url=url+"guess/?player=Julian")
#print(response.text)


#DELETE
response = requests.delete( url=url+"guess/1")
print(response.text)
# GET /guess
response = requests.get(url=url + "guess")
print(response.text)
