from os import getenv

from time import time
from enum import Enum
from uuid import uuid4
from json import dumps

from logging import getLogger
from datetime import datetime

from boto3 import Session
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError


class Level(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

    def __str__(self):
        return self.name.lower()


class Stream(Enum):
    LOCAL = (1, False)
    MONGO = (2, True)
    LLM = (3, True)

    def __init__(self, value, cloud_watch):
        self._value_ = value
        self.cloud_watch = cloud_watch

    def __str__(self):
        return self.name.lower()


class Log:
    _instance_ = None

    def __new__(cls, *args, **kwargs):
        if cls._instance_ is None:
            cls._instance_ = super().__new__(cls)
        return cls._instance_

    def __init__(self):
        if not hasattr(self, '_init_'):
            self.logger = getLogger("uvicorn")

            self.aws_access_key_id = getenv('AWS_ACCESS_KEY_ID')
            self.aws_secret_access_key = getenv('AWS_SECRET_ACCESS_KEY')
            self.aws_session_token = getenv('AWS_SESSION_TOKEN')
            self.aws_region = 'us-east-1'

            self.session = None

            self.cloud_watch = None
            self.cloud_watch_group = "narrify"

            self.id = uuid4()
            self.today = datetime.now().strftime("%Y-%m-%d")

            self._init_ = True
            self._init_cloud_watch()

    def _check_aws_credentials(self):
        try:
            self.session = Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                aws_session_token=self.aws_session_token,
                region_name=self.aws_region
            )

            sts_client = self.session.client('sts')
            identity = sts_client.get_caller_identity()

            self.logger.info(f"AWS Ready: {identity['Account']}")
            return True
        except NoCredentialsError:
            self.logger.error("AWS is not SET: No credentials")
            return False
        except PartialCredentialsError:
            self.logger.error("AWS is not SET: Partial credentials")
            return False
        except Exception as error:
            self.logger.error(f"AWS is not SET: {error}")
            return False

    def _init_cloud_watch(self):
        if not self._check_aws_credentials():
            self.logger.error("CloudWatch is not SET.")
            return

        try:
            self.cloud_watch = self.session.client('logs')

            try:
                self.cloud_watch.create_log_group(logGroupName=self.cloud_watch_group)
                self.logger.info(f"CloudWatch Group: {self.cloud_watch_group}")
            except ClientError as error:
                if error.response['Error']['Code'] == 'ResourceAlreadyExistsException':
                    self.logger.info(f"CloudWatch Group: {self.cloud_watch_group}")
                else:
                    raise

            try:
                self.cloud_watch.create_log_stream(
                    logGroupName=self.cloud_watch_group,
                    logStreamName=f"g/{self.today}/{self.id}"
                )
                self.logger.info(f"CloudWatch Stream: g/{self.today}/{self.id}")
            except ClientError as error:
                if error.response['Error']['Code'] == 'ResourceAlreadyExistsException':
                    self.logger.info(f"CloudWatch Stream: g/{self.today}/{self.id}")
                else:
                    pass

            self.logger.info("CloudWatch Ready")
        except Exception as error:
            self.logger.error(f"CloudWatch is not SET: {error}")

    def _send_to_cloud_watch(self, *detail: str, level: Level = Level.INFO, stream: Stream = Stream.LOCAL):
        self.cloud_watch.put_log_events(
            logGroupName=self.cloud_watch_group,
            logStreamName=f"g/{self.today}/{self.id}",
            logEvents=[
                {
                    'timestamp': int(time() * 1000),
                    "message": dumps({
                        "level": str(level),
                        "stream": str(stream),
                        "detail": detail
                    })
                }
            ]
        )

    def log(self, *message: str, level: Level = Level.INFO, stream: Stream = Stream.LOCAL):
        if self.cloud_watch and stream.cloud_watch:
            self._send_to_cloud_watch(*message, level=level, stream=stream)

        if level == Level.WARNING:
            self.logger.warning(f"({stream}) {message}")
        elif level == Level.ERROR:
            self.logger.error(f"({stream}) {message}")
        elif level == Level.CRITICAL:
            self.logger.critical(f"({stream}) {message}")
        else:
            self.logger.info(f"({stream}) {message}")

    def info(self, *message: str, stream: Stream = Stream.LOCAL):
        self.log(*message, level=Level.INFO, stream=stream)

    def warning(self, *message: str, stream: Stream = Stream.LOCAL):
        self.log(*message, level=Level.WARNING, stream=stream)

    def error(self, *message: str, stream: Stream = Stream.LOCAL):
        self.log(*message, level=Level.ERROR, stream=stream)

    def critical(self, *message: str, stream: Stream = Stream.LOCAL):
        self.log(*message, level=Level.CRITICAL, stream=stream)


log = Log()
