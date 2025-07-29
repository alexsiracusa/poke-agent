_command_exists cmd:
	@command -v {{cmd}} >/dev/null 2>&1

check-uv:
	@echo -e "\033[34m[INFO]\033[0m Checking for uv..."
	@if ! command -v uv >/dev/null 2>&1; then \
		echo -e "\033[31m[ERROR]\033[0m uv not found. Please install uv first."; \
		echo -e "\033[33m[HINT]\033[0m Install uv with: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
		exit 1; \
	else \
		echo -e "\033[32m[SUCCESS]\033[0m uv found"; \
	fi

create-venv:
	@if [ ! -d ".venv" ]; then \
		echo -e "\033[33m[SETUP]\033[0m Creating virtual environment..."; \
		uv venv; \
		echo -e "\033[32m[SUCCESS]\033[0m Virtual environment created"; \
	fi

install-deps: check-uv create-venv
	@echo -e "\033[34m[INFO]\033[0m Installing Python dependencies..."
	@uv pip install -e .[dev]
	@echo -e "\033[32m[SUCCESS]\033[0m Python dependencies installed"

start-server:
	@echo -e "\033[34m[INFO]\033[0m Starting Pokemon Showdown server in background..."
	@cd modules/pokemon-showdown && npm install
	@echo -e "\033[33m[SETUP]\033[0m Launching server in new terminal..."
	@osascript -e 'tell app "Terminal" to do script "cd \"{{justfile_directory()}}/modules/pokemon-showdown\" && node pokemon-showdown start --no-security"'
	@echo -e "\033[32m[SUCCESS]\033[0m Server started in new terminal window"

setup: start-server install-deps
	@echo -e "\033[32m[SUCCESS]\033[0m Setup complete!"
