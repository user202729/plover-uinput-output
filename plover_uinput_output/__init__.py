from typing import Dict, Tuple, TYPE_CHECKING, NamedTuple, Optional, Any
import subprocess
import sys
import time
import json
import argparse
import shlex
from pathlib import Path

import uinput

from plover import log
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

def send_message(process: subprocess.Popen, message: bytes)->None:
	# might raise BlockingIOError if the subprocess misbehave
	# is this safe without a lock? TODO test
	assert process.stdin is not None
	process.stdin.write(len(message).to_bytes(8, "little"))
	process.stdin.write(message)
	process.stdin.flush()

def send_json(process, data: Any)->None:
	send_message(process, json.dumps(data).encode('u8'))

process=None

def start()->None:
	global process
	assert not process


	#import inspect
	#lines=inspect.getsource(run).splitlines()
	#assert lines[0].lstrip().startswith('def')
	#indentation = len(lines[1])-len(lines[1].lstrip())
	#code="\n".join(line[indentation:] for line in lines[1:])

	print(__file__)
	code=(Path(__file__).parent / 'subprocess_run.py').open('r').read()

	process=subprocess.Popen(("sudo", sys.executable, "-c", code),
			stdin=subprocess.PIPE,
			#stdout=subprocess.DEVNULL,
			#stderr=subprocess.DEVNULL,
			)

	uinput_import_path=bytes(Path(uinput.__file__).parent.parent)
	assert uinput_import_path
	send_message(process,uinput_import_path)


class Main:
	def __init__(self, engine: "plover.engine.StenoEngine")->None:
		self._engine: "plover.engine.StenoEngine" = engine

	def start(self)->None:
		"""Starts the server.

		If the extension is enabled, this function is called when Plover starts.
		"""
		print("==start?")
		start()

	def stop(self)->None:
		#send_message(process, b"")
		#process.wait()
		print("stop?")

# https://www.kernel.org/doc/html/v4.12/input/uinput.html
#
# [...] so that userspace has time to detect, initialize the new device, and
# can start listening to the event, otherwise it will not notice the event we
# are about to send.

#time.sleep(2)

key_name_to_uinput_keycode_lookup_list = [
		(a.lower()[len("key_"):], getattr(uinput, a)[1])
		for a in dir(uinput) if a.startswith("KEY_")
		]
key_name_to_uinput_keycode_lookup=dict(key_name_to_uinput_keycode_lookup_list)
assert len(key_name_to_uinput_keycode_lookup)==len(key_name_to_uinput_keycode_lookup_list)


symbol_to_keycode=dict(zip(r"-=[]\;',./`" + "\t\n",
	[key_name_to_uinput_keycode_lookup[name] for name in
		"minus equal leftbrace rightbrace backslash semicolon apostrophe comma dot slash grave tab enter".split()
		]))

unshift_symbol_to_keycode=dict(zip(r'!@#$%^&*()_+{}|:"<>?~',
	[symbol_to_keycode.get(symbol) or key_name_to_uinput_keycode_lookup[symbol]
		for symbol in r"1234567890-=[]\;',./`"]
	))

for c in map(chr, range(ord('a'), ord('z')+1)):
	symbol_to_keycode[c]=unshift_symbol_to_keycode[c.upper()]=key_name_to_uinput_keycode_lookup[c]


from .set_xkb_alias import set_xkb_alias
set_xkb_alias(key_name_to_uinput_keycode_lookup)

for mod in "alt control shift super".split():
	key_name_to_uinput_keycode_lookup[mod] = key_name_to_uinput_keycode_lookup[mod+"_l"]

def key_name_to_uinput_keycode(key_name: str)->Optional[int]:
	return key_name_to_uinput_keycode_lookup[key_name]

assert uinput.KEY_A == (1, 30)
assert uinput.KEY_1 == (1, 2)
def uinput_keycode_to_event(uinput_keycode: int)->Tuple[int, int]:
	return (1, uinput_keycode)


#exclam 1 1
#at 2 1
#numbersign 3 1
#dollar 4 1
#percent 5 1
#asciicircum 6 1
#ampersand 7 1
#asterisk 8 1
#parenleft 9 1
#greater 102nd 1

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

	def set_time_between_key_presses(self, ms: int):
		print('???', ms)
		pass

	def send_backspaces(self, number_of_backspaces: int):
		for _ in range(number_of_backspaces):
			global process
			send_json(process, (uinput.KEY_BACKSPACE, 1))
			send_json(process, (uinput.KEY_BACKSPACE, 0))

	def send_string(self, s: str):
		for char in s:
			if char in unshift_symbol_to_keycode:
				keycode=unshift_symbol_to_keycode[char]
				self._send_key("leftshift", 1)
				self._send_keycode(keycode, 1)
				self._send_keycode(keycode, 0)
				self._send_key("leftshift", 0)

			elif char in symbol_to_keycode:
				keycode=symbol_to_keycode[char]
				self._send_keycode(keycode, 1)
				self._send_keycode(keycode, 0)

			else:
				key_name=CHAR_TO_KEYNAME.get(char)
				if key_name is None:
					log.warning("Char %s not supported", char)
					continue

				self._send_key(key_name, 1)
				self._send_key(key_name, 0)

	def _send_keycode(self, uinput_keycode: int, pressed: int)->None:
		event = uinput_keycode_to_event(uinput_keycode)
		send_json(process, (event, 1 if pressed else 0))

	def _send_key(self, key_name: str, pressed: int)->None:
		global process
		uinput_keycode = key_name_to_uinput_keycode(key_name)
		print(key_name, uinput_keycode)
		if uinput_keycode is None:
			log.warning("Key %s not supported", key_name)
		else:
			self._send_keycode(uinput_keycode, pressed)


	def send_key_combination(self, combo_string: str)->None:
		key_events = self._key_combo.parse(combo_string)
		for key_name, pressed in key_events:
			self._send_key(key_name, pressed)
