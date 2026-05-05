BACKEND_DIR := backend
FRONTEND_DIR := frontend
BACKEND_VENV_BIN := $(BACKEND_DIR)/.venv/bin

.PHONY: quality quality-backend quality-frontend test test-backend test-frontend

quality: quality-backend quality-frontend

quality-backend:
	cd $(BACKEND_DIR) && $(CURDIR)/$(BACKEND_VENV_BIN)/ruff check .
	cd $(BACKEND_DIR) && $(CURDIR)/$(BACKEND_VENV_BIN)/ruff format --check .

quality-frontend:
	cd $(FRONTEND_DIR) && npm run lint
	cd $(FRONTEND_DIR) && npm run format:check
	cd $(FRONTEND_DIR) && npm run typecheck

test: test-backend test-frontend

test-backend:
	cd $(BACKEND_DIR) && $(CURDIR)/$(BACKEND_VENV_BIN)/pytest

test-frontend:
	cd $(FRONTEND_DIR) && npm run test
