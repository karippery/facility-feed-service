resource "aws_s3_bucket" "feed_bucket" {
  bucket = "${var.bucket_name}-${var.environment}"
  force_destroy = var.environment == "dev" ? true : false
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.feed_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "encryption" {
  bucket = aws_s3_bucket.feed_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "block_public_access" {
  bucket = aws_s3_bucket.feed_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}