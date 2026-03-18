import os, sys
if sys.platform == "win32":
	os.system("color")

CYAN = "\033[36m"
RESET = "\033[0m"

print(f"{CYAN}--------------------------------{RESET}")
print(f"{CYAN}Currently in main.py{RESET}")
print(f"{CYAN}--------------------------------{RESET}")

import gi, status, config, math, pathlib
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk, Gdk, GLib
settings = Gtk.Settings.get_default()
settings.set_property("gtk-icon-theme-name", "Adwaita")

if sys.platform not in ["win32", "linux"]:
	status.fatal(f"Unsupported OS: {sys.platform}")
status.info("Attempting to create and present libadwaita window")


running = False

OUTLINE_WIDTH_DIVIDER = 1000

def saveConfig(widget, path, widgetType):
	if widgetType == Gtk.SpinButton:
		value = widget.get_value()
	elif widgetType == Gtk.CheckButton:
		value = widget.get_active()
	elif widgetType == Gtk.ColorDialogButton:
		rgba = widget.get_rgba()
		value = [rgba.red, rgba.green, rgba.blue, rgba.alpha]
	if value == config.readFromConfig(path): return
	config.writeToConfig(path, value)
	updateTimerVisuals()


def stopTimer(close = True):
	global timerDialog, running
	running = False
	if close: timerDialog.close()

def createOutlineShadow(radius, color, steps):
	shadows = []
	for i in range(steps):
		angle = (2 * math.pi * i) / steps
		x = round(math.cos(angle) * radius, 2)
		y = round(math.sin(angle) * radius, 2)
		shadows.append(f"{x}px {y}px 0 {color}")
	return ", ".join(shadows)

