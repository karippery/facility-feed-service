terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "s3_feed_bucket" {
  source = "./modules/s3"

  bucket_name = var.feed_bucket_name
  environment = var.environment
}

module "iam_roles" {
  source = "./modules/iam"

  ecs_task_role_name      = "${var.service_name}-ecs-task-role-${var.environment}"
  ecs_execution_role_name = "${var.service_name}-ecs-execution-role-${var.environment}"
  feed_bucket_arn         = module.s3_feed_bucket.bucket_arn
  environment             = var.environment
}

module "ecs_service" {
  source = "./modules/ecs"

  service_name          = var.service_name
  environment           = var.environment
  aws_region            = var.aws_region
  ecr_repository_name   = var.ecr_repository_name
  ecs_task_role_arn     = module.iam_roles.ecs_task_role_arn
  ecs_execution_role_arn = module.iam_roles.ecs_execution_role_arn
  feed_bucket_name      = module.s3_feed_bucket.bucket_name
  db_secret_arn         = var.db_secret_arn
  schedule_expression   = var.schedule_expression
  cpu                   = var.ecs_cpu
  memory                = var.ecs_memory
}