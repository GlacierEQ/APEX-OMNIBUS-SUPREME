.PHONY: apex-supreme apex-test apex-monitor apex-health apex-destroy

# 🏛️ APEX OMNIBUS SUPREME - Master Commands

apex-supreme:
	@echo "🏛️  DEPLOYING APEX OMNIBUS SUPREME..."
	@echo ""
	@python deploy/apex_deploy.py
	@echo ""
	@echo "🎊 APEX OMNIBUS SUPREME: FULLY OPERATIONAL!"
	@echo ""
	@echo "📊 Access Points:"
	@echo "  • Supreme API:     http://localhost:8000"
	@echo "  • Memory Nexus:    http://localhost:8080"
	@echo "  • Orchestration:   http://localhost:9000"
	@echo "  • Memory Trinity:  http://localhost:8081"
	@echo "  • Omni Engine:     http://localhost:9100"
	@echo "  • SUPERLUMINAL:    http://localhost:9001"
	@echo "  • Neo4j Browser:   http://localhost:7474"
	@echo "  • Grafana:         http://localhost:3000"
	@echo "  • Prometheus:      http://localhost:9090"
	@echo ""
	@echo "🎯 Quick Commands:"
	@echo "  • Health check:    make apex-health"
	@echo "  • Run tests:       make apex-test"
	@echo "  • Open monitoring: make apex-monitor"
	apex-health:
	@echo "🏥 APEX System Health Check..."
	@curl -s http://localhost:8000/api/v1/health | jq
	@echo ""
	@echo "Memory Nexus:"
	@curl -s http://localhost:8080/health || echo "  ❌ Not responding"
	@echo ""
	@echo "Orchestration:"
	@curl -s http://localhost:9000/health || echo "  ❌ Not responding"
	@echo ""
	@echo "Neo4j:"
	@curl -s http://localhost:7474 > /dev/null && echo "  ✅ Operational" || echo "  ❌ Not responding"

apex-test:
	@echo "🧪 Running APEX Integration Tests..."
	@pytest tests/test_integration.py -v
	@echo ""
	@echo "⚡ Performance Tests (<300ms validation)..."
	@pytest tests/test_performance.py -v
	@echo ""
	@echo "🔍 Forensic Workflow Tests..."
	@pytest tests/test_forensic.py -v
	@echo ""
	@echo "✅ All tests completed!"

apex-monitor:
	@echo "📊 Opening monitoring dashboards..."
	@open http://localhost:3000 || xdg-open http://localhost:3000
	@echo "✅ Grafana dashboard opened"
	@echo "   Default login: admin/glaciereq2025"

apex-examples:
	@echo "💡 Running example workflows..."
	@echo ""
	@echo "1️⃣  Forensic Case Analysis:"
	@python examples/forensic_case.py
	@echo ""
	@echo "2️⃣  Memory Operations:"
	@python examples/memory_operations.py
	@echo ""
	@echo "3️⃣  External API Calls:"
	@python examples/external_apis.py

apex-destroy:
	@echo "⚠️  DESTROYING APEX OMNIBUS SUPREME..."
	@read -p "Are you sure? This will stop all services [y/N]: " confirm && \
		if [ "$$confirm" = "y" ]; then \
			docker-compose down -v; \
			echo "💥 APEX destroyed"; \
		else \
			echo "❌ Cancelled"; \
		fi

apex-logs:
	@echo "📜 APEX System Logs:"
	@docker-compose logs -f --tail=100

apex-restart:
	@echo "🔄 Restarting APEX OMNIBUS SUPREME..."
	@docker-compose restart
	@echo "✅ All services restarted"

# Quick memory operations
memory-add:
	@echo "💾 Adding memory to APEX..."
	@curl -X POST http://localhost:8000/api/v1/memory/add \
		-H "Content-Type: application/json" \
		-d '{"content":"$(CONTENT)","user_id":"$(USER)"}' | jq

memory-search:
	@echo "🔍 Searching APEX memory..."
	@curl -X POST http://localhost:8000/api/v1/memory/search \
		-H "Content-Type: application/json" \
		-d '{"query":"$(QUERY)","user_id":"$(USER)"}' | jq

# Forensic operations
forensic-analyze:
	@echo "🔬 Running forensic analysis..."
	@curl -X POST http://localhost:8000/api/v1/forensic/analyze \
		-H "Content-Type: application/json" \
		-d '{"case_id":"$(CASE_ID)"}' | jq

help:
	@echo "🏛️  APEX OMNIBUS SUPREME - Command Reference"
	@echo ""
	@echo "Deployment:"
	@echo "  make apex-supreme     Deploy entire APEX stack"
	@echo "  make apex-destroy     Destroy all APEX services"
	@echo "  make apex-restart     Restart all services"
	@echo ""
	@echo "Monitoring:"
	@echo "  make apex-health      Check system health"
	@echo "  make apex-monitor     Open Grafana dashboard"
	@echo "  make apex-logs        View system logs"
	@echo ""
	@echo "Testing:"
	@echo "  make apex-test        Run all tests"
	@echo "  make apex-examples    Run example workflows"
	@echo ""
	@echo "Operations:"
	@echo "  make memory-add CONTENT='...' USER='...'    Add memory"
	@echo "  make memory-search QUERY='...' USER='...'   Search memory"
	@echo "  make forensic-analyze CASE_ID='...'         Analyze case"
