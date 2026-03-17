import gi
gi.require_version('Adw', '1')
from gi.repository import Adw, Gio, GLib

BOLD_RED = '\033[1;31m'
RED = "\033[31m"
YELLOW = '\033[33m'
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"

DIALOG_TYPES = {
	"fatal": {
		"title": "Fatal Error",
		"response": "Terminate",
		"responseAppearance": Adw.ResponseAppearance.DESTRUCTIVE,
		"responseAction": lambda: exit(1)
	},

	"error": {
		"title": "Error",
		"response": "Close",
		"responseAppearance": Adw.ResponseAppearance.DEFAULT,
		"responseAction": None
	}
}

def showDialog(type, message):
	if not type in DIALOG_TYPES.keys(): 
		print(f"{BOLD_RED}[FATAL]{RESET} invalid dialog type: {type}.\n Available dialog types: {', '.join(DIALOG_TYPES.keys())}")
		exit(1)
	dialogType = DIALOG_TYPES[type]
	dialog = Adw.AlertDialog(heading=dialogType["title"], body=message)
	dialog.add_response("response", dialogType["response"])
	dialog.set_response_appearance("response", dialogType["responseAppearance"])
	def onResponse(d, response):
		if not dialogType["responseAction"]: return
		dialogType["responseAction"]()
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
		dialog.present(window)
	else:
		runHeadless()
		return


def success(message):
	print(f"{GREEN}[SUCCESS]{RESET} {message}")

def info(message):
	print(f"{CYAN}[INFO]{RESET} {message}")

def warn(message):
	print(f"{YELLOW}[WARNING]{RESET} {message}")

def error(message):
	print(f"{RED}[ERROR]{RESET} {message}")
	showDialog("error", message)

def fatal(message):
	print(f"{BOLD_RED}[FATAL]{RESET} {message}")
	showDialog("fatal", message)