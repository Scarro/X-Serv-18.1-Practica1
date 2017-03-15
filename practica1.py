#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ---------------------------------
# Sergio Carro Albarrán
# SAT GITT
# ---------------------------------

import webapp
from urllib.request import urlopen
from urllib.parse import unquote

class acortadoraUrls(webapp.webApp):
    # Heredo de la clase webApp
    urls = []

    def dameHTMLformulario(self):
        formulario = "<form method='POST'>Introduce URL: "
        formulario += "<input type='text' name='url'"
        formulario += "value='' placeholder='Introduce direccion "
        formulario += "aqui'/><button type='submit'>Enviar</button"
        formulario += "></form>"
        return formulario

    def dameHTMLurls(self):
        html = ""
        if len(self.urls) > 0:
            html += "<ul><h3>Lista de urls acortadas:</h3>"
            posicion = 0
            for i in self.urls:
                posicion = posicion+1
                html += "<li><a href='" + i + "'>" + i + "</a>"
                html += " ==> Acortada: "
                html += "<a href='" + i + "'>http://localhost:1234/" + str(posicion) + "</a></li></br>"
            html += "</ul>"
        return html

    def dameHTMLprincipal(self,valida):
        HTTPcode = "200 OK"
        html = "<html><body><h1>Acortadora de URLS</h1>"
        html += self.dameHTMLformulario()
        if valida == 0:
            html += "<h3>No se ha introducido una URL valida, vuelve a intentarlo</h3>"
        html += self.dameHTMLurls()
        html += "</body></html>"
        return (HTTPcode, html)


    def compruebaUrl(self, url):
        try:
            urlopen(url)
            return True
        except:
            return False

    def existeUrl(self, url):
        if url.startswith("http"):
            url = unquote(unquote(url))
            if self.compruebaUrl(url):
                return (True, url)
        elif url != '':
            url1 = "https://" + url
            if not self.compruebaUrl(url1):
                url1 = "http://" + url
                if self.compruebaUrl(url1):
                    return (True, url1)
            else:
                return (True, url1)
        return (False, url)

    # redefino su parse y su process
    def parse(self, request):
        metodo = request.split()[0]
        recurso = request.split()[1]
        if recurso != '/favicon.ico':
            print("\n**********************************************")
            print("Peticion recibida:")
            print("------------------")
            print(request)
            print("**********************************************")
        cuerpo = ""
        if metodo == "POST":
            cuerpo = request.split("\r\n\r\n")[1].split("=")[1]
        return (metodo, recurso, cuerpo)

    def process(self, parsedRequest):
        metodo, recurso, cuerpo = parsedRequest
        urlvalida = 1
        HTTPCode = ""
        html = ""
        if metodo == "GET":
            if recurso != "/" and recurso != "/favicon.ico":
                redirect = 1
                try:
                    recurso = int(recurso[1:])
                    urls = len(self.urls)
                    if urls > 0 and recurso > 0 and recurso <= urls:
                        HTTPCode = "307 Temporaly Redirect\n"
                        HTTPCode += "Location:" + self.urls[recurso-1]
                        html = ""
                    else:
                        redirect = 0
                except ValueError:
                    recurso = recurso[1:]
                    redirect = 0
                finally:
                    if redirect == 0:
                        HTTPCode = "404 Not Found"
                        html = '<html><body>'
                        html += "<h2>Recurso '" + str(recurso)
                        html += "' no encontrado</h2>"
                        html += "<a href='http://" + self.hostname + ":" + str(self.port) + "'>"
                        html += "Volver</a>"
                        html += "</body></html>"
                    return (HTTPCode, html)
            (HTTPCode, html) = self.dameHTMLprincipal(urlvalida)

        if metodo == "POST":
            (existe,url) = self.existeUrl(cuerpo);
            if existe:
                cuerpo = url
                if cuerpo not in self.urls:
                    self.urls.append(cuerpo)
            else:
                urlvalida = 0
            (HTTPCode, html) = self.dameHTMLprincipal(urlvalida)
        return (HTTPCode, html)

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        webapp.webApp.__init__(self, hostname, port)

if __name__ == "__main__":
    try:
        test = acortadoraUrls("localhost", 1234)
    except KeyboardInterrupt:
        print("Server closed")