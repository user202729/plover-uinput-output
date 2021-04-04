from typing import Dict, Tuple, TYPE_CHECKING, NamedTuple, Optional
import subprocess
import sys
import json
from pathlib import Path
from plover import log
import argparse
import shlex
from plover.oslayer.config import CONFIG_DIR
from plover.key_combo import KeyCombo, CHAR_TO_KEYNAME

have_output_plugin = False
try:
	from plover.oslayer import KeyboardEmulationBase
	have_output_plugin = True
except ImportError:
	pass


if TYPE_CHECKING:
	import plover.engine

class Main:
	def __init__(self, engine: "plover.engine.StenoEngine")->None:
		self._engine: "plover.engine.StenoEngine" = engine

	def start(self)->None:
		"""Starts the server.

		If the extension is enabled, this function is called when Plover starts.
		"""
		pass

	def stop(self)->None:
		raise NotImplementedError

import sys, time, subprocess
try:
	#sys.path.append("/home/user202729/python-local-lib/")
	import uinput
	events = [(1, x-8) for x in range(8, 256)]
	device = uinput.Device(events)
except PermissionError:
	print("elevate self")
	sys.exit(subprocess.run(["sudo"] + sys.argv).returncode)


# https://www.kernel.org/doc/html/v4.12/input/uinput.html
#
# [...] so that userspace has time to detect, initialize the new device, and
# can start listening to the event, otherwise it will not notice the event we
# are about to send.

#time.sleep(2)

key_name_to_uinput_keycode_lookup = {
		a.lower()[len("key_"):]: getattr(uinput, a)[1]
		for a in dir(uinput) if a.startswith("KEY_")
		}

def key_name_to_uinput_keycode(key_name: str)->Optional[int]:
	return key_name_to_uinput_keycode_lookup[key_name]

assert uinput.KEY_A == (1, 30)
assert uinput.KEY_1 == (1, 2)
def uinput_keycode_to_event(uinput_keycode: int):
	return (1, uinput_keycode)

device.emit(uinput.KEY_E, 1) # Press.
print("Pressed")
time.sleep(2)
device.emit(uinput.KEY_E, 0) # Release.
print("Released")


class KeyboardEmulation(*([KeyboardEmulationBase] if have_output_plugin else [])):
	"""Emulate keyboard events."""

	@classmethod
	def get_option_info(cls):
		return {}

	def __init__(self, params=None):
		if have_output_plugin:
			KeyboardEmulationBase.__init__(self, params)
		self._key_combo = KeyCombo()

	def start(self):
		pass

	def cancel(self):
		pass

	def send_backspaces(self, number_of_backspaces):
		for _ in number_of_backspaces:
			device.emit(uinput.KEY_BACKSPACE, 1)
			device.emit(uinput.KEY_BACKSPACE, 0)

	def send_string(self, s):
		for char in s:
			try:
				key_name = CHAR_TO_KEYNAME[char]
			except KeyError:
				log.warning("Char %s not supported", char)
				continue

			self._send_key(key_name, 1)
			self._send_key(key_name, 0)

	def _send_key(key_name, pressed: int):
		uinput_keycode = key_name_to_uinput_keycode(key_name)
		if uinput_keycode is None:
			log.warning("Key %s not supported", key_name)
		else:
			event = uinput_keycode_to_event(uinput_keycode)
			device.emit(event, 1 if pressed else 0)


	def send_key_combination(self, combo_string):
		key_events = self._key_combo.parse(combo_string)
		for key_name, pressed in key_events:
			self._send_key(key_name, pressed)
