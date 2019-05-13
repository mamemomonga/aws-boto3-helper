#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

# Route53のレコード更新
class Route53SetRecord:

	# コンストラクタ
	def __init__(self,**kwargs):
		import boto3
		self.r53=boto3.client('route53')
		self.logger = kwargs.get('logger')

		self.zone_name = kwargs.get('ZoneName')
		self.rev_name  = kwargs.get('RevName')

		self.zone_id = self.name2id(self.zone_name)
		self.rev_id  = self.name2id(self.rev_name)

		self.logger.info("正引き {:<24} [{}]".format( self.zone_name, self.zone_id ))
		self.logger.info("逆引き {:<24} [{}]".format( self.rev_name,  self.rev_id ))

	def dump(self,data):
		import pprint
		pprint.PrettyPrinter(indent=4).pprint(data)

	def all_hosted_zones(self):
		if not '_all_hosted_zones' in locals():
			self._all_hosted_zones=self.r53.list_hosted_zones(MaxItems='1000')
		return self._all_hosted_zones

	def name2id(self,name):
		import re
		zones=self.all_hosted_zones()['HostedZones']
		for z in zones:
			if z['Name'] == name+'.':
				return re.sub('^/hostedzone/','',z['Id'])

	# 登録
	def regist(self,**kwargs):
  		import re
  
  		delete_only = kwargs.get('DeleteOnly',False)
		hostname    = kwargs.get('HostName')
		ipaddr      = kwargs.get('IpAddress')

		if delete_only:
			self.logger.info("削除します")

  		# 正引き
  		self.update_record(
  			HostedZoneId = self.zone_id,
  			Name         = hostname,
  			Type         = 'A',
  			Value        = ipaddr,
  			DeleteOnly   = delete_only
  		)
  
  		# 逆引き
  		sprivip=ipaddr.split('.')	
  		ptr=sprivip[3]+'.'+sprivip[2]+'.'+self.rev_name
  
  		self.update_record(
  			HostedZoneId = self.rev_id,
  			Name         = ptr,
  			Type         = 'PTR',
  			Value        = hostname,
  			DeleteOnly   = delete_only
  		)

	# レコード更新
	def update_record(self,**kwargs):
  		hosted_zone_id = kwargs.get('HostedZoneId')
  		default_ttl    = kwargs.get('DefaultTTL',60)
  		record_name    = kwargs.get('Name')
  		record_type    = kwargs.get('Type')
  		record_value   = kwargs.get('Value','')
  		delete_only    = kwargs.get('DeleteOnly',False)

  		# レコード一覧
  		r=self.r53.list_resource_record_sets( HostedZoneId=hosted_zone_id )
  
  		# レコードがすでに定義してあるか探す
  		rr=[]
  		ttl=default_ttl
  		for i in r['ResourceRecordSets']:
  			if i['Name'] == record_name+'.':
  				if i['Type'] == record_type:
  					rr=i['ResourceRecords']
  					ttl=i['TTL']
  					break
  
  		# レコードがあれば消す
  		if len(rr) > 0:
  			self.logger.info("Route53: %s から %s の削除" % ( hosted_zone_id, record_name) )
  			self.r53.change_resource_record_sets(
  				HostedZoneId=hosted_zone_id,
  				ChangeBatch={
  					'Changes': [{
  						'Action': 'DELETE',
  						'ResourceRecordSet': {
  							'Name': record_name,
  							'Type': record_type,
  							'TTL' : ttl,
  							'ResourceRecords': rr,
  						}
  					}]
  				}
  			)
  
  		if delete_only:
  			return
  
  		# レコードの追加
  		self.logger.info("Route53: %s へ %s の追加" % ( hosted_zone_id, record_name) )
  		r=self.r53.change_resource_record_sets(
  			HostedZoneId=hosted_zone_id,
  			ChangeBatch={
  				'Changes': [{
  					'Action': 'UPSERT',
  					'ResourceRecordSet': {
  						'Name': record_name,
  						'Type': record_type,
  						'TTL' : default_ttl,
  						'ResourceRecords': [{
  							'Value': record_value
  						}]
  					}
  				}]
  			}
  		)

def _startup():
	from site import addsitedir
	from os.path import dirname, realpath, abspath
	basedir = abspath(dirname( realpath(__file__)) + '/.' )
	sitedir = basedir + '/libs'
	addsitedir( sitedir )
	return basedir
basedir = _startup()

def _logger():
	from logging import getLogger, StreamHandler, Formatter, DEBUG
	import sys
	logger = getLogger(__name__)
	handler = StreamHandler(sys.stderr)
	handler.setFormatter( Formatter(fmt='[%(asctime)-15s][%(levelname)-8s] %(message)s'))
	handler.setLevel(DEBUG)
	logger.setLevel(DEBUG)
	logger.addHandler(handler)
	logger.propagate = False
	return logger
logger = _logger()

def main():
	import argparse,sys

	logger.info("Rote53 PrivateZone更新ツール")
	parser = argparse.ArgumentParser(description='Rote53 PrivateZone更新ツール')
	parser.add_argument('-z', '--zone', type=str, help='正引きドメイン名', required=True ) 
	parser.add_argument('-r', '--rev',  type=str, help='逆引きドメイン名', required=True ) 
	parser.add_argument('-o', '--host', type=str, help='ホスト名',         required=True ) 
	parser.add_argument('-i', '--ip',   type=str, help='IPアドレス',       required=True ) 
	parser.add_argument('-d', '--delete',dest='delete', help='削除', action='store_true') 
	args = parser.parse_args()

	r53=Route53SetRecord(
		logger=logger,
		ZoneName  = args.zone,
		RevName   = args.rev
	)
	r53.regist(
		HostName  = args.host,
		IpAddress = args.ip,
		DeleteOnly = args.delete
	)

if __name__ == '__main__':
	main()
