
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

while True:
	data=read_message()
	if not data: break
	try:
		device.emit(*json.loads(data))
	except:
		import traceback
		traceback.print_exc()
		print(data)
