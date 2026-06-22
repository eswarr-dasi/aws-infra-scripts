#!/usr/bin/env python3
"""S3 bucket management scripts for common DevOps tasks."""

import click
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

s3 = boto3.client('s3')


@click.group()
def cli():
      """S3 management utilities."""
      pass


@cli.command()
@click.argument('bucket')
@click.option('--days', default=30, help='Files older than N days')
@click.option('--dry-run', is_flag=True, help='List files without deleting')
def cleanup(bucket, days, dry_run):
      """Clean up old files from S3 bucket."""
      cutoff = datetime.utcnow() - timedelta(days=days)
      paginator = s3.get_paginator('list_objects_v2')
      total_size = 0
      deleted = 0

    for page in paginator.paginate(Bucket=bucket):
              for obj in page.get('Contents', []):
                            if obj['LastModified'].replace(tzinfo=None) < cutoff:
                                              total_size += obj['Size']
                                              if dry_run:
                                                                    click.echo(f"Would delete: {obj['Key']} ({obj['Size']} bytes)")
                            else:
                                                  s3.delete_object(Bucket=bucket, Key=obj['Key'])
                                                  deleted += 1

                    action = 'Would delete' if dry_run else 'Deleted'
    click.echo(f"{action} {deleted} files, total {total_size / 1024 / 1024:.2f} MB")


@cli.command()
@click.argument('source-bucket')
@click.argument('dest-bucket')
@click.option('--prefix', default='', help='Key prefix to copy')
def sync(source_bucket, dest_bucket, prefix):
      """Sync objects between S3 buckets."""
    paginator = s3.get_paginator('list_objects_v2')
    copied = 0

    for page in paginator.paginate(Bucket=source_bucket, Prefix=prefix):
              for obj in page.get('Contents', []):
                            copy_source = {'Bucket': source_bucket, 'Key': obj['Key']}
                            try:
                                              s3.copy_object(
                                                                    CopySource=copy_source,
                                                                    Bucket=dest_bucket,
                                                                    Key=obj['Key']
                                              )
                                              copied += 1
                                              click.echo(f"Copied: {obj['Key']}")
except ClientError as e:
                click.echo(f"Error copying {obj['Key']}: {e}", err=True)

    click.echo(f"Sync complete. Copied {copied} objects.")


@cli.command()
@click.argument('bucket')
def check_public(bucket):
      """Check for publicly accessible objects in a bucket."""
    paginator = s3.get_paginator('list_objects_v2')
    public_count = 0

    for page in paginator.paginate(Bucket=bucket):
              for obj in page.get('Contents', []):
                            acl = s3.get_object_acl(Bucket=bucket, Key=obj['Key'])
                            for grant in acl['Grants']:
                                              grantee = grant['Grantee']
                                              if grantee.get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                                                                    click.secho(f"PUBLIC: {obj['Key']}", fg='red')
                                                                    public_count += 1

                                  if public_count == 0:
                                            click.secho("No public objects found.", fg='green')
else:
        click.secho(f"Found {public_count} public objects!", fg='red')


if __name__ == '__main__':
      cli()
