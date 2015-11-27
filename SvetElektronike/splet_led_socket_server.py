from RPi import GPIO
import socket
import time

GPIO.setmode(GPIO.BOARD)
leds_pin = [11,12,13]

for x in range(0, len(leds_pin)):
	GPIO.setup(leds_pin[x], GPIO.OUT) # led out

from flask import Flask, render_template, request

app = Flask(__name__, static_url_path = "", static_folder = "img")
html = ["" for x in range(len(leds_pin)+4)]

for x in range(0, len(leds_pin)):
	img_off = """<img id="button""" + str(x) + """" src="/red/red_""" + str(x)  + """.jpg">"""
	html[x] = """<a href="/ledOn/""" + str(x) + """">""" + img_off + """</a>"""

html[len(leds_pin)] = """<p>Senzor premika: /N/A <a href="/status/1">osvezi</a><br>"""
html[len(leds_pin)+1] = """Senzor zvoka: /N/A <a href="/status/2">osvezi</a><br>"""
html[len(leds_pin)+2] = """Temperaturni senzor: /N/A <a href="/status/3">osvezi</a><br>"""
html[len(leds_pin)+3] =  """Senzor vlage: /N/A <a href="/status/4">osvezi</a></p></body></html>"""
	
@app.route("/")
def zacetek():
      	return ' '.join(html)

@app.route("/ledOn/<number>")
def ledOn(number):
	pin_number = leds_pin[int(number)]
	# prizgi led
	GPIO.output(pin_number, 1)
	# zamenjaj sliko
	img_on = """<img id="button""" + number + """" src="/green/green_""" + number + """.jpg">"""
	html[int(number)] = """<a href="/ledOff/""" + number + """">""" + img_on + """</a>"""
	return ' '.join(html)

@app.route("/ledOff/<number>")
def ledOff(number):
	pin_number = leds_pin[int(number)]
	# ugasni led
	GPIO.output(pin_number, 0)
	# zamenjaj sliko
	img_off = """<img id="button""" + number + """" src="/red/red_""" + number  + """.jpg">"""
	html[int(number)] = """<a href="/ledOn/""" + number + """">""" + img_off + """</a>"""	 
	return ' '.join(html)

@app.route("/status/<number>")
def status(number):
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('192.168.1.15', 50007))
	time.sleep(1)

	# req = M
        if (number == "1"):
		s.sendall('M')
        	data = s.recv(1024)
		s.close()        	
		html[len(leds_pin)] = """<p>Senzor premika: """ + data.split(":")[1]  + """ <a href="/status/1">osvezi</a><br>"""
	# req = L
	if (number == "2"):
		s.sendall('L')
		data = s.recv(1024)
		s.close()
		html[len(leds_pin)+1] = """Senzor zvoka: """ + data.split(":")[1] +  """ <a href="/status/2">osvezi</a><br>"""
       # req = T
        if (number == "3"): 
		s.sendall('T')     
		data = s.recv(1024)
		s.close()    
		html[len(leds_pin)+2] = """Temperaturni senzor: """ + data.split(":")[1] + """&deg;C <a href="/status/3">osvezi</a><br>"""
        # req = H
        if (number == "4"):
		s.sendall('H')
		data = s.recv(1024)
		s.close()
		html[len(leds_pin)+3] = """Senzor vlage: """ + data.split(":")[1] + """ <a href="/status/4">osvezi</a></p>"""
	 
	return ' '.join(html)
	
app.run(host="192.168.1.5") 


