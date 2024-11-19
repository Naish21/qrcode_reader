import os, sys, io
import M5
from M5 import *
from unit import QRCodeUnit
from hardware import sdcard
from hardware import *
import time


title0 = None
label0 = None
users = None
ili9342 = None
i2c0 = None
qrcode_0 = None

qrdata = []
usuarios = []
blacklist = []

# Describe this function...
def read_usuarios():
  global qrdata, usuarios, blacklist, title0, label0, users, ili9342, i2c0, qrcode_0
  try:
    with open('/sd/qr/usuarios.txt', 'r') as users:
      usuarios = users.readlines()
      usuarios = [i.strip() for i in usuarios]
      print(usuarios)
  except Exception:
    print('users file not found')
  try:
    with open('/sd/qr/blacklist.txt', 'r') as black:
      blacklist = black.readlines()
      blacklist = [i.strip() for i in blacklist]
      print(blacklist)
  except Exception:
    print('blacklist file not found')


def save_newuser(usuario):
  try:
    with open('/sd/qr/nuevos.txt', 'a') as nuevos:
      nuevos.write(f'{usuario}\n')
  except Exception:
    print(f"Ha fallado la escritura del usuario {usuario}")

def qrcode_0_event(_qrdata):
  global title0, label0, users, ili9342, i2c0, qrcode_0, qrdata, usuarios
  qrdata = _qrdata[0:6]
  if qrdata in usuarios:  # Autorizados
    Widgets.fillScreen(0x33cc00)  # VERDE
    label0.setText(str(qrdata))
    time.sleep(1.5)
  elif qrdata in blacklist:  # Blacklisteados
    Widgets.fillScreen(0xff0000)  # ROJO
    label0.setText(str(qrdata))
    time.sleep(3)
  else:  # No apuntados
    Widgets.fillScreen(0xffa500)  # NARANJA
    label0.setText(str(qrdata))
    save_newuser(qrdata)
    time.sleep(3)
  Widgets.fillScreen(0x000000)
  title0 = Widgets.Title("Ready to read QR-code", 3, 0xffffff, 0x0000FF, Widgets.FONTS.DejaVu18)


def setup():
  global title0, label0, users, ili9342, i2c0, qrcode_0, qrdata, usuarios

  M5.begin()
  title0 = Widgets.Title("Ready to read QR-code", 3, 0xffffff, 0x0000FF, Widgets.FONTS.DejaVu18)
  label0 = Widgets.Label("", 16, 36, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)

  sdcard.SDCard(slot=3, width=1, sck=40, miso=39, mosi=14, cs=12, freq=1000000)
  ili9342 = UserDisplay(panel=UserDisplay.PANEL.ILI9342, w=320, h=240, ox=0, oy=0, invert=True, rgb=False, spi_host=2, spi_freq=40, sclk=-1, mosi=-1, miso=-1, dc=-1, cs=-1, rst=-1, busy=-1, bl=-1, bl_invert=False, bl_pwm_freq=1000, bl_pwm_chn=0)
  i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
  qrcode_0 = QRCodeUnit(0, i2c0, 0x21)
  qrcode_0.set_event_cb(qrcode_0_event)
  read_usuarios()


def loop():
  global title0, label0, users, ili9342, i2c0, qrcode_0, qrdata, usuarios
  M5.update()
  qrcode_0.event_poll_loop()


if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")
