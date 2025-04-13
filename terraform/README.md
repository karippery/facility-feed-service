
# Terraform Infrastructure for Django Feed Generator

## 📁 Directory Structure
```
terraform/
├── modules/          # Reusable components
│   ├── ecs/          # ECS Fargate configuration
│   ├── s3/           # S3 bucket for feed storage
│   └── iam/          # IAM roles and policies
├── main.tf           # Primary configuration
├── variables.tf      # Input variables
├── outputs.tf        # Output values
├── backend.tf        # Remote state configuration
```

## 🚀 What This Terraform Does

This infrastructure automates the deployment of:
- **S3 Bucket**: Stores generated JSON feed files and metadata
- **ECR Repository**: Hosts your Docker container images
- **ECS Fargate Cluster**: Runs your feed generator as a scheduled task
- **IAM Roles**: Secure permissions for the ECS task
- **CloudWatch Event**: Triggers the task on a schedule (cron)

## 🛠️ Prerequisites

1. **AWS Account** with proper permissions
2. **AWS CLI** configured (`aws configure`)
3. **Terraform** installed (v1.0+)
4. **Docker** installed (for building/pushing images)

## 🔧 Configuration

### 1. Mandatory Adjustments

Edit these files before first deploy:

**`variables.tf`**:
```hcl
variable "db_secret_arn" {
  description = "ARN of your database secret in AWS Secrets Manager"
  type        = string
  default     = "arn:aws:secretsmanager:us-east-1:123456789:secret:your-db-secret" # REPLACE ME
}
```

**`modules/ecs/main.tf`** (around line 80):
```hcl
network_configuration {
  subnets         = ["subnet-12345678"] # Replace with your private subnets
  security_groups = ["sg-12345678"]     # Replace with your security group
}
```

### 2. Optional Adjustments

**Schedule** (in `variables.tf`):
```hcl
variable "schedule_expression" {
  default = "cron(0 12 * * ? *)" # Runs daily at noon UTC
}
```

**Resource Sizing** (in `variables.tf`):
```hcl
variable "ecs_cpu" {
  default = 512 # 0.5 vCPU
}
variable "ecs_memory" {
  default = 1024 # 1GB RAM
}
```

## 🏃‍♂️ How To Run

### First-Time Setup
```bash
# Initialize Terraform and plugins
terraform init

# Review execution plan
terraform plan
```

### Deploy Infrastructure
```bash
# Apply configuration (will prompt for confirmation)
terraform apply

# Auto-approve (for CI/CD)
terraform apply -auto-approve
```

### Destroy Infrastructure
```bash
# Tear down all resources
terraform destroy
```

## 🔄 CI/CD Integration

1. Add these secrets to your GitHub repository:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION`

2. Example GitHub Actions workflow:
```yaml
- name: Terraform Apply
  run: terraform apply -auto-approve
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

## 🔐 Security Notes

1. **Never commit**:
   - AWS credentials
   - Terraform state files (`*.tfstate`)
   - `.env` files

2. Required permissions:
   - IAM, ECS, S3, ECR, CloudWatch full access
   - SecretsManager read access for DB credentials

## 💡 Troubleshooting

**Error: "Invalid credentials"**
- Run `aws configure` to refresh credentials
- Verify IAM user has proper permissions

**Error: "Subnet not found"**
- Update subnet IDs in `modules/ecs/main.tf`

**View logs**:
```bash
aws logs tail /ecs/django-feed-generator --follow
```

## 📝 Outputs After Deployment

After successful `apply`, you'll get:
- S3 Bucket name for feed storage
- ECR Repository URL for Docker pushes
- ECS Cluster name
- CloudWatch Event rule ARN

Access these later with:
```bash
terraform output
```