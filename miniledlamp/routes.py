from flask import render_template, request, jsonify
import logging
import subprocess
from miniledlamp import app
from miniledlamp import led_brightness_controller
from miniledlamp import turn_off_timer
from miniledlamp import wifi_util

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

@app.route('/turn-off-timer', methods=['GET', 'POST'])
def _turn_off_timer(): # '_' for avoiding name conflict with the module
  if request.method == 'POST':
    content = request.json
    enabled = content['enabled']
    timer_index = content['timer_index']
    if enabled == True:
      hour = content['hour'] if 'hour' in content else -1
      minute = content['minute'] if 'minute' in content else -1
      logging.info(f'(POST) setting timer: [{timer_index}] (enabled: {enabled}) {hour}:{minute}')
      turn_off_timer.TurnOffTimerUtil.set_timer(timer_index, hour, minute)
    else:
      logging.info(f'(POST) clearing timer: [{timer_index}]')
      turn_off_timer.TurnOffTimerUtil.clear_timer(timer_index)
    return jsonify({'timers': turn_off_timer.TurnOffTimerUtil.get_timers()})
  else:
    return jsonify({'timers': turn_off_timer.TurnOffTimerUtil.get_timers()})

@app.route('/add-turn-off-timer', methods=['POST'])
def add_turn_off_timer():
  return jsonify({'awww': True})

@app.route('/wifi-settings')
def wifi_settings():
  return render_template('wifi-settings.html')

@app.route('/connect-to-wireless-ap')
def connect_to_wireless_ap():
  status = wifi_util.connect(ssid, password)
  return jsonify({'status': status, 'message': 'awww'})

@app.route('/get-currently-connected-wireless-ap-info')
def get_currently_connected_wireless_ap_info():
  return jsonify({'ssid': wifi_util.get_currently_connected_ap_ssid()})

@app.route('/shutdown')
def shutdown_this_computer():
  subprocess.check_output(['sudo', 'shutdown'])
  return jsonify({'awww': True})
