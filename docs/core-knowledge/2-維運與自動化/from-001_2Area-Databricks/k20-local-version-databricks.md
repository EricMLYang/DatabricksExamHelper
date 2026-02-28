---
tags:
  - databricks
---
# Local Version Databricks

## \[ Concept \] 

### Breakdown Databricks:

1. **Apache Spark**: The distributed computing engine that powers data processing in Databricks, enabling parallel computation across clusters.

2. **Delta Lake**: The storage layer that brings ACID transactions, schema enforcement, and versioning to your data lakes.

3. **Cloud Storage**: Underlying storage systems like Azure Blob Storage, AWS S3, or Google Cloud Storage that physically store your data files.

4. **Pipeline Mechanism**: Components for orchestrating data workflows, which include:

   - Databricks Jobs for scheduling and monitoring

   - Databricks Workflows for creating DAG-based pipelines

   - Integration with external orchestrators like Azure Data Factory or Apache Airflow

5. **Distributed Management**: Tools for managing compute resources:

   - Cluster management and auto-scaling

   - Job scheduling and distribution

   - Pool management for resource sharing

6. **Additional Components**:

   - **Workspace**: The collaborative environment where notebooks, dashboards, and ML experiments live

   - **Unity Catalog**: Centralized governance layer for data and AI assets

   - **MLflow**: For managing the machine learning lifecycle

   - **SQL Analytics**: For SQL-based analytics and dashboarding

   - **Repos**: Git integration for version control

   - **Security**: Fine-grained access controls, encryption, etc.



### Local Version:

When you're planning to recreate a minimal version locally, you'll need to focus on the core components (Spark + Delta Lake) while simplifying the distributed aspects to run on a single machine or small cluster.



### Delta Lake:

- Scala software that runs on machine

- but it's more than just something that deals with Parquet files. It's an open-source storage layer that brings ACID transactions, scalable metadata handling, and data versioning to data lakes. It works on top of existing storage systems like HDFS, S3, or local filesystems.


