#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import boto3

ec2 = boto3.client('ec2')

# インスタンスの状態が変わるまで待機する
def wait_instance_state(instance_id,target_state):
	import time
	print "%s が %s 状態になるまで待機中" % ( instance_id, target_state )
	while True:
		cs=ec2.describe_instances( InstanceIds=[instance_id] )
		current_state=cs['Reservations'][0]['Instances'][0]['State']['Name']
		if current_state == target_state:
			break
		time.sleep(1)

# 使い方
def usage():
	print "USAGE: %s [InstanceID] [State]"
	print "  State: pending | running | shutting-down"
	print "         terminated | stopping | stopped"
	quit()

# main
if __name__ == '__main__':
	import sys
	argvs = sys.argv
	argc = len(argvs)

	if argc != 3:
		usage()

	wait_instance_state(argvs[1], argvs[2])

