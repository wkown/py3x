#!/usr/bin/python3
# -*- coding:utf-8 -*-
from kafka import TopicPartition, KafkaProducer
producer = KafkaProducer(bootstrap_servers='192.168.112.131:9092')
for i in range(100):
    msg = b'some_message_bytes %d' % i
    print(msg)
    producer.send('test', msg)