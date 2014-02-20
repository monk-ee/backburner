#!/usr/bin/python

__author__ = 'monkee'
from datetime import date
import sys
import logging

import boto.sqs
import yaml
from boto.sqs.message import RawMessage
import json

def main(argv):
    tag = ''
    checkout_dir = ''
    ssh_key = ''
    timestamp = str(date.today())

    #get configuration
    try:
        configStr = open('config.yml','r')
        config = yaml.load(configStr)
    except (OSError, IOError), emsg:
        print('Cannot find or parse config file: ' + str(emsg))
        sys.exit(2)

    #logging for debug really you can set to logging.INFO to chill it out
    logging.basicConfig(filename=config['logfile'],level=logging.INFO)

    #try:
    #    tag = argv[1]
    #    ip = argv[2]
    #except BaseException, emsg:
    #    logging.warning(timestamp + ': Missing Arguments: ' + str(emsg) + ' : '+str(argv))
    #    sys.exit(2)

    try:
        sqs = boto.sqs.connect_to_region("us-west-2",aws_access_key_id=config['s3']['aws_access_key'], aws_secret_access_key=config['s3']['aws_secret_key'])
        queue = sqs.get_queue(config['sqs']['name'])
        queue.set_message_class(RawMessage)
        print queue.count()
        for msg in queue.get_messages(5,visibility_timeout=10):
            single_message = json.loads(msg.get_body())
            print single_message['Message']
            #q.delete_message(m)
    except BaseException, emsg:
         logging.warning(timestamp + ': cannot get messages: ' + str(emsg))
         sys.exit(2)

    sys.exit()

if __name__ == "__main__":
   main(sys.argv)