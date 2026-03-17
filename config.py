import pathlib, json, status, gi
from gi.repository import Gdk
status.info("Initializing configuration")

configFolder = pathlib.Path.home() / ".config" / "shaweelTimer"
configFolder.mkdir(parents=True, exist_ok=True)

defaultConfig = {
	"time": {
		"hours": 0,
		"minutes": 0,
		"seconds": 30
	},
	"preferences": {
		"backgroundOpacity": 80,
		"fontSize": 40,
		"fontWeight": 900,
		"textColor": [1, 1, 1, 1],
		"textOutline": False,
		"outlineColor": [0, 0, 0, 1],
		"outlineWidth": 30,
		"textShadow": False,
		"shadowColor": [0, 0, 0, 1]
	}
}

def correctConfig(config, path):
	if config == {} and path == "":
		status.warn("No config found or config is corrupted. Creating new config from default")
		return defaultConfig
	
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
	return config

def saveConfig():
	configFile.write_text(json.dumps(config))

def getFullConfig():
	return config

def readFromConfig(path):
	pathArray = path.split(".")
	current = config
	for entry in pathArray[:-1]:
		current = current[entry]
	return current[pathArray[-1]]

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

config = correctConfig(config, "")
saveConfig()
status.success("Config saved")
