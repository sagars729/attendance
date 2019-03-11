import sqlite3
import argparse
from progress.bar import Bar
import cv2 as cv
import os

ap = argparse.ArgumentParser()
ap.add_argument('-d', '--database', help="Path To SQLite Database", required=True)
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

def vis(datestr, location, compid):
	os.chdir("tiny")
	if not curs: return
	rows = curs.execute("select image from records where compid=? and loc=? and datetime like ?", (compid,location,datestr))
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
	datestr = input("Date (yyyy-mm-dd): ")+"%"
	loc = input("Location: ")
	compid = int(input("Tracking ID: "))
	userid = int(input("User ID: "))
	tag(datestr, loc, compid, userid)
	return True

def vis_inp():
	datestr = input("Date (yyyy-mm-dd): ")+"%"
	loc = input("Location: ")
	compid = int(input("Tracking ID: "))
	vis(datestr, loc, compid)
	return True
	
if __name__ == "__main__":
	connect()
	print(conn,curs)
	while True: 
		inp = int(input("0 To Tag\n1 To Visualize\n-1 To Quit\nCommand: "))
		if(inp == -1): break 
		elif(inp == 0): tag_inp()
		else: vis_inp()		
	close()
