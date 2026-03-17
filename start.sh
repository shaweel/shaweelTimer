RED="\e[31m"
GREEN="\e[32m"
CYAN="\e[36m"
RESET="\e[0m"
echo -e "${CYAN}--------------------------------${RESET}"
echo -e "${CYAN}Currently in start.sh${RESET}"
echo -e "${CYAN}--------------------------------${RESET}"

venvPip() {
	.venv/bin/pip "$@"
}

if ! command -v python3.14 &> /dev/null; then
	echo -e "${RED}Install ${CYAN}python3.14${RED} first.${RESET}"
	exit
fi
echo -e "${CYAN}python3.14${GREEN} is installed. Good.${RESET}"

if [ ! -d ".venv" ]; then
	echo -e "${CYAN}venv ${RED}doesn't exist, ${GREEN}creating.${RESET}"
	python3.14 -m venv .venv
else
	echo -e "${CYAN}venv ${GREEN}exists. Good.${RESET}"
fi

if .venv/bin/python -m pip list --outdated | grep -q pip; then
	echo -e "${CYAN}pip ${RED}is outdated, ${GREEN}updating.${RESET}"
	venvPip install --upgrade pip
else
	echo -e "${CYAN}pip ${GREEN}is up to date. Good.${RESET}"
fi

if ! .venv/bin/python -c "import gi" &> /dev/null; then
	echo -e "${CYAN}PyGObject ${RED}isn't installed in venv, ${GREEN}installing.${RESET}"
	venvPip install PyGObject
else
	echo -e "${CYAN}PyGObject ${GREEN}is installed in venv. Good.${RESET}"
fi

if .venv/bin/python -m pip list --outdated | grep -q PyGObject; then
	echo -e "${CYAN}PyGObject ${RED}is outdated, ${GREEN}updating.${RESET}"
	venvPip install --upgrade PyGObject
else
	echo -e "${CYAN}PyGObject ${GREEN}is up to date. Good.${RESET}"
fi


echo -e "${GREEN}Everything should be ready. Running ${CYAN}main.py.${RESET}"
.venv/bin/python main.py