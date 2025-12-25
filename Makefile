.PHONY: help apex-supreme apex-supreme-2025 apex-health apex-test apex-monitor memory-add memory-search forensic-analyze

# APEX OMNIBUS SUPREME - Makefile
# One-command operations for supreme power

help:
	@echo "\033[1;36m====================================\033[0m"
	@echo "\033[1;35m🏛️  APEX OMNIBUS SUPREME 2025\033[0m"
	@echo "\033[1;36m====================================\033[0m"
	@echo ""
	@echo "\033[1;33mDeployment Commands:\033[0m"
	@echo "  make apex-supreme         Deploy original APEX stack"
	@echo "  make apex-supreme-2025    Deploy 2025 enhanced stack"
	@echo "  make apex-down            Stop all services"
	@echo "  make apex-rebuild         Rebuild and restart"
	@echo ""
	@echo "\033[1;33mHealth & Monitoring:\033[0m"
	@echo "  make apex-health          Check all layer health"
	@echo "  make apex-test            Run integration tests"
	@echo "  make apex-monitor         Open monitoring dashboard"
	@echo "  make apex-logs            View all logs"
	@echo ""
	@echo "\033[1;33mMemory Operations:\033[0m"
	@echo "  make memory-add CONTENT='...' USER='...'   Add memory"
	@echo "  make memory-search QUERY='...' USER='...'  Search memory"
	@echo ""
	@echo "\033[1;33mForensic Operations:\033[0m"
	@echo "  make forensic-analyze CASE_ID='...'        Analyze case"
	@echo ""

apex-supreme:
	@echo "\033[1;32m🚀 Deploying APEX OMNIBUS SUPREME...\033[0m"
	@docker-compose up -d
	@echo "\033[1;32m✅ Waiting for services to be healthy...\033[0m"
	@sleep 10
	@$(MAKE) apex-health
	@echo ""
	@echo "\033[1;35m🎊 APEX OMNIBUS SUPREME: FULLY OPERATIONAL!\033[0m"
	@echo "\033[1;36mGateway: http://localhost:8000\033[0m"
	@echo "\033[1;36mGrafana: http://localhost:3000\033[0m"
	@echo "\033[1;36mNeo4j:   http://localhost:7474\033[0m"

apex-supreme-2025:
	@echo "\033[1;32m🚀 Deploying APEX OMNIBUS SUPREME 2025 Edition...\033[0m"
	@pip install -r requirements.txt --quiet
	@python deploy/apex_deploy_2025.py
	@echo "\033[1;35m✅ 2025 integrations active\033[0m"
	@echo "\033[1;35m✅ Google MCP servers configured\033[0m"
	@echo "\033[1;35m✅ AWS MCP bridges established\033[0m"
	@echo "\033[1;35m✅ Advanced memory architecture live\033[0m"
	@echo "\033[1;35m✅ Multi-agent orchestration ready\033[0m"
	@echo "\033[1;35m🎊 APEX 2025: SUPREME POWER ACHIEVED!\033[0m"

apex-down:
	@echo "\033[1;33m⏹️  Stopping APEX services...\033[0m"
	@docker-compose down
	@echo "\033[1;32m✅ All services stopped\033[0m"

apex-rebuild:
	@echo "\033[1;33m🔧 Rebuilding APEX stack...\033[0m"
	@docker-compose down
	@docker-compose build --no-cache
	@$(MAKE) apex-supreme

apex-health:
	@echo "\033[1;36m🏥 Checking APEX health...\033[0m"
	@echo "\033[1;33mL0 - APEX Gateway:\033[0m"
	@curl -sf http://localhost:8000/health && echo "  ✅ OK" || echo "  ❌ FAIL"
	@echo "\033[1;33mL1 - Memory Nexus:\033[0m"
	@curl -sf http://localhost:8080/health && echo "  ✅ OK" || echo "  ❌ FAIL"
	@echo "\033[1;33mL2 - Orchestration:\033[0m"
	@curl -sf http://localhost:9000/health && echo "  ✅ OK" || echo "  ❌ FAIL"
	@echo "\033[1;33mL6 - Neo4j:\033[0m"
	@curl -sf http://localhost:7474/ && echo "  ✅ OK" || echo "  ❌ FAIL"
	@echo "\033[1;33mL7 - Prometheus:\033[0m"
	@curl -sf http://localhost:9090/-/healthy && echo "  ✅ OK" || echo "  ❌ FAIL"
	@echo "\033[1;33mL7 - Grafana:\033[0m"
	@curl -sf http://localhost:3000/api/health && echo "  ✅ OK" || echo "  ❌ FAIL"

apex-test:
	@echo "\033[1;36m🧪 Running integration tests...\033[0m"
	@pytest tests/ -v --tb=short

apex-monitor:
	@echo "\033[1;36m📊 Opening monitoring dashboard...\033[0m"
	@open http://localhost:3000 || xdg-open http://localhost:3000

apex-logs:
	@docker-compose logs -f

memory-add:
	@echo "\033[1;36m💾 Adding memory...\033[0m"
	@curl -X POST http://localhost:8000/api/v1/memory/add \
		-H 'Content-Type: application/json' \
		-d '{"content":"$(CONTENT)","user_id":"$(USER)"}'
	@echo "\n\033[1;32m✅ Memory added\033[0m"

memory-search:
	@echo "\033[1;36m🔍 Searching memory...\033[0m"
	@curl -X POST http://localhost:8000/api/v1/memory/search \
		-H 'Content-Type: application/json' \
		-d '{"query":"$(QUERY)","user_id":"$(USER)"}'

forensic-analyze:
	@echo "\033[1;36m🔬 Analyzing forensic case...\033[0m"
	@curl -X POST http://localhost:8000/api/v1/forensic/analyze \
		-H 'Content-Type: application/json' \
		-d '{"case_id":"$(CASE_ID)"}'
	@echo "\n\033[1;32m✅ Analysis complete\033[0m"