def updateTimerVisuals():
	try:
		timerDialog
	except NameError:
		return
	padding = config.readFromConfig("preferences.padding")
	fontSize = config.readFromConfig("preferences.fontSize")
	fontWeight = config.readFromConfig("preferences.fontWeight")
	backgroundOpacity = config.readFromConfig("preferences.backgroundOpacity")/100
	textColor = config.readFromConfig("preferences.textColor")
	textColor = [textColor[0]*255, textColor[1]*255, textColor[2]*255, textColor[3]]
	textOutline = config.readFromConfig("preferences.textOutline")
	outlineColor = config.readFromConfig("preferences.outlineColor")
	outlineColor = [outlineColor[0]*255, outlineColor[1]*255, outlineColor[2]*255, outlineColor[3]]
	outlineWidth = config.readFromConfig("preferences.outlineWidth")
	outlineWidth = outlineWidth / OUTLINE_WIDTH_DIVIDER * fontSize
	textShadow = config.readFromConfig("preferences.textShadow")
	shadowColor = config.readFromConfig("preferences.shadowColor")
	shadowColor = [shadowColor[0]*255, shadowColor[1]*255, shadowColor[2]*255, shadowColor[3]]

	cssData = f"""
	.timer {{ font-size: {fontSize}px; font-weight: {fontWeight}; color: rgba({textColor[0]}, {textColor[1]}, {textColor[2]}, {textColor[3]}); }}
	.outlined-text {{ text-shadow: {createOutlineShadow(outlineWidth, f"rgba({outlineColor[0]}, {outlineColor[1]}, {outlineColor[2]}, {outlineColor[3]})", 32)}; }} 
	.shadowed-text {{ text-shadow: {fontSize/10}px {fontSize/10}px 10px rgba({shadowColor[0]}, {shadowColor[1]}, {shadowColor[2]}, {shadowColor[3]}); }}
	.outlined-shadowed-text {{
		text-shadow: 
		{createOutlineShadow(outlineWidth, f"rgba({outlineColor[0]}, {outlineColor[1]}, {outlineColor[2]}, {outlineColor[3]})", 32)},
		{fontSize/10}px {fontSize/10}px 10px rgba({shadowColor[0]}, {shadowColor[1]}, {shadowColor[2]}, {shadowColor[3]});
	}}
	.timer-dialog {{ 
	background-color: alpha(@window_bg_color, {backgroundOpacity}); 
	border-radius: 12px;
	outline-color: alpha(@window_bg_color, {backgroundOpacity});
	box-shadow: 0 4px 12px alpha(black, {backgroundOpacity}); }}
	"""

	if textOutline and textShadow:
		timerLabel.add_css_class("outlined-shadowed-text")
		timerLabel.remove_css_class("outlined-text")
		timerLabel.remove_css_class("shadowed-text")
	elif textShadow:
		timerLabel.add_css_class("shadowed-text")
		timerLabel.remove_css_class("outlined-text")
		timerLabel.remove_css_class("outlined-shadowed-text")
	elif textOutline:
		timerLabel.add_css_class("outlined-text")
		timerLabel.remove_css_class("shadowed-text")
		timerLabel.remove_css_class("outlined-shadowed-text")
	else:
		timerLabel.remove_css_class("outlined-text")
		timerLabel.remove_css_class("shadowed-text")
		timerLabel.remove_css_class("outlined-shadowed-text")

	css = Gtk.CssProvider()
	css.load_from_data(cssData)
		
	Gtk.StyleContext.add_provider_for_display(timerDialog.get_display(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

	timerLabel.set_margin_start(fontSize*padding/100)
	timerLabel.set_margin_end(fontSize*padding/100)
	timerLabel.set_margin_top(fontSize*padding/100)
	timerLabel.set_margin_bottom(fontSize*padding/100)

def startTimer():
	global timerDialog, running, timerLabel

	hours = int(config.readFromConfig("time.hours"))
	minutes = int(config.readFromConfig("time.minutes"))
	seconds = int(config.readFromConfig("time.seconds"))

	if hours == 0 and minutes == 0 and seconds == 0:
		startLabel.set_label("Start")
		startImage.set_from_icon_name("media-playback-start-symbolic")
		status.error("Cannot start timer when it's at 0 seconds.")
		return

	running = True
	
	timerDialog = Gtk.Window()
	timerDialog.set_resizable(False)
	timerDialog.set_titlebar(Gtk.Box())
	timerDialog.set_title("shaweelTimerInstance")
	def close():
		startLabel.set_label("Start"),
		startImage.set_from_icon_name("media-playback-start-symbolic"),
		stopTimer(False)
		status.success("Timer stopped")
		return False
		

	timerDialog.connect("close-request", lambda window: close())

	timerLabel = Gtk.Label(label=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
	timerLabel.add_css_class("timer")

	def countDown():
		nonlocal hours, minutes, seconds
		
		if not running: 
			return False
		elif seconds == 1 and minutes == 0 and hours == 0:
			seconds -= 1
			stopTimer(True)
			status.showDialog("done", "The timer has finished.")
			return False
		elif seconds > 0:
			seconds -= 1
		elif minutes > 0:
			seconds = 59
			minutes -= 1
		elif minutes <= 0 and hours > 0:
			seconds = 59
			minutes = 59
			hours -= 1
		
		timerLabel.set_label(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
		return True
	
	GLib.timeout_add(1000, lambda: countDown())

	handle = Gtk.WindowHandle()
	handle.set_child(timerLabel)
	
	updateTimerVisuals()

	timerDialog.add_css_class("timer-dialog")
	timerDialog.set_child(handle)
	timerDialog.present()
	def windowsAlwaysOnTop():
		import ctypes
		HWND_TOPMOST = -1
		SWP_NOMOVE = 0x0002
		SWP_NOSIZE = 0x0001
		hwnd = ctypes.windll.user32.FindWindowW(None, "shaweelTimerInstance")
		if hwnd:
			status.success("Window found")
			ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
			status.success("Made window always on top")
			return False
		status.warn("Didn't find window")
		return True
	
	if sys.platform == "win32":
		status.info("Waiting for window...")
		GLib.timeout_add(250, windowsAlwaysOnTop)
	elif sys.platform == "linux":
		ignoreFile = pathlib.Path.home() / ".config" / "shaweelTimer" / ".noAlwaysOnTopWarning"
		if not ignoreFile.exists(): status.warn("You will have to make the timer always on top yourself since you're on Linux. On GNOME you can achieve this by right clicking the timer and checking the \"Always on Top\" option. This is because, there is no cross-platform way to make a window always on top.", True)
	status.success("Timer started")

def openPreferences(button: Gtk.Button):
	dialog = Adw.Dialog()
	css = Gtk.CssProvider()
	css.load_from_data(b".title-5 { font-size: 16px; font-weight: 600; }")
	Gtk.StyleContext.add_provider_for_display(dialog.get_display(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
	dialog.set_size_request(400, 0)
	mainOverlay = Gtk.Overlay()

	mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
	mainBox.set_margin_top(10)
	mainBox.set_margin_bottom(20)
	mainBox.set_margin_start(20)
	mainBox.set_margin_end(20)

	title = Gtk.Label(label="Preferences")
	title.add_css_class("title-2")
		
	def createOption(name, widget):
		optionBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		label = Gtk.Label(label=name)
		label.add_css_class("title-5")
		spacer = Gtk.Box()
		spacer.set_hexpand(True)
		optionBox.append(label)
		optionBox.append(spacer)
		optionBox.append(widget)
		return optionBox

	backgroundOpacity = Gtk.SpinButton()
	backgroundOpacity.set_range(0, 100)
	backgroundOpacity.set_increments(1, 5)
	backgroundOpacity.set_width_chars(5)
	def formatButton(button):
			value = int(button.get_value())
			button.set_text(f"{value}%")
			return True
	backgroundOpacity.connect("output", formatButton)

	padding = Gtk.SpinButton()
	padding.set_range(0, 100)
	padding.set_increments(1, 5)
	padding.set_width_chars(5)
	def formatButton(button):
			value = int(button.get_value())
			button.set_text(f"{value}%")
			return True
	padding.connect("output", formatButton)

	fontSize = Gtk.SpinButton()
	fontSize.set_range(8, 120)
	fontSize.set_increments(1, 4)
	fontSize.set_width_chars(4)

	fontWeight = Gtk.SpinButton()
	fontWeight.set_range(100, 900)
	fontWeight.set_increments(100, 100)
	fontWeight.set_width_chars(4)

	textColor = Gtk.ColorDialogButton(dialog=Gtk.ColorDialog())

	textOutline = Gtk.CheckButton()
	textOutline.connect("toggled", lambda widget: [
		outlineColor.set_sensitive(widget.get_active()),
		outlineWidth.set_sensitive(widget.get_active()),
		])

	outlineColor = Gtk.ColorDialogButton(dialog=Gtk.ColorDialog())
	outlineColor.set_sensitive(textOutline.get_active())

	outlineWidth = Gtk.SpinButton()
	outlineWidth.set_range(1, 100)
	outlineWidth.set_increments(1, 1)
	outlineWidth.set_sensitive(textOutline.get_active())
	outlineWidth.set_width_chars(5)
	outlineWidth.connect("output", formatButton)

	textShadow = Gtk.CheckButton()
	textShadow.connect("toggled", lambda widget: [
		shadowColor.set_sensitive(widget.get_active()),
		])

	shadowColor = Gtk.ColorDialogButton(dialog=Gtk.ColorDialog())
	shadowColor.set_sensitive(textShadow.get_active())


	mainBox.append(title)
	mainBox.append(createOption("Padding", padding))
	mainBox.append(createOption("Background Opacity", backgroundOpacity))
	mainBox.append(createOption("Font Size", fontSize))
	mainBox.append(createOption("Font Weight", fontWeight))
	mainBox.append(createOption("Text Color", textColor))
	mainBox.append(createOption("Text Outline", textOutline))
	mainBox.append(createOption("Outline Color", outlineColor))
	mainBox.append(createOption("Outline Width", outlineWidth))
	mainBox.append(createOption("Text Shadow", textShadow))
	mainBox.append(createOption("Shadow Color", shadowColor))

	buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
	buttonBox.set_halign(Gtk.Align.END)
	buttonBox.set_valign(Gtk.Align.START)
	buttonBox.set_margin_end(5)
	buttonBox.set_margin_top(5)

	quitButton = Gtk.Button(icon_name="window-close-symbolic")
	quitButton.set_size_request(20, 20)
	quitButton.set_hexpand(False)
	quitButton.set_vexpand(False)
	quitButton.add_css_class("destructive-action")
	quitButton.connect("clicked", lambda button: [status.success("Closed preferences dialog"), dialog.close()])

	buttonBox.append(quitButton)

	mainOverlay.set_child(mainBox)
	mainOverlay.add_overlay(buttonBox)

	handle = Gtk.WindowHandle()
	handle.set_child(mainOverlay)

	dialog.set_child(handle)
	dialog.present()
	status.success("Presented preferences dialog")

	status.info("Loading preferences...")
	padding.set_value(		config.readFromConfig("preferences.padding"))
	backgroundOpacity.set_value(	config.readFromConfig("preferences.backgroundOpacity"))
	fontSize.set_value(		config.readFromConfig("preferences.fontSize"))
	fontWeight.set_value(		config.readFromConfig("preferences.fontWeight"))
	textColor.set_rgba(		Gdk.RGBA(*config.readFromConfig("preferences.textColor")))
	textOutline.set_active(		config.readFromConfig("preferences.textOutline"))
	outlineColor.set_rgba(		Gdk.RGBA(*config.readFromConfig("preferences.outlineColor")))
	outlineWidth.set_value(		config.readFromConfig("preferences.outlineWidth"))
	textShadow.set_active(		config.readFromConfig("preferences.textShadow"))
	shadowColor.set_rgba(		Gdk.RGBA(*config.readFromConfig("preferences.shadowColor")))
	status.success("Loaded preferences")

	status.info("Registering real-time saving...")
	padding.connect("value-changed", lambda widget: 		saveConfig(widget, "preferences.padding", Gtk.SpinButton))
	backgroundOpacity.connect("value-changed", lambda widget: 	saveConfig(widget, "preferences.backgroundOpacity", Gtk.SpinButton))
	fontSize.connect("value-changed", lambda widget: 		saveConfig(widget, "preferences.fontSize", Gtk.SpinButton))
	fontWeight.connect("value-changed", lambda widget: 		saveConfig(widget, "preferences.fontWeight", Gtk.SpinButton))
	textColor.connect("notify::rgba", lambda widget, _: 		saveConfig(widget, "preferences.textColor", Gtk.ColorDialogButton))
	textOutline.connect("toggled", lambda widget: 			saveConfig(widget, "preferences.textOutline", Gtk.CheckButton))
	outlineColor.connect("notify::rgba", lambda widget, _:		saveConfig(widget, "preferences.outlineColor", Gtk.ColorDialogButton))
	outlineWidth.connect("value-changed", lambda widget: 		saveConfig(widget, "preferences.outlineWidth", Gtk.SpinButton))
	textShadow.connect("toggled", lambda widget: 			saveConfig(widget, "preferences.textShadow", Gtk.CheckButton))
	shadowColor.connect("notify::rgba", lambda widget, _: 		saveConfig(widget, "preferences.shadowColor", Gtk.ColorDialogButton))
	status.success("Registered real-time saving")

def onActivate(application):
	global startImage, startLabel
	window = Adw.ApplicationWindow(application=application)
	window.set_resizable(False)
	css = Gtk.CssProvider()
	css.load_from_data(b".colon { font-size: 40px; font-weight: 800; }")
	Gtk.StyleContext.add_provider_for_display(window.get_display(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

	mainOverlay = Gtk.Overlay()

	mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
	mainBox.set_margin_top(10)
	mainBox.set_margin_bottom(10)

	title = Gtk.Label(label="shaweelTimer")
	title.add_css_class("title-2")

	timeBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
	timeBox.set_halign(Gtk.Align.CENTER)
	def createSpinButton(min, max):
		spinButton = Gtk.SpinButton()
		spinButton.set_size_request(60, 120)
		spinButton.add_css_class("title-3")
		spinButton.set_orientation(Gtk.Orientation.VERTICAL)
		spinButton.set_range(min, max)
		spinButton.set_increments(1, 1)
		spinButton.set_digits(0)
		def formatButton(button):
			value = int(button.get_value())
			button.set_text(f"{value:02d}")
			return True

		spinButton.connect("output", formatButton)
		return spinButton

	def createColon():
		colon = Gtk.Label(label=":")
		colon.add_css_class("colon")
		return colon
		
	hoursSpinButton = createSpinButton(0, 23)
	minutesSpinButton = createSpinButton(0, 59)
	secondsSpinButton = createSpinButton(0, 59)

	timeBox.append(hoursSpinButton)
	timeBox.append(createColon())
	timeBox.append(minutesSpinButton)
	timeBox.append(createColon())
	timeBox.append(secondsSpinButton)

	startButton = Gtk.Button()
	startButtonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
	startButtonBox.set_halign(Gtk.Align.CENTER)
	startLabel = Gtk.Label(label="Start")
	startImage = Gtk.Image(icon_name="media-playback-start-symbolic")
	startButtonBox.append(startImage)
	startButtonBox.append(startLabel)
	startButton.set_hexpand(False)
	startButton.set_size_request(160, 0)
	startButton.set_halign(Gtk.Align.CENTER)
	startButton.set_child(startButtonBox)
	def onStartButtonClicked():
		global running
		if running:
			startLabel.set_label("Start")
			startImage.set_from_icon_name("media-playback-start-symbolic")
			stopTimer()
		else:
			startLabel.set_label("Stop")
			startImage.set_from_icon_name("media-playback-stop-symbolic")
			startTimer()

	startButton.connect("clicked", lambda _: onStartButtonClicked())
		
	mainBox.append(title)
	mainBox.append(timeBox)
	mainBox.append(startButton)

	buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
	buttonBox.set_halign(Gtk.Align.END)
	buttonBox.set_valign(Gtk.Align.START)
	buttonBox.set_margin_end(5)
	buttonBox.set_margin_top(5)

	quitButton = Gtk.Button(icon_name="window-close-symbolic")
	quitButton.set_size_request(20, 20)
	quitButton.set_hexpand(False)
	quitButton.set_vexpand(False)
	quitButton.add_css_class("destructive-action")
	quitButton.connect("clicked", lambda button: application.quit())

	preferencesButton = Gtk.Button(icon_name="preferences-system-symbolic")
	preferencesButton.set_size_request(20, 20)
	preferencesButton.set_hexpand(False)
	preferencesButton.set_vexpand(False)
	preferencesButton.connect("clicked", lambda button: openPreferences(button))

	buttonBox.append(preferencesButton)
	buttonBox.append(quitButton)

	mainOverlay.set_child(mainBox)
	mainOverlay.add_overlay(buttonBox)

	handle = Gtk.WindowHandle()
	handle.set_child(mainOverlay)

	window.set_content(handle)

	window.present()
	status.success("Presented libadwaita window")
	status.info("Loading last time...")
	hoursSpinButton.set_value(	config.readFromConfig("time.hours"))
	minutesSpinButton.set_value(	config.readFromConfig("time.minutes"))
	secondsSpinButton.set_value(	config.readFromConfig("time.seconds"))
	status.success("Loaded last time")
	status.info("Registering real-time saving...")
	hoursSpinButton.connect("value-changed", lambda widget:	saveConfig(widget, "time.hours", Gtk.SpinButton))
	minutesSpinButton.connect("value-changed", lambda widget:	saveConfig(widget, "time.minutes", Gtk.SpinButton))
	secondsSpinButton.connect("value-changed", lambda widget:	saveConfig(widget, "time.seconds", Gtk.SpinButton))
	status.success("Registered real-time saving")

application = Adw.Application()
application.connect("activate", onActivate)
application.run()
status.success(("Application quit"))