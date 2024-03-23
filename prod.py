# from kafka import KafkaProducer
# import json
# import base64
# producer = KafkaProducer(
#     bootstrap_servers='grand-ox-5531-us1-kafka.upstash.io:9092',
#     sasl_mechanism='SCRAM-SHA-256',
#     security_protocol='SASL_SSL',
#     sasl_plain_username='Z3JhbmQtb3gtNTUzMST2eH4nv4xIx83xiDG0RKmiQ-0uwb25Uw6NPxeYZmqwMag',
#     sasl_plain_password='NDJmNmExZjEtOTkxMC00NGU0LTlhZTctMzRjYzU4MTUwOTky',
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# enc_content_base64 = base64.b64encode(b'test coentnt').decode('utf-8')
# encrypt_symmetric_key_base64 = base64.b64encode(b'theKEY').decode('utf-8')
# # task={
# #     "task_name":"MAKE_LETTER",
# #     # print("2. symmentric key used on letter for enc:", symmetric_key)
# #     "letter_tittle":"sun in the winter",
# #     # content=form.content.data
# #     "enc_content" :enc_content_base64,
    
# #     "encrypted_symmetric_key":encrypt_symmetric_key_base64 ,
# #     "author":"meow" ,
# #     "receiver":"doggo",
# #     "timestamp":"03:49, 19-02-2024",
# #     "letter_id":"testid diasdj",
    
    
# # }
           
    
# try:
#     producer.send('letters',value=task)
#     producer.flush()
#     print("Message produced without Avro schema!")
# except Exception as e:
#     print(f"Error producing message: {e}")
# finally:
#     producer.close()
