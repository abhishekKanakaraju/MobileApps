# -*- coding: utf-8 -*-
from kivy.lang import Builder
from plyer import gps
from kivy.app import App
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.clock import Clock, mainthread
from kivy.uix.popup import Popup
from kivy.network.urlrequest import UrlRequest
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.garden.mapview import MapView
import json


from os.path import exists
from kivy.uix.scatter import Scatter
from functools import partial

from plyer import camera
#from jnius import autoclass, cast

from PIL import Image

from base64 import b64encode

kv = '''
#:import C kivy.utils.get_color_from_hex
#:import sys sys
#:import MapSource mapview.MapSource
BoxLayout:
    canvas:
        Color:
            rgb: C('#ffffff')
        Rectangle:
            pos: self.pos
            size: self.size
    orientation: 'vertical'
    BoxLayout:
        assunto: assunto
        comentario: comentario
        comentario_lbl: comentario_lbl
        orientation: 'vertical'
        padding: [5, 5, 5, 5]
        spacing: 5
        Spinner:
            id: assunto
            text: 'Selecionar Assunto'
            background_color: C('#1180c4')
            background_normal: ''
            values: ('Buraco na rua', 'Iluminação', 'Lixo esposto', 'Mato', 'Entulho na rua/calçada', 'Sinalização', 'Esgoto exposto')
            size_hint_y: None
            height: '40dp'
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: '40dp'  
            Button:
                text: 'Capturar Foto'
                on_press: app.tirar_foto()
            Button:
                text: 'Enviar'
                on_press: app.salvarLocalizacao()
        Label:
            id: comentario_lbl
            text: 'Comentario:'
            halign: 'left'
            valign: 'middle'
            text_size: self.size
            color: C('#000000')
        TextInput:
            id: comentario
            text: ''
            hint_text: 'Escreva seu comentario...'
            input_filter: lambda text, from_undo: text[:140 -len(self.text)]
            multiline: True
    BoxLayout:
        orientation: 'vertical'
        MapView:
            lat: app.lat
            lon: app.long
            zoom: 15
            map_source: MapSource(sys.argv[1], attribution="") if len(sys.argv) > 1 else "osm"
            MapMarkerPopup:
                lat: app.lat
                lon: app.long
                popup_size: dp(230), dp(130)
                Bubble:
                    BoxLayout:
                        orientation: "horizontal"
                        padding: "5dp"
                        Label:
                            text: "[b]Você está aqui![/b]"
                            markup: True
                            halign: "center"                
'''

#Environment = autoclass('android.os.Environment')

class Picture(Scatter):
    source = StringProperty(None)


class GpsTest(App):
    gps_get = StringProperty()
    gps_location = StringProperty()
    gps_status = StringProperty()
    foto_carregada = StringProperty()
    lat = NumericProperty()
    long = NumericProperty()
    mapview = None

    def build(self):
        try:
            gps.configure(on_location=self.on_location,
                          on_status=self.on_status)
            self.start(0, 1000)

        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_status = 'Por favor, ative o GPS'
  
        return Builder.load_string(kv)
     
        

    def get_filename(self):
        fn = Environment.getExternalStorageDirectory().getPath() + '/fiscalizacao.jpg'
        return fn

    def tirar_foto(self):
        camera.take_picture(self.get_filename(), self.add_picture)
        self.root.ids.foto_carregada = 'Foto carregada com sucesso!'


    def add_picture(self, fn, *args):
        size = 300, 300
        im = Image.open(fn)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(fn, quality=95)

    def start(self, minTime, minDistance):
        gps.start(minTime, minDistance)

    def stop(self):
        gps.stop()

    @mainthread
    def on_location(self, **kwargs):
        self.lat = kwargs.get('lat')
        self.long = kwargs.get('lon')

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    def on_pause(self):
        gps.stop()
        return True

    def on_resume(self):
        gps.start(1000, 0)
        pass


    def salvarLocalizacao(self):
        self.filename = self.get_filename()
        with open(self.filename, 'rb') as self.f:
            self.data = self.f.read()
        self.imagem = b64encode(self.data)
        self.localizacao = "POINT(" + str(self.long) + " " + str(self.lat) + ")"
        self.params = json.dumps(
            {"assunto": self.root.ids.assunto.text, "comentario": self.root.ids.comentario.text, "localizacao": self.localizacao, "imagem": self.imagem})
        self.headers = {'Content-type': 'application/json',
                        'Accept': 'application/json; charset=UTF-8',
                        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'}
        self.req = UrlRequest('https://fiscaliza.herokuapp.com/api/add/', req_body=self.params, req_headers=self.headers,
                              on_success=self.postSucess, on_error=self.postFail)

    def postSucess(self, req, result):
        text = Label(text="Enviado com sucesso!".format())
        pop_up = Popup(title="Sucesso", content=text, size_hint=(.7, .7))
        pop_up.open()

    def postFail(self, req, result):
        text = Label(text="Erro de conexão, verifique sua internet!".format())
        pop_up = Popup(title="Erro de conexão", content=text, size_hint=(.7, .7))
        pop_up.open()



if __name__ == '__main__':
    GpsTest().run()
