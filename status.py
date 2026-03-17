import gi, pathlib
gi.require_version('Adw', '1')
from gi.repository import Adw, Gio, GLib, Gtk

BOLD_RED = '\033[1;31m'
RED = "\033[31m"
YELLOW = '\033[33m'
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"

def noAlwaysOnTopWarning():
	file = pathlib.Path.home() / ".config" / "shaweelTimer" / ".noAlwaysOnTopWarning"
	file.parent.mkdir(parents=True, exist_ok=True)
	file.touch()

DIALOG_TYPES = {
	"fatal": {
		"title": "Fatal Error",
		"responses": ["Terminate"],
		"responseAppearance": Adw.ResponseAppearance.DESTRUCTIVE,
		"responseActions": [lambda: exit(1)]
	},

	"error": {
		"title": "Error",
		"responses": ["Close"],
		"responseAppearance": Adw.ResponseAppearance.DEFAULT,
		"responseActions": [None]
	},

	"warn": {
		"title": "Warning",
		"responses": ["Close", "Do not show again"],
		"responseAppearance": Adw.ResponseAppearance.DEFAULT,
		"responseActions": [None, lambda: noAlwaysOnTopWarning()]
	},

	"done": {
		"title": "Done",
		"responses": ["Close"],
		"responseAppearance": Adw.ResponseAppearance.DEFAULT,
		"responseActions": [None]
	}
}

def showDialog(type, message):
	if not type in DIALOG_TYPES.keys(): 
		print(f"{BOLD_RED}[FATAL]{RESET} invalid dialog type: {type}.\n Available dialog types: {', '.join(DIALOG_TYPES.keys())}")
		exit(1)
	dialogType = DIALOG_TYPES[type]
	dialog = Adw.AlertDialog(heading=dialogType["title"], body=message)
	if len(dialogType["responses"]) > 1:
		dialog.set_size_request(450, 0)
	css = Gtk.CssProvider()
	css.load_from_data(f"dialog {{ background-color: alpha(@window_bg_color, 1); border-radius: 12px; }}")
	Gtk.StyleContext.add_provider_for_display(dialog.get_display(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
	for response in dialogType["responses"]: 
		dialog.add_response(response, response)
		dialog.set_response_appearance(response, dialogType["responseAppearance"])
	
	def onResponse(d, response):
		index = 0
		for response2 in dialogType["responses"]: 
			if response == response2: break
			index += 1
		
		if not dialogType["responseActions"][index]: return
		dialogType["responseActions"][index]()
	dialog.connect("response", onResponse)

	
	application = Gio.Application.get_default()
	def runHeadless():
		Adw.init()
		loop = GLib.MainLoop()
		dialog.connect("response", lambda d, r: loop.quit())
		dialog.present()
		loop.run()

	if not application:
		runHeadless()
		return
	
	window = application.get_active_window()
	if window:
		loop = GLib.MainLoop()
		dialog.connect("response", lambda d, r: loop.quit())
		dialog.present(window)
		loop.run()
	else:
		runHeadless()
		return


def success(message):
	print(f"{GREEN}[SUCCESS]{RESET} {message}")

def info(message):
	print(f"{CYAN}[INFO]{RESET} {message}")

def warn(message, dialog=False):
	print(f"{YELLOW}[WARNING]{RESET} {message}")
	if dialog: showDialog("warn", message)

def error(message):
	print(f"{RED}[ERROR]{RESET} {message}")
	showDialog("error", message)

def fatal(message):
	print(f"{BOLD_RED}[FATAL]{RESET} {message}")
	showDialog("fatal", message)