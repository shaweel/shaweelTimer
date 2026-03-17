import pathlib, json, status, gi
from gi.repository import Gdk
status.info("Initializing configuration")

configFolder = pathlib.Path.home() / ".config" / "shaweelTimer"
configFolder.mkdir(parents=True, exist_ok=True)
#TODO ERROR HANDLING FOR NON-EXISTANT PATHS
defaultConfig = {
	"time": [0, 0, 30],
	"preferences": {
		"backgroundOpacity": 20,
		"textSize": 24,
		"textColor": [1, 1, 1, 1],
		"textOutline": False,
		"outlinecolor": [0, 0, 0, 1],
		"outlineWidth": 5,
		"textShadow": False,
		"shadowcolor": [0, 0, 0, 1]
	}
}

def correctConfig(config, path):
	if config == {} and path == "":
		status.warn("No config found or config is corrupted. Creating new config from default")
		config = defaultConfig
	
	if path == "": currentDefault = defaultConfig
	else: 
		pathArray = path.split(".")
		currentDefault = defaultConfig
		for entry in pathArray:
			currentDefault = currentDefault[entry]

	for key, value in currentDefault.items():
		if key not in config:
			default = {} if isinstance(value, dict) else value
			fullKey = f"{path}.{key}" if path != "" else key
			status.warn(f"No config key \"{fullKey}\", applying default: {default}")
			config[key] = default
		if isinstance(value, dict):
			fullKey = f"{path}.{key}" if path != "" else key
			correctConfig(config[key], fullKey)
	if path == "": status.success("Config fully corrected")

def saveConfig():
	configFile.write_text(json.dumps(config))
	status.success("Config saved")

def getFullConfig():
	return config

def getFromConfig(path):
	pathArray = path.split(".")
	current = config
	for entry in pathArray:
		current = current[entry]
	return current

def writeToConfig(path, value):
	pathArray = path.split(".")
	current = config
	for entry in pathArray[:-1]:
		current = current[entry]
	current[pathArray[-1]] = value
	status.success(f"Written {value} to {path}")
	saveConfig()

configFile = configFolder / "config.json"
configFile.touch()

try:
	config = json.loads(configFile.read_text())
except Exception as exception:
	status.warn(f"Failed to parse config: {exception}")
	config = {}

correctConfig(config, "")
saveConfig()
