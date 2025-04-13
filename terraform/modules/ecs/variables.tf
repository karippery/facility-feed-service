variable "service_name" {
  description = "Name of the service"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "ecr_repository_name" {
  description = "Name of the ECR repository"
  type        = string
}

variable "ecs_task_role_arn" {
  description = "ARN of the ECS task role"
  type        = string
}

variable "ecs_execution_role_arn" {
  description = "ARN of the ECS execution role"
  type        = string
}

variable "feed_bucket_name" {
  description = "Name of the feed S3 bucket"
  type        = string
}

variable "db_secret_arn" {
  description = "ARN of the database secret"
  type        = string
}

variable "schedule_expression" {
  description = "CloudWatch Events schedule expression"
  type        = string
}

variable "cpu" {
  description = "CPU units for the ECS task"
  type        = number
}

variable "memory" {
  description = "Memory for the ECS task (MB)"
  type        = number
}