import boto3
import re
import json


dsclient = boto3.client('ds', region_name='us-east-2')
ssmclient = boto3.client('ssm', region_name='us-east-2')
iamclient = boto3.client('iam')
ldapdirs = dsclient.describe_directories()['DirectoryDescriptions']
#print(dirs)
for ldap in ldapdirs:
	if 'z' in ldap['Name']:
		ldapid = ldap['DirectoryId']
		ldapdns = ldap['DnsIpAddrs']
		ldapname = ldap['Name']
		ldapshortname = ldap['ShortName']
		ldap_dict = {
			"schemaVersion" : "1.0",
			"description" : "Join instance to domain" +ldapname+"",
			"runtimeConfig" : {
			"aws:domainJoin": {
			"properties":{
				"directoryId": ldapid +"",
				"directoryName": ldapname +"",
				"directoryOU" : "OU=AWS,DC="+ldapshortname+",DC=com",
				"dnsIpAdresses": ldapdns
					}

				} 
			}
		}
		json_output = json.dumps(ldap_dict)
		ssmclient.create_document(
			Name = "awsconfig_Domain_"+ldapid+"_"+ldapname+"",
			Content = json_output,
			DocumentFormat = 'JSON',
			TargetType = '/AWS::EC2::Instance'

			)
ssmpolicy = {
		"Version": "2012-10-17",
		"Statement": [
		{
			"Effect": "Allow",
			"Action": [
			"ssm:DescribeAssociation",
			"ssm:GetDocument",
			"ssm:ListAssociations",
			"ssm:UpdateAssociationStatus",
			"ssm:UpdateInstanceInformation",
			"ssm:CreateAssociation"
			],
			"Resource": "*"

					}
					]
}

response = iam.create_policy(
	PolicyName = 'SSMADJoiner',
	PolicyDocument = json.dumps(ssmpolicy)
	)



		