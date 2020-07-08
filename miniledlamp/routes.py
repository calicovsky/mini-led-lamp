from flask import render_template, request, jsonify
import logging
from miniledlamp import app
from miniledlamp import led_brightness_controller

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/led-brightness', methods=['GET', 'POST'])
def led_brightness():
  if request.method == 'POST':
    content = request.json
    brightness = content['brightness']
    logging.info(f'(POST) led_brightness: {brightness}')
    led_brightness_controller.set_brightness(brightness)
    return jsonify({'brightness': brightness})
  else:
    brightness = led_brightness_controller.get_brightness()
    print(brightness)
    logging.info(f'(GET) led_brightness: {brightness}')
    return jsonify({'brightness': brightness})
