from gpiozero import Button
from time import sleep

btnUP = Button(26)
btnDOWN = Button(19)
btnLEFT = Button(13)
btnRIGHT = Button(6)
btnRESET = Button(5)
btnSET = Button(0)
btnMID = Button(1)
while True:
	if btnUP.is_pressed:
		print("UP")
	elif btnDOWN.is_pressed:
		print("DOWN")
	elif btnLEFT.is_pressed:
		print("LEFT")
	elif btnRIGHT.is_pressed:
		print("RIGHT")
	elif btnRESET.is_pressed:
		print("RESET")
	elif btnSET.is_pressed:
		print("SET")
	elif btnMID.is_pressed:
		print("MID")
	else:
	sleep(0.2)