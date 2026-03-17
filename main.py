CYAN = "\033[36m"
RESET = "\033[0m"

print(f"{CYAN}--------------------------------{RESET}")
print(f"{CYAN}Currently in main.py{RESET}")
print(f"{CYAN}--------------------------------{RESET}")

import gi, status, config

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk, Gdk
status.info("Attempting to create and present libadwaita window")

def openPreferences(button: Gtk.Button):
	dialog = Adw.Dialog()
	css = Gtk.CssProvider()
	css.load_from_data(b".title-5 { font-size: 17px; font-weight: 650; }")
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

	def saveColor(widget, configPath):
		rgba = widget.get_rgba()
		config.writeToConfig(configPath, [rgba.get_red(), rgba.get_green(), rgba.get_blue(), rgba.get_alpha()])

	backgroundOpacity = Gtk.SpinButton()
	backgroundOpacity.set_range(0, 100)
	backgroundOpacity.set_increments(1, 1)
	backgroundOpacity.set_value(config.getFromConfig("preferences.backgroundOpacity"))
	backgroundOpacity.set_width_chars(5)
	def formatButton(button):
			value = int(button.get_value())
			button.set_text(f"{value}%")
			return True
	backgroundOpacity.connect("output", formatButton)
	backgroundOpacity.connect("changed", config.writeToConfig("preferences.backgroundOpacity", backgroundOpacity.get_value()))

	textSize = Gtk.SpinButton()
	textSize.set_range(8, 120)
	textSize.set_increments(1, 1)
	textSize.set_value(config.getFromConfig("preferences.textSize"))
	textSize.set_width_chars(4)
	textSize.connect("changed", config.writeToConfig("preferences.textSize", textSize.get_value()))

	textColor = Gtk.ColorDialogButton(dialog=Gtk.ColorDialog())
	textColor.set_rgba(Gdk.RGBA(*config.getFromConfig("preferences.textColor")))
	textColor.connect("changed", lambda widget: widget.saveColor(widget, "preferences.textColor"))

	textOutline = Gtk.CheckButton()
	textOutline.connect("toggled", lambda button: [
		outlineColor.set_sensitive(button.get_active()),
		outlineWidth.set_sensitive(button.get_active())
		])
	textOutline.set_active(config.getFromConfig("preferences.textOutline"))
	textOutline.connect("changed", config.writeToConfig("preferences.textOutline", textOutline.get_active()))

	outlineColor = Gtk.ColorDialogButton(dialog=Gtk.ColorDialog())
	outlineColor.set_rgba(Gdk.RGBA(*config.getFromConfig("preferences.outlineColor")))
	outlineColor.set_sensitive(textOutline.get_active())
	outlineColor.connect("changed", lambda widget: widget.saveColor(widget, "preferences.textColor"))

	outlineWidth = Gtk.SpinButton()
	outlineWidth.set_range(1, 20)
	outlineWidth.set_increments(1, 1)
	outlineWidth.set_value(config.getFromConfig("preferences.outlineWidth"))
	outlineWidth.set_sensitive(textOutline.get_active())
	outlineWidth.set_width_chars(3)

	textShadow = Gtk.CheckButton()
	textShadow.connect("toggled", lambda button: [
		shadowColor.set_sensitive(button.get_active()),
		])
	textShadow.set_active(config.getFromConfig("preferences.textShadow"))

	shadowColor = Gtk.ColorDialogButton(dialog=Gtk.ColorDialog())
	shadowColor.set_rgba(Gdk.RGBA(*config.getFromConfig("preferences.shadowColor")))
	shadowColor.set_sensitive(textShadow.get_active())

	mainBox.append(title)
	mainBox.append(createOption("Background Opacity", backgroundOpacity))
	mainBox.append(createOption("Text Size", textSize))
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


def onActivate(application):
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
		css = Gtk.CssProvider()
		css.load_from_data(b"label { font-size: 32px; }")
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
	startButtonBox.append(Gtk.Image(icon_name="media-playback-start-symbolic"))
	startButtonBox.append(Gtk.Label(label="Start"))
	startButton.set_hexpand(False)
	startButton.set_size_request(160, 0)
	startButton.set_halign(Gtk.Align.CENTER)
	startButton.set_child(startButtonBox)
		
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

application = Adw.Application()
application.connect("activate", onActivate)
application.run()
status.success(("Application quit"))