# ⚡ Execution Checklist (Operational)

Standard operating procedures for running and maintaining CognitiveHub-AI.

## 1. Daily Operations
- [ ] **Health Monitoring**: Check status of API Gateway and core AI services.
- [ ] **OpenAI Credit Check**: Verify API usage and remaining credits.
- [ ] **Workflow Monitoring**: Review all "Failed" or "Stalled" workflows in the dashboard.
- [ ] **Log Review**: Scan for any recurring 5xx errors or service timeouts.

## 2. Environment Management
- [ ] **Variable Sync**: Ensure `.env` files are consistent across developer machines.
- [ ] **Service Discovery**: Verify inter-service URLs in the API Gateway are correct.
- [ ] **Port Conflicts**: Check that local ports (8000-8007, 5432, 6379, etc.) are available.

## 3. Maintenance Tasks
- [ ] **Redis Flush**: Clear expired cache data if performance degrades.
- [ ] **Qdrant Indexing**: Periodically re-index core knowledge documents if accuracy drops.
- [ ] **Database Vacuum**: Run maintenance on PostgreSQL to optimize storage.

## 4. Emergency Procedures
- [ ] **Service Kill Switch**: Document how to manually stop a runaway AI workflow.
- [ ] **Rollback**: Identify the latest stable Git hash for immediate deployment rollback.
- [ ] **Secret Rotation**: Procedure for updating tokens if a leak is suspected.
