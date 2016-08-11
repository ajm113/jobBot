#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

def initalizeDatabase(databaseFilename):
	connection = sqlite3.connect(databaseFilename)
	cursor = connection.cursor()

	# Create table if it doesn't already exsists.
	cursor.execute('''CREATE TABLE IF NOT EXISTS posts
		     (uid CHAR(250))''')
	return {'connection' : connection, 'cursor' : cursor}

def fetchByPosts(conn, posts):
	conn['connection'].execute('SELECT uid FROM posts WHERE uid IN (%s)' %','.join('?'*len(posts)), posts)

def insertPost(conn, post):
	t = (post,)
	conn['cursor'].execute('INSERT INTO posts VALUES (?)', t)
	conn['connection'].commit()

def closeConnection(conn):
	conn['connection'].close()