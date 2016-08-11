#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
import urllib, re, requests


def crawlCraigslistListPage(baseUrl, agentName, niche, jobRadius, zipCode, excludedKeywords):
	posts = []
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
			return False
		else:
			# See if we can find any emails in the description while we are in here.
			foundEmails = re.findall(r'[\w\.-]+@[\w\.-]+', description.text().lower())
	except Exception:
		print("error!")
		return False
	except requests.exceptions.ConnectionError:
		print ("Failed fetching post.")
		return False
	return {'emails' : foundEmails, 'description': description.text().strip(), 'title': title.text().strip()}

def crawlCraigsListPostAjaxContactInfo(baseUrl, post, agentName, stateAbv):
	ajaxUrl = baseUrl + generateEmailAjax(post, stateAbv)
	foundEmails = []
	try:
		page = pq(url=ajaxUrl, headers={'user-agent': agentName}, method='get', verify=True)
		email =  page(".anonemail")
		if len(email.text()) > 0:
			foundEmails.append(email.text().strip())
	except Exception:
		print ("Error!")
		return foundEmails
	except requests.exceptions.ConnectionError:
		print ("Failed fetching ajax page.")
		return foundEmails
	return foundEmails

def generateEmailAjax(postUrl, stateAbv):
	postUrl = postUrl.replace(".html","",1)
	postUrl = postUrl.replace("wvl","reply/%s" % (stateAbv), 1)
	postUrl = postUrl.strip()
	return postUrl