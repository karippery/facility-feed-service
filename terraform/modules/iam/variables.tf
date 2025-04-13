variable "ecs_task_role_name" {
  description = "Name of the ECS task role"
  type        = string
}

variable "ecs_execution_role_name" {
  description = "Name of the ECS execution role"
  type        = string
}

variable "feed_bucket_arn" {
  description = "ARN of the feed S3 bucket"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}