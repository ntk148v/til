# Enterprise AI Infrastructure 101: From Proof of Concept to Production

Source:
- <https://youtu.be/9cDnHMIWsMQ>
- <https://www.onesourcecloud.net/blog/enterprise-ai-infrastructure-poc-to-production-4096b>

# 1. What makes it "enterprise"?

- Scale:
  - 100s-1000s of users.
  - 24/7 availability.
  - TB-PB data volumes.
- Integration:
  - Legacy systems.
  - Existing workflows.
  - Data governance.
- Compliance:
  - HiPAA, SOX, GDPR.
  - Industry regulations.
  - Audit requirements.
- Accountability:
  - Auditability.
  - Explainability.
  - Human oversight.

## 2. Architecture patterns

- Financial services:
  - Use cases:
    - Credit risk scoring.
    - Trading algorithms.
  - Architecture: hybrid (cloud: training, on-prem: inference).
  - Key drivers:
    - SOX compliance.
    - Low latency (<50ms).
    - Cost control.
- Healthcare:
  - Use cases:
    - Readmission risk.
    - Medical imaging.
    - Clinical decision support.
  - Architecture: on-prem (on-prem: everything, cloud research only)
  - Key drivers:
    - Patient privacy.
    - Data sovereignty.
    - HiPAA requirements.
- Manufacturing:
  - Use cases:
    - Predictive maintenance.
    - Quality defect detection.
    - Supply chain optimization.
    - Energy optimization.
  - Architecture:
    - Hybrid + edge (edge: factory floor, cloud training/analytics).
  - Key drivers:
    - Real-time control.
    - Cost efficiency.
    - Operational flexibility.

## 3. Kubernetes for AI Infrastructure

- Container orchestration:
  - Consistent deployments across environments.
  - Simplified dependency management.
- Abstraction layer:
  - Same code runs on AWS, Azure, GCP, on-prem.
  - Avoid vendor lock-in.
- Built for scale:
  - Auto-scaling, load balancing, self-healing.
  - Resource management (CPU, GPU, memory).
- Industry standard:
  - Large ecosystem, community support.
  - Integrates with ML tools (KubeFlow, KServe, MLflow)

## 4. Key Kubernetes concepts for AI workloads

- Nodes & node pools:
  - Physical/virtual machines.
  - CPU nodes vs GPU nodes.
  - Scale: 3-100+ nodes.
- Pods & deployments:
  - Container + resources.
  - Model serving instances.
  - replicas for redundancy.
- Service & ingress:
  - Endpoint for models.
  - Load balancing.
  - External access.
- Persistent volumes:
  - Model storage.
  - Training data.
  - Shared artifacts.

## 5. GPU vs CPU resource allocation

- Training workloads:
  - Always GPU (unless very small models)
  - 8-32 GPUs for production models.
  - Training on CPU takes weeks vs hours.
- Inference workloads:
  - Depends on model size, latency, cost.
- Use GPU when:
  - Large models (>1GB).
  - Real-time required.
  - High throughput needed.
  - < 100ms latency required.
- Use CPU when:
  - Small models (<100MB).
  - Batch processing Ok.
  - Cost-sensitive.
  - Occasional requests.

## 6. Multi-instance GPU (MIG) for Resource sharing

Harness the full power of a single NVIDIA A100 (80GB) GPU by dividing it into dedicated, isolated instances.

## 7. ML Tools landscape on Kubernetes

- Pipelines & orchestration:
  - KubeFlow.
  - Argo workflows.
  - Apache Airflow.
- Model serving:
  - KServe.
  - NVIDIA Triton.
  - TorchServe.
  - TensorFlow Serving.
- Experimental tracking & registry:
  - MLflow.
  - Weights & Biases.
  - DVC.
- Monitoring:
  - Prometheus + Grafana.
  - ELK stack.
  - DataDog.

## 8. Kubernetes Multi-tenancy

- Namespace.
- Resource quota.
- Role-based access control (RBAC).

## 9. Security & performance considerations

- Security isolation:
  - Network policies:
    - Prevent cross-namespace traffic.
    - Whitelist only required connections.
  - Pod security policies:
    - Prevent privileged containers.
    - Enforce security context.
  - Secrets management:
    - Namespace-scoped secrets.
    - External secret stores (vault).
- Noisy neighbor prevention:
  - Resource limits:
    - Hard enforcement to prevent resource hogging.
  - Quality of service (QoS):
    - Guaranteed (high priority).
    - Burstable (medium priority).
    - BestEffort (low priority).
  - GPU Time-slicing.
    - Ensures fair scheduling and prevents monopolization.
