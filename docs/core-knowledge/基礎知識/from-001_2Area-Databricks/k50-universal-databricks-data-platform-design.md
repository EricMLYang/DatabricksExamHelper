---
tags:
  - data-platform
---
# Universal Databricks Data Platform Design

## \[ Purpose \]

A Universal Data Pipeline Architecture

Design a standardized data pipeline framework that can be rapidly deployed across different data platforms, specifically optimized for Azure and AWS cloud environments. This framework aims to:

- Provide a template-based approach for consistent data flow implementation

- Maintain platform agnosticity while leveraging cloud-specific optimizations

- Enable quick setup and deployment of core data processing workflows



## \[ Main Tools \]

- Compute

   - Analysis Flow: Databricks Cluster in Azure or AWS

   - Streaming:

      - AWS Kinesis + AWS Lambda

      - Azure EventHub + Azure Function

- Storage:

   - Data Governance: Delata Lake

   - Application: SQL Server, **PostgreSQL**, MySQL

   - Others: Azure Blog, AWS S3





## \[ Main Modules \]

- Repository

   - 參數化配置

   - 儲存抽象: Azure Blob, AWS S3

   - 串流抽象: Azure EventHub, AWS Kinesis Streaming

   - 運算函式庫

   - 流程模組間的溝通介面 ( 介面 = Function + Config )

      - 


