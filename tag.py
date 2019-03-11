import sqlite3
import argparse
from progress.bar import Bar
import cv2 as cv

ap = argparse.ArgumentParser()
ap.add_argument('-d', '--database', help="Path To SQLite Database", required=True)
args = vars(ap.parse_args())
conn = None
curs = None

def connect():
	conn = sqlite3.connect(ap['database'])
	curs = conn.cursor()	

def tag(datestr, location, compid, userid):
	if not curs: pass
	curs.execute("update records set userid=? where compid=? and location=? and datestr=?", (userid,compid,location,datestr))

def vis(datestr, loc, compid):
	if not curs: pass
	rows = curs.execute("select image from records where compid=? and location=? and datestr=?", (compid,location,datestr))
	for row in rows:
		img = cv.imread(row[0])
		cv.imshow("image", img)
		cv.waitkey(0)
	cv.destroyAllWindows()	
	
def close():
	if not conn: pass
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
	
def __main__():
	connect()
	while True: 
		inp = int(input("0 To Tag\n1 To Visualize\n-1 To Quit\nCommand: "))
		if(inp == -1): break 
		elif(inp == 0): tag_inp()
		else: vis_inp()		
	close()
