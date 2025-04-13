resource "aws_ecr_repository" "service" {
  name = var.ecr_repository_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecs_cluster" "cluster" {
  name = "${var.service_name}-cluster-${var.environment}"
}

resource "aws_cloudwatch_log_group" "service_logs" {
  name = "/ecs/${var.service_name}-${var.environment}"
  retention_in_days = 30
}

resource "aws_ecs_task_definition" "service" {
  family                   = "${var.service_name}-${var.environment}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory
  execution_role_arn       = var.ecs_execution_role_arn
  task_role_arn            = var.ecs_task_role_arn

  container_definitions = jsonencode([{
    name      = var.service_name
    image     = "${aws_ecr_repository.service.repository_url}:latest"
    essential = true
    environment = [
      {
        name  = "ENVIRONMENT",
        value = var.environment
      },
      {
        name  = "FEED_BUCKET_NAME",
        value = var.feed_bucket_name
      }
    ]
    secrets = [
      {
        name      = "DB_CONNECTION_STRING",
        valueFrom = var.db_secret_arn
      }
    ]
    logConfiguration = {
      logDriver = "awslogs",
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.service_logs.name,
        "awslogs-region"        = var.aws_region,
        "awslogs-stream-prefix" = "ecs"
      }
    }
  }])
}

resource "aws_cloudwatch_event_rule" "scheduled_task" {
  name                = "${var.service_name}-scheduled-task-${var.environment}"
  description         = "Run ${var.service_name} on a schedule"
  schedule_expression = var.schedule_expression
}

resource "aws_cloudwatch_event_target" "scheduled_task" {
  rule      = aws_cloudwatch_event_rule.scheduled_task.name
  target_id = "${var.service_name}-target-${var.environment}"
  arn       = aws_ecs_cluster.cluster.arn
  role_arn  = var.ecs_execution_role_arn

  ecs_target {
    task_count          = 1
    task_definition_arn = aws_ecs_task_definition.service.arn
    launch_type         = "FARGATE"
    network_configuration {
      assign_public_ip = false 
      subnets         = ["subnet-12345678"] # Replace with your private subnets from VPC
      security_groups = ["sg-12345678"]     # Replace with your security group from EC2 section,security group
    }
  }
}