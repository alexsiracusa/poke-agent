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

check-git:
	@echo -e "\033[34m[INFO]\033[0m Checking for git..."
	@if ! command -v git >/dev/null 2>&1; then \
		echo -e "\033[31m[ERROR]\033[0m git not found. Please install git first."; \
		exit 1; \
	else \
		echo -e "\033[32m[SUCCESS]\033[0m git found"; \
	fi

create-venv:
	@if [ ! -d ".venv" ]; then \
		echo -e "\033[33m[SETUP]\033[0m Creating virtual environment..."; \
		uv venv; \
		echo -e "\033[32m[SUCCESS]\033[0m Virtual environment created"; \
	fi

install-deps: check-uv check-git create-venv
	@echo -e "\033[34m[INFO]\033[0m Downloading submodules..."
	@git submodule update --init --recursive --progress --verbose
	@echo -e "\033[34m[INFO]\033[0m Installing Python dependencies..."
	@uv pip install -e .[dev]
	@echo -e "\033[32m[SUCCESS]\033[0m Python dependencies installed"

start-server:
	@echo -e "\033[34m[INFO]\033[0m Starting Pokemon Showdown server in background..."
	@if pgrep -f "node.*pokemon-showdown" >/dev/null 2>&1; then \
		echo -e "\033[33m[WARNING]\033[0m Server is already running"; \
		exit 0; \
	fi
	@echo -e "\033[34m[INFO]\033[0m Creating required directories..."
	@mkdir -p modules/pokemon-showdown/logs/repl
	@cd modules/pokemon-showdown && npm install
	@echo -e "\033[33m[SETUP]\033[0m Launching server as background process..."
	@cd modules/pokemon-showdown && nohup node pokemon-showdown start --no-security > showdown.log 2>&1 &
	@sleep 3
	@if pgrep -f "node.*pokemon-showdown" >/dev/null 2>&1; then \
		echo -e "\033[32m[SUCCESS]\033[0m Server started in background"; \
	else \
		echo -e "\033[31m[ERROR]\033[0m Failed to start server - check logs"; \
		exit 1; \
	fi
	@echo -e "\033[34m[INFO]\033[0m Server logs available at: modules/pokemon-showdown/showdown.log"
	@echo -e "\033[34m[INFO]\033[0m Test your server at http://localhost:8000"

stop-server:
	@echo -e "\033[34m[INFO]\033[0m Stopping Pokemon Showdown server..."
	@if pgrep -f "pokemon-showdown" >/dev/null 2>&1; then \
		pkill -f "pokemon-showdown"; \
		echo -e "\033[32m[SUCCESS]\033[0m Server stopped"; \
	else \
		echo -e "\033[33m[WARNING]\033[0m Server is not running"; \
	fi

server-status:
	@echo -e "\033[34m[INFO]\033[0m Checking Pokemon Showdown server status..."
	@if pgrep -f "pokemon-showdown" >/dev/null 2>&1; then \
		echo -e "\033[32m[RUNNING]\033[0m Server is running"; \
		echo -e "\033[34m[INFO]\033[0m Server available at http://localhost:8000"; \
	else \
		echo -e "\033[31m[STOPPED]\033[0m Server is not running"; \
	fi

restart-server: stop-server start-server
	@echo -e "\033[32m[SUCCESS]\033[0m Server restarted successfully"

server-logs:
	@echo -e "\033[34m[INFO]\033[0m Showing Pokemon Showdown server logs..."
	@if [ -f "modules/pokemon-showdown/showdown.log" ]; then \
		tail -f modules/pokemon-showdown/showdown.log; \
	else \
		echo -e "\033[33m[WARNING]\033[0m No log file found"; \
	fi

clean-logs:
	@echo -e "\033[34m[INFO]\033[0m Cleaning Pokemon Showdown logs..."
	@rm -f modules/pokemon-showdown/showdown.log
	@rm -rf modules/pokemon-showdown/logs/repl/*
	@echo -e "\033[32m[SUCCESS]\033[0m Logs cleaned"