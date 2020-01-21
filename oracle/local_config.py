import os

KEY = 'd413519f1bda2c8d7a700aab95cdef57-f7910792-ee3b91ed'
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
    "api_login_name": "8HtWfmFw2k6j",
    "transaction_key": ""
}



CELERY_SETTINGS = {
    "celery_broker_url": 'pyamqp://guest@localhost//',
    "result_backend": 'rpc://',
    
}

ADMIN = {
    "email_id" : "admin@oracleproducts.com",
    "password" : "oracle@123"
}


