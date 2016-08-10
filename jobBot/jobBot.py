#!/usr/bin/env python
import argparse
from jobCrawler import *
from jobDatabase import *
from jobMailer import *

def main():
	parser = argparse.ArgumentParser(description='Search for jobs via craigslist!')

	parser.add_argument('u', '--url', type=str,
			help='The base url of the craigslist')

	parser.add_argument('e', '--email', type=str,
			help='The email address you want to use as "from".')

	parser.add_argument('p', '--password', type=str,
			help='The SMTP password.')

	parser.add_argument('l', '--login', type=str,
			help='The SMTP username login.')

	parser.add_argument('t', '--template', type=str,
			help='The email template file')

	parser.add_argument('x', '--exclude', type=str,
			help='Words you want to exclude from job listings.')

	parser.add_argument('z', '--zip', type=str,
			help='The zipcode we are looking in.')

	parser.add_argument('r', '--radius', type=str,
			help='The radius (miles) we want to search.')

	parser.add_argument('n', '--niches', type=str,
			help='Job niches we want. (PLEASE USE CRAIGSLIST NICHE CODES)')

	parser.add_argument('a', '--agent', type=str,
			help='Agent name we want to use scrapping CraigsList')

	parser.add_argument('w', '--wait', type=str,
			help='Amount of times in seconds to wait each request. (Usuage 5 is good!)')

	parser.add_argument('s', '--sleep', type=str,
			help='Amount of times in seconds to sleep after checking after each job.')

	args = parser.parse_args()


if __name__ == '__main__':
	main()