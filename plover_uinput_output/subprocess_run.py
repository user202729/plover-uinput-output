
import sys
import json
import subprocess
from typing import Any

subprocess.run(('modprobe', 'uinput'), check=True)

def read_message()->bytes:
	message_size = int.from_bytes(sys.stdin.buffer.read(8), 'little') # 8 is definitely enough
	return sys.stdin.buffer.read(message_size)

def read_json()->Any:
	return json.loads(read_message().decode('u8'))

uinput_import_path=read_message()
#try:
#	import uinput
#except ImportError:
if uinput_import_path:
	sys.path.append(uinput_import_path.decode('u8'))
try:
	import uinput
except ImportError:
	uinput=None


try:
	events = [(1, x-8) for x in range(8, 256)]
	device = uinput.Device(events)
except PermissionError:
	raise

first_time = True

while True:
	data=read_message()
	if not data: break
	try:
		if first_time:
			if sys.platform.startswith('linux'):
				subprocess.run(
						r"xinput reattach $(xinput|grep python-uinput|sed -E 's/.*\tid=([0-9]+).*/\1/g') $(xinput|grep 'Virtual core keyboard'|sed -E 's/.*\tid=([0-9]+).*/\1/g')",
						shell=True)
			first_time = False
		device.emit(*json.loads(data))
	except:
		import traceback
		traceback.print_exc()
		print(data)
