import subprocess
import logging
from wireless import Wireless
import re

def get_currently_connected_ap_ssid():
  # strip() trims the trailing newline character
  # Typically, decode-strip-split will convert the raw check_output() like
  # b'wlan0     ESSID:"NyankoLab-2.4G"\n'
  # into
  # ['wlan0', 'ESSID:"NyankoLab-2.4G"']
#  stdout = subprocess.check_output(['iwgetid']).decode('utf-8').strip().split()
#  logging.info(f'Wi-Fi AP info: {stdout}')
#  if len(stdout) < 2:
#    return ''
#  essid_and_name = stdout[1].split(':')
#  if len(essid_and_name) < 2:
#    logging.warn(f'iwgetid returned SSID info in an unexpected format: {stdout}')
#    return ''
#  ssid = essid_and_name[1].strip('"')
#  return ssid if 0 < len(ssid) else None
  w = Wireless()
  ssid = w.current()
  logging.info(f'Current ssid: {ssid}')
  return ssid

# Returns an array where each element represents an available WiFi network
def scan_and_list_available_networks():
  wireless_interface = 'wlan0'
  s = subprocess.check_output(['sudo', 'iwlist', wireless_interface, 'scanning']).decode('utf-8')
  lines = s.split('\n')
  # TODO: parse network information as well, e.g. signal strength
  ssids = [ line.strip().split(':')[1].strip('"') for line in lines if line.strip().startswith('ESSID:') ]
  #print(ssids)
  aps = []
  for ssid in ssids:
    if len(ssid) == 0:
      continue
    aps.append({'ssid': ssid})
  return aps

def replace_in_file(regex, replacement_string, file_pathname):
  replaced = False
  with open(file_pathname, "rt") as fin:
    with open("replace", "wt") as fout:
      for line in fin:
        if replaced:
          fout.write(line)
        else:
          result = re.sub(regex, replacement_string, line)
          fout.write(result)
          # Replace only the first occurrence
          if line != result:
            replaced = True
        
  subprocess.check_output(['cp', '-f', 'replace', file_pathname])

def change_ssid_and_password_in_wpa_supplicant_conf(ssid, password):
  # Edit wpa_supplicant.conf
  temporary_file = 'copy-wpa_supplicant.conf'
  # Copy the file to the current working directory for editing
  subprocess.check_output(['sudo', 'cp', '/etc/wpa_supplicant/wpa_supplicant.conf', temporary_file])
  # Change the permission so we can edit (wpa_supplicant.conf is usually 600)
  subprocess.check_output(['sudo', 'chmod', '666', temporary_file])
  # Replace ssid
  replace_in_file(r'ssid=".+"$', f'ssid="{ssid}"', temporary_file)
  # Replace password
  replace_in_file(r'psk=".+"$', f'psk="{password}"', temporary_file)
  # Set the permission back to 600
  subprocess.check_output(['sudo', 'chmod', '600', temporary_file])
  # Replace the current wpa_supplicant.conf
  subprocess.check_output(['sudo', 'cp', '-f', temporary_file, '/etc/wpa_supplicant/wpa_supplicant.conf'])

def connect(ssid, password):
  #interface_name = 'wlan0'
  #results = subprocess.check_output(['sudo', 'wpa_cli', f'-i{interface_name}', 'add_network']).decode('utf-8')
  #id = int(results)
  #results = subprocess.check_output(['sudo', 'wpa_cli', id, 'ssid', ssid])
  #results = subprocess.check_output(['sudo', 'wpa_cli', id, 'psk', password])
  #results = subprocess.check_output(['sudo', 'wpa_cli', 'enable_network', id])

  # Use the wireless library
  # w = Wireless()
  # connected = w.connect(ssid, password)
  # logging.error(f'Failed to connect to the wireless network "{ssid}"')

  change_ssid_and_password_in_wpa_supplicant_conf(ssid, password)

  # This restarts wifi
  # Ref: https://raspberrypi.stackexchange.com/questions/73749/how-to-connect-to-wifi-without-reboot
  subprocess.check_output(['sudo', 'systemctl' ,'daemon-reload'])
  subprocess.check_output(['sudo', 'systemctl' ,'restart', 'dhcpcd'])

  i = 0
  num_retries = 5
  seconds_to_sleep = 2.0
  while i < num_retries:
    ssid = get_currently_connected_ap_ssid()
    if 0 < len(ssid):
      return 'success'
    time.sleep(2.0)

  return 'error'
