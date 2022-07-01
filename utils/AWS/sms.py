import boto3
from django.conf import settings

# sms = boto3.resource("sns",
#                      region_name='eu-central-1',
#                      aws_access_key_id=settings.AWS_ACCESS_KEY,
#                      aws_secret_access_key=settings.AWS_SECRET_KEY
#                      )
#
# class SnsWrapper:
#     """Encapsulates Amazon SNS topic and subscription functions."""
#     def __init__(self, sns_resource):
#         """
#         :param sns_resource: A Boto3 Amazon SNS resource.
#         """
#         self.sns_resource = sns_resource
#
#     def publish_text_message(self, phone_number, message):
#         """
#         Publishes a text message directly to a phone number without need for a
#         subscription.
#
#         :param phone_number: The phone number that receives the message. This must be
#                              in E.164 format. For example, a United States phone
#                              number might be +12065550101.
#         :param message: The message to send.
#         :return: The ID of the message.
#         """
#         try:
#             response = self.sns_resource.meta.client.publish(
#                 PhoneNumber=phone_number, Message=message)
#             message_id = response['MessageId']
#             #  logger.info("Published message to %s.", phone_number)
#         except ClientError:
#             # logger.exception("Couldn't publish message to %s.", phone_number)
#             raise
#         else:
#             return message_id
#
# sender = SnsWrapper(sms)

def send_sms_single(phone_num, tpl, code):
    client = boto3.client('sns',
                          region_name='eu-central-1',
                          aws_access_key_id=settings.AWS_ACCESS_KEY,
                          aws_secret_access_key=settings.AWS_SECRET_KEY
                          )


    response = client.publish(
        # TopicArn='arn:aws:sns:eu-central-1:437230381224:SAAS_System',
        #TargetArn='string',
        PhoneNumber='+49{}'.format(phone_num),
        Message='Welecome to use SAAS Management System, your {} code is: {}. The code will be invalid in 5 minutes.'.format(tpl, code[0]),
        Subject='string',
        MessageStructure='string',
        # MessageAttributes={
        #     'string': {
        #         'DataType': 'string',
        #         'StringValue': 'string',
        #         'BinaryValue': b'bytes'
        #     }
        # },
        # MessageDeduplicationId='string',
        # MessageGroupId='string'
    )

    return response
