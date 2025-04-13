output "ecr_repository_url" {
  value = aws_ecr_repository.service.repository_url
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.cluster.name
}

output "ecs_task_definition_arn" {
  value = aws_ecs_task_definition.service.arn
}

output "cloudwatch_event_rule_arn" {
  value = aws_cloudwatch_event_rule.scheduled_task.arn
}