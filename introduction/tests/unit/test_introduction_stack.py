import aws_cdk as core
import aws_cdk.assertions as assertions

from introduction.introduction_stack import IntroductionStack

# example tests. To run these tests, uncomment this file along with the example
# resource in introduction/introduction_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = IntroductionStack(app, "introduction")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
