#!/usr/bin/env python
# -*- coding: utf-8 -*-

def emailEmployeer(emails, emailFrom, emailReplyTo, title, postUrl, templateFilePath):
	
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
			smtpObj = smtplib.SMTP(smtpHost)
			smtpObj.ehlo()
			smtpObj.starttls()
			smtpObj.ehlo()
			smtpObj.login(smtpEmail,smtpPass)
		   	smtpObj.sendmail(smtpEmail, emails, template)
			smtpObj.quit()
		except smtplib.SMTPException, e:
			print e
			return False
	return True