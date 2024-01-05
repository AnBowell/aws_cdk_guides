from aws_cdk import (
    BundlingOptions,
    RemovalPolicy,
    Stack,
    aws_lambda,
    Duration,
    aws_s3 as s3,
    aws_events as events,
    aws_events_targets as targets,
)
from constructs import Construct


class IntroductionStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket_name = "dog-pics"

        dog_pic_bucket = s3.Bucket(
            scope=self,
            id="DogPicBucket",
            bucket_name=bucket_name,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            removal_policy=RemovalPolicy.RETAIN,
        )

        dog_lambda = aws_lambda.Function(
            self,
            "DogLambda",
            function_name="DogPictureDownloader",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            code=aws_lambda.Code.from_asset(
                "lambda_func",
                bundling=BundlingOptions(
                    image=aws_lambda.Runtime.PYTHON_3_11.bundling_image,
                    command=[
                        "bash",
                        "-c",
                        "pip install -r requirements.txt -t /asset-output && cp -r . /asset-output",
                    ],
                ),
            ),
            handler="index.handler",
            timeout=Duration.seconds(5),
            memory_size=128,
            environment={
                "AWS_BUCKET_NAME": bucket_name,
                "RANDOM_DOG_URL": "https://dog.ceo/api/breeds/image/random",
            },
        )

        # Give the lambda function permissions to write data to the bucket.
        dog_pic_bucket.grant_write(dog_lambda)

        dog_trigger = events.Rule(
            self,
            "DogTriggerSchedule",
            schedule=events.Schedule.rate(Duration.minutes(15)),
        )

        # Tell the EventBridge rule to trigger the lambda.
        dog_trigger.add_target(targets.LambdaFunction(dog_lambda))  # type: ignore
