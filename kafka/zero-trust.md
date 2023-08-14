# Zero Trust with Kafka

Source: <https://engineering.grab.com/zero-trust-with-kafka>

**TL;DR**: Grab, the real-time data platform team, implemented a zero-trust security approach for their Kafka data streaming platform. They used mutual Transport Layer Security (mTLS) for authentication and encryption. Hashicorp Vault and its PKI engine were utilized to generate short-lived certificates for clients. Policy-Based Access Control (PBAC) and the Open Policy Agent (OPA) were chosen for authorization. Strimzi, the Kafka on Kubernetes operator, was leveraged to integrate mTLS and OPA with Kafka. The setup involved server authentication, client authentication, and an authorization process using OPA policies. The deployment was managed using Terraform, and a customized SDK was provided for client access. The security design resulted in a performance impact but significantly enhanced the platform's security.
