import sqlite3
import argparse
from progress.bar import Bar
import cv2 as cv
import os
import json

ap = argparse.ArgumentParser()
ap.add_argument('-d', '--database', help="Path To SQLite Database", required=True)
ap.add_argument('-t', '--datetime', help="Autofill Datetime")
ap.add_argument('-l', '--location', help="Autofill Location")
args = vars(ap.parse_args())
conn = None
curs = None
def connect():
	global conn, curs
	conn = sqlite3.connect(args['database'])
	curs = conn.cursor()	

def tag(datestr, location, compid, userid):
	if not curs: return
	curs.execute("update records set userid=? where compid=? and loc=? and datetime like ?", (userid,compid,location,datestr))

def useridToJSON(datestr, location):
	if not curs: return
	rows = curs.execute("select distinct compid, userid from records where loc=? and datetime like ?", (location, datestr)).fetchall()
	return {row[0]: row[1] for row in rows}

def JSONToUserid(datestr,location,dic):
	for k in dic: tag(datestr, location, int(k), dic[k])

def vis(datestr, location, compid):
	os.chdir("tiny")
	if not curs: return
	rows = curs.execute("select image from records where compid=? and loc=? and datetime like ?", (compid,location,datestr)).fetchall()
	if len(rows) > 10: rows = rows[0:10]
	for row in rows:
		img = cv.imread(row[0])
		cv.imshow("image", img)
		cv.waitKey(0)
	cv.destroyAllWindows()	
	os.chdir('..')

def close():
	if not conn: return
	conn.commit()
	conn.close()

def tag_inp():
	if args["datetime"]: datestr = args["datetime"] + "%"
	else: datestr = input("Date (yyyy-mm-dd): ")+"%"
	if args["location"]: loc = args["location"]
	else: loc = input("Location: ")
	compid = int(input("Tracking ID: "))
	userid = int(input("User ID: "))
	tag(datestr, loc, compid, userid)
	return True

def vis_inp():
	if args["datetime"]: datestr = args["datetime"] + "%"
	else: datestr = input("Date (yyyy-mm-dd): ")+"%"
	if args["location"]: loc = args["location"]
	else: loc = input("Location: ")
	compid = int(input("Tracking ID: "))
	vis(datestr, loc, compid)
	return True

def reset():
	if not curs: return
	curs.execute("drop table records")
	curs.execute("CREATE TABLE records (image text primary key, datetime text, loc text, res int, compid int, userid int, width int, height int, hwratio double, x int, y int, frame int)")	
	return True

def vis_user():
	if not curs: return
	rows = curs.execute("select * from users")
	for i in rows: print(i)

def add_user(userid, name):
	if not curs: return
	curs.execute("insert into users (userid, name) values (?,?)",(userid,name))

def upd_user(userid, name):
	if not curs: return
	curs.execute("update users set name=? where userid=?",(name,userid))

def toJSON():
	if args["datetime"]: datestr = args["datetime"] + "%"
	else: datestr = input("Date (yyyy-mm-dd): ")+"%"
	if args["location"]: loc = args["location"]
	else: loc = input("Location: ")
	fn = input("Filename: ")
	json.dump(useridToJSON(datestr,loc),open(fn,'w'))

def loJSON():
	if args["datetime"]: datestr = args["datetime"] + "%"
	else: datestr = input("Date (yyyy-mm-dd): ")+"%"
	if args["location"]: loc = args["location"]
	else: loc = input("Location: ")
	fn = input("Filename: ")
	JSONToUserid(datestr,loc,json.load(open(fn,'r')))
	
if __name__ == "__main__":
	connect()
	print(conn,curs)
	while True: 
		inp = int(input("0 To Tag\n1 To Visualize\n2 To Reset\n3 To See Registered Users\n4 To Add New User\n5 To Update Existing User\n-1 To Save and Quit\n-2 To Save\nCommand: "))
		if(inp == -1): break 
		elif(inp == -2): conn.commit()
		elif(inp == 0): tag_inp()
		elif(inp == 1): vis_inp()
		elif(inp == 2): reset()
		elif(inp == 3): vis_user()	
		elif(inp == 4): add_user(int(input("User ID: ")), input("User Name: "))	
		elif(inp == 5): upd_user(int(input("User ID: ")), input("User Name: "))	
		elif(inp == 6): toJSON()
		elif(inp == 7): loJSON() 	
	close()

