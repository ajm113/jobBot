#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
import urllib, time, re, requests


def crawlCraigslistListPage(baseUrl, agentName, niche, jobRadius, zipCode, excludedKeywords):
	posts = []
	for niche in jobTypes:
		pageUrl = "%s/search/wvl/%s?sort=date&search_distance=%s&postal=%s" % (baseUrl, niche, jobRadius, zipCode)
		page = pq(url=pageUrl, headers={'user-agent': agentName}, method='get', verify=True)
		links =  page("a.hdrlnk")
		for link in links:
			pLink = pq(link)
			if any(ext in pLink.text().lower() for ext in excludedKeywords) == False:
				posts.append(pLink.attr('href'))	# Use the url as the 'id'.
	return posts

def crawlCraigsListPost(baseUrl, uri, agentName, excludedKeywords):
	pageUrl = baseUrl + uri
	foundEmails = []
	try:
		page = pq(url=pageUrl, headers={'user-agent': agentName}, method='get', verify=True)
		description =  page("#postingbody")
		title = page("#titletextonly")
		if any(ext in description.text().lower() for ext in excludedKeywords) == True:
			return foundEmails
		else:
			# See if we can find any emails in the description while we are in here.
			foundEmails = re.findall(r'[\w\.-]+@[\w\.-]+', description.text().lower())
	except Exception, e:
		print e
	except requests.exceptions.ConnectionError:
		print "Failed fetching post."
	return foundEmails

def crawlCraigsListPostAjaxContactInfo(baseUrl, post, agentName):
	ajaxUrl = baseUrl + generateEmailAjax(post)
	foundEmails = []
	try:
		page = pq(url=ajaxUrl, headers={'user-agent': agentName}, method='get', verify=True)
		email =  page(".anonemail")
		if len(email.text()) > 0:
			foundEmails.append(email.text().strip())
	except Exception, e:
		print e
	except requests.exceptions.ConnectionError:
		print "Failed fetching ajax page."
	return foundEmails

def generateEmailAjax(postUrl, stateAbv):
	postUrl = postUrl.replace(".html","",1)
	postUrl = postUrl.replace("wvl","reply/%s" % (_, stateAbv), 1)
	postUrl = postUrl.strip()
	return postUrl