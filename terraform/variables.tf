variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "service_name" {
  description = "Name of the service"
  type        = string
  default     = "django-feed-generator"
}

variable "feed_bucket_name" {
  description = "Name of the S3 bucket for feed storage"
  type        = string
  default     = "django-feed-generator-bucket"
}

variable "ecr_repository_name" {
  description = "Name of the ECR repository"
  type        = string
  default     = "django-feed-generator"
}

variable "db_secret_arn" {
  description = "ARN of the database secret in AWS Secrets Manager"
  type        = string
}

variable "schedule_expression" {
  description = "CloudWatch Events schedule expression for the ECS task"
  type        = string
  default     = "cron(0 12 * * ? *)" # Run daily at noon UTC
}

variable "ecs_cpu" {
  description = "CPU units for the ECS task"
  type        = number
  default     = 512 # 0.5 vCPU
}

variable "ecs_memory" {
  description = "Memory for the ECS task (MB)"
  type        = number
  default     = 1024 # 1GB
}