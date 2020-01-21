
KEY = 'd413519f1bda2c8d7a700aab95cdef57-f7910792-ee3b91ed'
SANDBOX = 'transaction-email.esthenos.com'

BUFFER_PERIOD = 5
MONGODB_SETTINGS = {
    "DB": "oracle-products-dev",
    "PORT": 27017,
    "HOST": "localhost",
    "connect": True,
}

AWS_SETTINGS = {
  'AWS_CDN_PATH' : 's3.ap-south-1.amazonaws.com',
  'AWS_S3_BUCKET' : 'esthenos-northernarc-test',
  'AWS_COGNITO_ID' : 'ap-south-1:80af4439-f24e-4fa7-8869-a50dc896f8fd',
  'AWS_ACCESS_KEY_ID' : 'AKIATM6KAUK6CYGNT5ON',
  'AWS_SECRET_ACCESS_KEY' : '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',
  'AWS_REGION':'ap-south-1',
  'AWS_COGNITO_PROVIDER_ID':'com.esthenos.conatus',
  'StreamName': 'esthenos-northernarc-dev',
  'Shard': 1,
  'PartitionKey': 'EsthenosNorthernArc'

}


AUTHORIZE_CREDENTIALS = {
    "api_login_name": "8HtWfmFw2k6j",
    "transaction_key": "9R65uL8D4dg6w9jK"
}

RABBIT_MQ_SERVER = "127.0.0.1"
RABBIT_MQ_PORT = "5672"

CELERY_SETTINGS = {
    "CELERY_broker_url": "amqp://oracle-task:oracle@{}:{}//oracle-task".format(
        RABBIT_MQ_SERVER, RABBIT_MQ_PORT
    ),
    "result_backend": "amqp://oracle-task:oracle@{}:{}//oracle-task".format(
        RABBIT_MQ_SERVER, RABBIT_MQ_PORT
    ),
    
}

ADMIN = {
    "email_id" : "admin@oracleproducts.com",
    "password" : "oracle@123"
}


