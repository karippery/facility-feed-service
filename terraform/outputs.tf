output "feed_bucket_name" {
  value = module.s3_feed_bucket.bucket_name
}

output "ecr_repository_url" {
  value = module.ecs_service.ecr_repository_url
}

output "ecs_cluster_name" {
  value = module.ecs_service.ecs_cluster_name
}

output "ecs_task_definition_arn" {
  value = module.ecs_service.ecs_task_definition_arn
}

output "cloudwatch_event_rule_arn" {
  value = module.ecs_service.cloudwatch_event_rule_arn
}