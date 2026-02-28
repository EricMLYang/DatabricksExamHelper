---
tags:
  - vms
---
# Databricks IaC & CI/CD

## 名詞解釋

- Infrastructure as Code (IaC): 用 code (  scripts, configuration files ...等)，定義、設定、管理基礎設施 (EX: servers, databases, networks ...等)，而不是透過 UI 介面手動調整。EX: 

   - Terraform

   - Pulumi

   - AWS CloudFormation

   - Azure Resource Manager (ARM) Templates 

- CI/CD Tools:  簡稱 CI/CD Automation Tools or DevOps Pipelines. EX: 

   - GitHub Actions

   - GitLab CI/CD

   - Azure DevOps Pipelines



## 觀念

- IaC, CI/CD 自動化，基本上都是針對基礎設施配置、專案佈署流程去進行流程撰寫、給參數、設定服務環境 ... 等， 所以原本手動流程熟的話比較好理解這些 Scripts 或 Configs，另一方面來說，理解完這些 Scripts，對於整個流程會有較全面的認知

- IaC 與 CD/CD Tools 最粗略的分別是，

   - IaC 主要是幫你啟動資源與配置:

      - 建立 VPC、子網路、安全群組等網路基礎設施

      - 啟動 EC2、RDS、S3、Lambda 等各種雲服務

      - 配置負載平衡器、DNS 記錄

      - 設定 IAM 角色和權限 建立 Kubernetes 叢集、容器服務

   - CD/CD Tools 是幫你把系統程式更新與佈署的自動化



## 目標工具簡述

### 1\. Databricks Asset Bundles

**特點**: Terraform 包裝版，專為 Databricks 資源管理設計
**配置檔**: `databricks.yml`

```yaml
bundle:
  name: my-project
resources:
  jobs:
    my_job:
      name: "ETL Pipeline"
      tasks:
        - task_key: "extract"
          notebook_task:
            notebook_path: "./notebooks/extract"
```

### 2\. Terraform

**特點**: 多雲和地端適用的基礎設施即代碼，支援多雲部署
**配置檔**: `main.tf`

```hcl
resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  
  tags = {
    Name = "WebServer"
  }
}
```

### 3\. GitHub Actions

**特點**: GitHub 生態系整合，可部署至任何平台
**配置檔**: `.github/workflows/deploy.yml`

```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to AWS
        run: aws s3 sync . s3://my-bucket
```

### 4\. Azure DevOps Pipelines

**特點**: 微軟生態系整合，支援多雲部署
**配置檔**: `azure-pipelines.yml`

```yaml
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: AzureCLI@2
  inputs:
    azureSubscription: 'my-subscription'
    scriptType: 'bash'
    scriptLocation: 'inlineScript'
    inlineScript: 'az webapp deploy --name myapp'
```



##  Terraform 

- A Terraform provider is a plugin for the Terraform tool that enables users to interact with specific APIs. In this case, the Terraform provider interacts with the Databricks REST API, allowing workspace administrators to automate the deployment of even the most complex data processing environments.

- Terraform Registry:

   - the **official public repository** of **Terraform modules, providers, and examples**, maintained by **HashiCorp**

   - Think of it like a package manager (like npm for Node.js or PyPI for Python), but for Terraform.

## Step

- Install Terraform CLI

- Import Terraform provider ( EX: Databricks Provider )

- Authenticate with Databricks

   - Using a workspace administrator username and password

   - Using a Databricks **Personal Access Token** (**PAT**)

   - Using the Azure CLI or Google Cloud CLI

   - If using the Azure cloud provider, using a service principal or managed service identity

   - Using the Databricks CLI (user-to-machine authentication)

- Storing authentication tokens that are used with Terraform

   - directly within the Terraform configuration file as a part of the Databricks provider import

   - on the local machine within a configuration file (recommend to avoid accidental exposure)

      - The easiest method for populating this configuration file is by using the Databricks CLI.



## Databricks Provider Example

### **Demo 1: Defining a DLT pipeline source notebook**

- Delta Live Tables (DLT) is a Databricks-managed framework for building reliable ETL pipelines on top of Delta Lake. It simplifies the process of:

   - Ingesting

   - Transforming

   - Validating

   - Managing data pipelines