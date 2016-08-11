#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib

def emailEmployeer(emails, emailFrom, emailReplyTo, title, postUrl, templateFilePath, smtpSettings):
	
	template = ''
	
	# Load in the template file and do string replacements.
	with open(templateFilePath, 'r') as emailTemplateFile:
		template=emailTemplateFile.read()
		template = template.replace("%toEmail%", ' '.join(emails))
		template = template.replace("%fromEmail%", emailFrom)
		template = template.replace("%subject%", title)
		template = template.replace("%replyEmail%", emailReplyTo)
		template = template.replace("%url%", postUrl)
		try:
			smtpObj = smtplib.SMTP(smtpSettings['host'])
			smtpObj.ehlo()
			smtpObj.starttls()
			smtpObj.ehlo()
			smtpObj.login(smtpSettings['login'], smtpSettings['password'])
		   	smtpObj.sendmail(smtpSettings['login'], emails, template)
			smtpObj.quit()
		except smtplib.SMTPException, e:
			print e
			return False
	return True