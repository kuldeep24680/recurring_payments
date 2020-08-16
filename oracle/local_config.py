import os

KEY = ''
SANDBOX = ''

BUFFER_PERIOD = 5
MONGODB_SETTINGS = {
    "DB": "oracle-products-dev",
    "PORT": 27017,
    "HOST": "localhost",
    "connect": True,
}

AWS_SETTINGS = {
  'AWS_S3_BUCKET' : '',
  'AWS_ACCESS_KEY_ID' : '',
  'AWS_SECRET_ACCESS_KEY' : '',
  'AWS_REGION':'ap-south-1',


}


AUTHORIZE_CREDENTIALS = {
    "api_login_name": "",
    "transaction_key": ""
}



CELERY_SETTINGS = {
    "celery_broker_url": 'pyamqp://guest@localhost//',
    "result_backend": 'rpc://',
    
}

ADMIN = {
    "email_id" : "",
    "password" : ""
}


