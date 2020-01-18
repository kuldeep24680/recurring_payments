
SANDBOX = "transaction-email.oracleproducts.com"
KEY = "c37ce326adfc744ff27f31dabaa7153d-0a4b0c40-49167757"
BUFFER_PERIOD = 5
MONGODB_SETTINGS = {
    "DB": "oracle-products-dev",
    "PORT": 27017,
    "HOST": "localhost",
    "connect": False,
}

AWS_SETTINGS = {
    "AWS_CDN_PATH": "s3.ap-south-1.amazonaws.com",
    "AWS_S3_BUCKET": "midland-test",
    "AWS_REGION": "ap-south-1",
    "AWS_COGNITO_ID": "ap-south-1:21f42969-f6bf-4f81-b673-1859223d9ba6",
    "AWS_COGNITO_PROVIDER_ID": "com.esthenos.midland",
    "AWS_ACCESS_KEY_ID": "AKIAIFWIECXTMBUKIJGA",
    "AWS_SECRET_ACCESS_KEY": "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",
}

AUTHORIZE_CREDENTIALS = {
    "api_login_name": "8HtWfmFw2k6j",
    "transaction_key": "9R65uL8D4dg6w9jK"
}

RABBIT_MQ_SERVER = "127.0.0.1"
RABBIT_MQ_PORT = "5672"

CELERY_SETTINGS = {
    "CELERY_broker_url": "amqp://oracle-tasks:oracle@{}:{}//oracle-tasks".format(
        RABBIT_MQ_SERVER, RABBIT_MQ_PORT
    ),
    "result_backend": "amqp://oracle-tasks:oracle@{}:{}//oracle-tasks".format(
        RABBIT_MQ_SERVER, RABBIT_MQ_PORT
    ),
    "CELERY_enable_utc": False,
}


