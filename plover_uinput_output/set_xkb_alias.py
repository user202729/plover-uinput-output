from typing import Dict

def set_xkb_alias(key_name_to_uinput_keycode: Dict[str, str])->None:
	for k, v in [a.split() for a in """
	alt_l leftalt
	alt_r rightalt
	audioforward fastforward
	audiolowervolume volumedown
	audiomedia media
	audiomute min_interesting
	audiomute mute
	audionext nextsong
	audiopause pausecd
	audioplay play
	audioplay playcd
	audioplay playpause
	audioprev previoussong
	audioraisevolume volumeup
	audiorecord record
	audiorewind rewind
	audiostop stopcd
	bracketleft leftbrace
	bracketright rightbrace
	calculator calc
	cancel stop
	caps_lock capslock
	close exit
	control_l leftctrl
	control_r rightctrl
	display switchvideomode
	dos msdos
	eject ejectcd
	eject ejectclosecd
	escape esc
	explorer file
	favorites bookmarks
	game sport
	go connect
	henkan_mode henkan
	hiragana_katakana katakanahiragana
	kbdbrightnessdown kbdillumdown
	kbdbrightnessup kbdillumup
	kbdlightonoff kbdillumtoggle
	kp_add kpplus
	kp_begin kp5
	kp_decimal kpcomma
	kp_delete kpdot
	kp_divide kpslash
	kp_down kp2
	kp_end kp1
	kp_enter kpenter
	kp_equal kpequal
	kp_home kp7
	kp_insert kp0
	kp_left kp4
	kp_multiply kpasterisk
	kp_next kp3
	kp_page_down kp3
	kp_page_up kp9
	kp_prior kp9
	kp_right kp6
	kp_subtract kpminus
	kp_up kp8
	l1 f11
	l2 f12
	launch1 prog1
	launch2 prog2
	launch3 prog3
	launch4 prog4
	launch5 f14
	launch6 f15
	launch7 f16
	launch8 f17
	launch9 f18
	launcha scale
	launchb dashboard
	less 102nd
	mail email
	mailforward forwardmail
	menu compose
	menukb menu
	messenger chat
	monbrightnessdown brightnessdown
	monbrightnessup brightnessup
	mycomputer computer
	next pagedown
	num_lock numlock
	page_down pagedown
	page_up pageup
	parenleft kpleftparen
	parenright kprightparen
	period dot
	plusminus kpplusminus
	poweroff power
	print sysrq
	prior pageup
	quoteleft grave
	quoteright apostrophe
	redo again
	reload refresh
	return enter
	rotatewindows direction
	rotatewindows rotate_display
	screensaver coffee
	screensaver screenlock
	scroll_lock scrolllock
	send sendfile
	shift_l leftshift
	shift_r rightshift
	super_l leftmeta
	super_r rightmeta
	taskpane cyclewindows
	tools config
	tools f13
	webcam camera
	xf86_audioforward fastforward
	xf86_audiolowervolume volumedown
	xf86_audiomedia media
	xf86_audiomute min_interesting
	xf86_audiomute mute
	xf86_audionext nextsong
	xf86_audiopause pausecd
	xf86_audioplay play
	xf86_audioplay playcd
	xf86_audioplay playpause
	xf86_audioprev previoussong
	xf86_audioraisevolume volumeup
	xf86_audiorecord record
	xf86_audiorewind rewind
	xf86_audiostop stopcd
	xf86_back back
	xf86_battery battery
	xf86_bluetooth bluetooth
	xf86_calculator calc
	xf86_close close
	xf86_close exit
	xf86_copy copy
	xf86_cut cut
	xf86_display switchvideomode
	xf86_documents documents
	xf86_dos msdos
	xf86_eject ejectcd
	xf86_eject ejectclosecd
	xf86_explorer file
	xf86_favorites bookmarks
	xf86_finance finance
	xf86_forward forward
	xf86_game sport
	xf86_go connect
	xf86_homepage homepage
	xf86_kbdbrightnessdown kbdillumdown
	xf86_kbdbrightnessup kbdillumup
	xf86_kbdlightonoff kbdillumtoggle
	xf86_launch1 prog1
	xf86_launch2 prog2
	xf86_launch3 prog3
	xf86_launch4 prog4
	xf86_launch5 f14
	xf86_launch6 f15
	xf86_launch7 f16
	xf86_launch8 f17
	xf86_launch9 f18
	xf86_launcha scale
	xf86_launchb dashboard
	xf86_mail email
	xf86_mailforward forwardmail
	xf86_mail mail
	xf86_menukb menu
	xf86_messenger chat
	xf86_monbrightnessdown brightnessdown
	xf86_monbrightnessup brightnessup
	xf86_mycomputer computer
	xf86_new new
	xf86_open open
	xf86_paste paste
	xf86_phone phone
	xf86_poweroff power
	xf86_reload refresh
	xf86_reply reply
	xf86_rotatewindows direction
	xf86_rotatewindows rotate_display
	xf86_save save
	xf86_screensaver coffee
	xf86_screensaver screenlock
	xf86_scrolldown scrolldown
	xf86_scrollup scrollup
	xf86_search search
	xf86_send send
	xf86_send sendfile
	xf86_shop shop
	xf86_sleep sleep
	xf86_taskpane cyclewindows
	xf86_tools config
	xf86_tools f13
	xf86_wakeup wakeup
	xf86_webcam camera
	xf86_wlan wlan
	xf86_www www
	xf86_xfer xfer
	
	exclam 1
	at 2
	numbersign 3
	dollar 4
	percent 5
	asciicircum 6
	ampersand 7
	asterisk 8
	parenleft 9
	parenright 0
	""".strip().splitlines() if a.strip()]:
		if k not in key_name_to_uinput_keycode:
			key_name_to_uinput_keycode[k]=key_name_to_uinput_keycode[v]