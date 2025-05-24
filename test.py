from microbit import *
from maqueenplusv2 import *

init_maqueen()
display.show(Image('00000:'
                  '09090:'
                  '00500:'
                  '60006:'
                  '07770'))
while True:
   if button_b.was_pressed():
       sleep_ms(200)
       spin_right(50)
       sleep_ms(200)
       spin_left(50)
       sleep_ms(400)
       spin_right(50)
       sleep_ms(200)
       backup(50)
       sleep_ms(200)
       drive(50)
       sleep_ms(200)
       stop()
   elif button_a.was_pressed():
       sleep_ms(200)
       spin_right(100)
       sleep_ms(1800)
       stop()
   elif pin_logo.is_touched():
       for _ in range(4):
           display.show(Image('09090:'
                              '00500:'
                              '60006:'
                              '07770:'
                              '00000'))
           sleep_ms(100)
           display.show(Image('00000:'
                              '09090:'
                              '00500:'
                              '60006:'
                              '07770'))
           sleep_ms(100)