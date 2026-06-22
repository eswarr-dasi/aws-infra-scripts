# ☁️ aws-infra-scripts

> **Project 9 of 10** · [30-Day Dev Roadmap](https://github.com/eswarr-dasi/dev-project-roadmap) · Jul 15, 2026
>
> A collection of **Python + Boto3** scripts to automate common AWS infrastructure tasks: EC2 management,
> S3 lifecycle policies, VPC security-group auditing, and cost reporting.
>
> ---
>
> ## ✨ Scripts
>
> | Script | Description |
> |--------|-------------|
> | `ec2_manager.py` | Start/stop/list EC2 instances by tag; find untagged instances |
> | `s3_lifecycle.py` | Apply/update lifecycle policies: transition to IA, Glacier, delete |
> | `sg_auditor.py` | Audit VPC security groups for overly permissive rules (0.0.0.0/0) |
> | `cost_reporter.py` | Pull Cost Explorer data, generate per-service cost report |
> | `snapshot_cleanup.py` | Find and delete orphaned EBS snapshots older than N days |
> | `unused_eip.py` | Identify and release unattached Elastic IPs |
>
> ---
>
> ## 🛠️ Tech Stack
>
> | Layer | Technology |
> |-------|------------|
> | Language | Python 3.12 |
> | AWS SDK | Boto3 |
> | CLI | Click |
> | Config | YAML / environment variables |
> | Testing | pytest + moto (AWS mocks) |
>
> ---
>
> ## 🚀 Usage
>
> ### Prerequisites
> ```bash
> pip install -r requirements.txt
> aws configure  # or set AWS_PROFILE / environment vars
> ```
>
> ### EC2 Manager
> ```bash
> # List all running instances
> python ec2_manager.py list --state running
>
> # Stop instances by tag
> python ec2_manager.py stop --tag Environment=staging
>
> # Find untagged instances
> python ec2_manager.py untagged
> ```
>
> ### Security Group Auditor
> ```bash
> # Audit all VPCs for open ingress rules
> python sg_auditor.py audit --region us-east-1
>
> # Output as JSON report
> python sg_auditor.py audit --output json > sg-report.json
> ```
>
> ### Cost Reporter
> ```bash
> # Last 30 days, grouped by service
> python cost_reporter.py report --days 30 --group-by SERVICE
>
> # Compare this month vs last month
> python cost_reporter.py compare
> ```
>
> ---
>
> ## 📝 Sample Output: Security Group Audit
>
> ```
> ⚠️  Security Group Audit Report — us-east-1
> 🔴 HIGH RISK (open to 0.0.0.0/0):
>   sg-0abc123 (prod-web): port 22 (SSH) open to internet
>   sg-0def456 (legacy-db): port 3306 (MySQL) open to internet
>
> ⚠️  MEDIUM RISK:
>   sg-0ghi789 (api-servers): port range 8000-9000 open to 0.0.0.0/0
>
> ✅ 2/5 security groups are correctly restricted
> ```
>
> ---
>
> ## 🧪 Testing
>
> ```bash
> pytest
> ```
>
> Tests use `moto` to mock AWS API calls — no real AWS account needed.
>
> ---
>
> ## 🎯 Career Relevance
>
> Codeifies the AWS (EC2, S3, VPC, Security Groups) experience from my time at MTek Solutions into
> portable, reusable automation scripts. Cloud automation skills are directly valued for any cloud-adjacent
> engineering or DevOps role.
>
> ---
>
> ## 📅 Part of the 30-Day Dev Challenge
>
> See the full roadmap: [dev-project-roadmap](https://github.com/eswarr-dasi/dev-project-roadmap)
>
> *Built by [Eswarr Dasi](https://github.com/eswarr-dasi) · Jul 2026*
