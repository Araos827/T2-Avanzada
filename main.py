import os
import sys
import PyQt5.QtCore as core
from PyQt5 import uic
import PyQt5.QtWidgets as widgets
import PyQt5.QtGui as gui
from windows import VentanaInicio, VentanaJuego
from dccafe import DCCafe
from threads import MiuEnzo

def hook(type, value, traceback):
    print(type)
    print(traceback)
sys.__excepthook__ = hook


#instanciar
app = widgets.QApplication([])
ventana_inicial = VentanaInicio()
ventana_juego = VentanaJuego()
enzo = MiuEnzo(ventana_juego.display_x, ventana_juego.display_y)
dcc = DCCafe(enzo)


#conectar
ventana_inicial.senal_abrir_ventana.connect(ventana_juego.cargar_objetos)
ventana_juego.senal_cargar_partida.connect(dcc.cargar_partida)
ventana_juego.senal_mover_character.connect(enzo.move)
dcc.send_reputacion_signal.connect(ventana_juego.recibir_reputacion)
dcc.send_ronda_signal.connect(ventana_juego.recibir_ronda)
dcc.send_dinero_signal.connect(ventana_juego.recibir_dinero)
dcc.send_clientes_antedidos_signal.connect(ventana_juego.recibir_clientes_atendidos)
dcc.send_clientes_perdidos_signal.connect(ventana_juego.recibir_clientes_perdidos)
dcc.send_clientes_proximos_signal.connect(ventana_juego.recibir_clientes_proximos)
dcc.send_resumen_ronda_signal.connect(ventana_juego.recibir_resumen)
ventana_juego.send_pause_signal.connect(dcc.recieve_pause)
ventana_juego.senal_reiniciar_partida.connect(dcc.reiniciar_partida)
ventana_juego.senal_guardar.connect(dcc.guardar_partida)
ventana_juego.senal_comenzar_ronda.connect(dcc.comenzar_ronda)
enzo.update_position_signal.connect(ventana_juego.update_position)
dcc.senal_update_position.connect(ventana_juego.update_position)
ventana_juego.display_label.senal_drop.connect(dcc.create_object)
dcc.senal_create_object.connect(ventana_juego.create_object)
ventana_juego.senal_check_superposicion.connect(dcc.chequear_superposicion)
dcc.senal_return_intersection.connect(ventana_juego.recive_superposicion)
ventana_juego.senal_send_object.connect(dcc.recieve_object)
enzo.senal_chequear_colision.connect(dcc.chequear_colision)
dcc.senal_return_colision.connect(enzo.recibir_colision)

sys.exit(app.exec_())