#!/usr/bin/env python
import argparse, time

def parseArguments():
	parser = argparse.ArgumentParser(description='Search for jobs via craigslist!')

	requiredNamed = parser.add_argument_group('required arguments')

	requiredNamed.add_argument('-u', '--url', type=str,
			help='The base url of the craigslist', required=True)

	requiredNamed.add_argument('-b', '--abbreviation', type=str,
			help='The CraigsList city abbreviation.', required=True)

	requiredNamed.add_argument('-e', '--email', type=str,
			help='The email address you want to use as "from".', required=True)

	requiredNamed.add_argument('-p', '--password', type=str,
			help='The SMTP password.', required=True)

	requiredNamed.add_argument('-s', '--server', type=str,
			help='The SMTP host.', required=True)

	requiredNamed.add_argument('-l', '--login', type=str,
			help='The SMTP username login.', required=True)

	requiredNamed.add_argument('-t', '--template', type=str,
			help='The email template file', required=True)

	requiredNamed.add_argument('-z', '--zip', type=str,
			help='The zipcode we are looking in.', required=True)

	requiredNamed.add_argument('-r', '--radius', type=int,
			help='The radius (miles) we want to search.', required=True)

	requiredNamed.add_argument('-n', '--niches', type=str,
			help='Job niches we want. (PLEASE USE CRAIGSLIST NICHE CODES)', required=True)

	parser.add_argument('-x', '--exclude', type=str,
			help='Words you want to exclude from job listings.', required=False)

	parser.add_argument('-a', '--agent', type=str,
			help='Agent name we want to use scrapping CraigsList (Default is JobBot)', required=False, default="jobBot 1.0")

	parser.add_argument('-w', '--wait', type=int,
			help='Amount of times in seconds to wait each request. (Default is 5)', required=False, default=5)

	parser.add_argument('-f', '--fall', type=int,
			help='Amount of times in seconds to sleep after checking after each job. (Default is 1 hour)', required=False, default=3600)

	parser.add_argument('-d', '--dry', type=bool,
			help='Simply dry run. (Do NOT send emails)', required=False)

	args = parser.parse_args()

	if args.exclude != None:
		args.exclude = args.exclude.split(',')
	else:
		args.exclude = []

	args.niches = args.niches.split(',')

	return args

def crawlCraigslist(args):
	import jobCrawler
	import jobDatabase
	import jobMailer

	#Initalize the database!
	sqlConnection = jobDatabase.initalizeDatabase("%s.db" % args.email)

	while True:
		try:
			# Find posts to parse!
			print ("Finding posts...")
			foundPosts = []
			for niche in args.niches:
				foundPosts += jobCrawler.crawlCraigslistListPage(args.url, args.agent, niche, args.radius, args.zip, args.exclude)
				time.sleep(args.wait)

			print ("Excluding any posts we already searched...")
			# Exlucde any we already went through.
			jobDatabase.fetchByPosts(sqlConnection, foundPosts)
			for row in sqlConnection['cursor']:
				if row[0] in foundPosts:
					 foundPosts.remove(row[0])	# Remove if found in result.

			print ("Looking for jobs...")
			# Now iterate over our found posts, find if we can appy!
			for post in foundPosts:
				postData = jobCrawler.crawlCraigsListPost(args.url, post, args.agent, args.exclude)
				time.sleep(args.wait)

				if postData == False:
					continue

				foundEmails = postData['emails']

				foundEmails += jobCrawler.crawlCraigsListPostAjaxContactInfo(args.url, post, args.agent, args.abbreviation)
				time.sleep(args.wait)

				print foundEmails

				# Insert the post into our db.
				jobDatabase.insertPost(sqlConnection, post)

				# Send the emails if everything checks out!
				if args.dry != True & len(foundEmails) > 0:
					emailSubject = "Re: %s" % (postData['title'])
					print "Sending '%s'!" % (emailSubject)

					smtpSettings = {
						'host': args.server,
						'login': args.login,
						'password': args.password
					}

					jobMailer.emailEmployeer(['andrewmcrobb@gmail.com'], args.login, args.email, emailSubject, post, args.template, smtpSettings)
				
			print ("All done! Going to sleep...")
			time.sleep(args.fall
				)
		except KeyboardInterrupt:
			print "Keyboard Interrupt detected! Shutting down!"
			jobDatabase.closeConnection(sqlConnection)
			break

def main():
	crawlCraigslist(parseArguments())

if __name__ == '__main__':
	main()