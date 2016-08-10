#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

def initalizeDatabase(databaseFilename):
	connection = sqlite3.connect(databaseFilename)
	cursor = connection.cursor()

	# Create table if it doesn't already exsists.
	cursor.execute('''CREATE TABLE IF NOT EXISTS posts
		     (uid CHAR(250))''')
	return [connection, cursor]

def fetchByPosts(cursor, posts):
	cursor.execute('SELECT uid FROM posts WHERE uid IN (%s)' %','.join('?'*len(posts)), posts)

def insertPost(connection, cursor, post):
	t = (post,)
	cursor.execute('INSERT INTO posts VALUES (?)', t)
	connection.commit()

def closeConnection(connection):
	connection.close()