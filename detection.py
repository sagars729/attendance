import matlab.engine
import cv2 as cv
import numpy as np
import multiprocessing
from multiprocessing import pool
import os
import sys
import _pickle as cPickle
from munkres import Munkres
import _pickle as cPickle
import argparse
try:
	from secrets import token_hex
except ImportError:
	from os import urandom
	def token_hex(nbytes=None):
		return urandom(nbytes).hex()
print('Imported External Libraries')

### CMD LINE ARGS ###
ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video',help='Path to Video file')
ap.add_argument('-w', '--webcam',help='Enable WebCam',action="store_true",default=False)
ap.add_argument('-n', '--number-of-frames',type=int,default=-1,help="Maximum Number of Frames To Capture")
ap.add_argument('-s', '--skip-rate',type=int,default=1,help="Skip Rate of Frames")
ap.add_argument('-b', '--boxes',help="Path To Bounding Boxes File")
ap.add_argument('-t', '--track',help="Enable Tracking",action="store_true",default=False)
ap.add_argument('--no-display',help="Disables Display",action="store_true",default=False)
ap.add_argument('--save-boxes',help="Path To Save Bounding Boxes")
ap.add_argument('--save-video',help="Path TO Save Video")
args = vars(ap.parse_args())
#### INIT SCRIPT ####
os.chdir("tiny")#eng.eval("cd tiny")
print("Changed Working Directory To Tiny")
if not args['boxes']: 
	eng = matlab.engine.start_matlab()
	print("Matlab Engine Spun Up")
m = Munkres()
#####################
class Box:	
	def __init__(self,vals,i_d = None):
		self.coord = vals
		if vals != None: self.area = abs(vals[2] - vals[0])*abs(vals[3]-vals[1])
		self.id = i_d
		if self.id == None: self.color = (0,255,0)
		else: self.color = (255-self.id*10,0,self.id*10)
	def setId(self,i_d,coef=40):
		self.id = i_d
		if self.id == None: self.color = (0,255,0)
		else: self.color = (255-self.id*coef,0,self.id*coef)
	def IoU(self, other):
		if self.coord == None or other.coord == None: return .01
		boxA = self.coord
		boxB = other.coord
		xA = max(boxA[0], boxB[0])
		yA = max(boxA[1], boxB[1])
		xB = min(boxA[2], boxB[2])
		yB = min(boxA[3], boxB[3])
		interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
		boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
		boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
		iou = interArea / float(boxAArea + boxBArea - interArea)
		return iou	
	def __repr__(self):
		return str(self.coord)

def getImageBoxes(frame):
	fname = 'temp_pics/' + token_hex(6) + '.jpg'
	cv.imwrite(fname,frame)
	cmd = "tiny_face_detector('"+fname+"','"+fname+"',.5,.1,0)"
	bboxes = eng.eval(cmd)
	os.system('rm ' + fname) 
	return bboxes

def showVideo(vid):
	i = 0
	while i < len(vid):
		cv.imshow('Detections',vid[i])
		if cv.waitKey(1) & 0xFF == ord('q'): break
		if i == len(vid)-1 and int(input("1 To Replay ")) == 1: i = 0
		else: i+=1
	cv.destroyAllWindows()
def readVideo(fname, n=-1, s=1):
	vid = []
	cap = cv.VideoCapture(fname)
	i = -1
	while cap.isOpened():
		if len(vid) == n: break
		ret, frame = cap.read()
		i+=1
		if i%s != 0: continue
		vid.append(frame)
		if cv.waitKey(1) & 0xFF == ord('q'): break
	return vid

def getVideoBoxes(vid):
	print("Computing Video Boxes")
	boxes = []
	for frame in vid: boxes.append([Box(i) for i in getImageBoxes(frame)])
	return boxes 

def drawBoxes(vid,boxes):
	for i in range(len(vid)):
		frame = vid[i]
		bboxes = boxes[i]
		for box in bboxes: 
			coords = box.coord
			if(coords == None): continue
			frame = cv.rectangle(frame, (int(coords[0]), int(coords[1])), (int(coords[2]), int(coords[3])), box.color, 2)

def track(boxes):
	if(len(boxes)==0): return
	bboxes = boxes[0]
	maxid = len(boxes[0])
	for i in range(len(bboxes)): bboxes[i].setId(i)
	for i in range(1,len(boxes)):
		curr = boxes[i]
		prev = boxes[i-1]
		lc = len(curr)
		lp = len(prev)		
		if len(curr) < len(prev): curr += [Box(None) for i in range(0,len(prev)-len(curr))]
		if len(prev) < len(curr):
			maxid += len(curr) - len(prev)
			prev = prev + [Box(None,maxid-i) for i in range(0,len(curr)-len(prev))]
		cmat = [[-1*c.IoU(p) for p in prev] for c in curr]
		matches = m.compute(cmat)
		for c,p in matches: curr[c].setId(prev[p].id)				
		curr = curr[0:lc]
		prev = prev[0:lp]
	
def readWebCam(n=-1,s=1):
	DCS_IP = "198.38.18.121"#"192.168.1.29"
	userauth = ('admin', 'pass098')
	streamurl = "http://" + ':'.join(userauth) + '@' + DCS_IP + "/video/mjpg.cgi?type=.mjpg" 
	vid = []
	cap = cv.VideoCapture(streamurl)
	i = -1
	while True:
		if len(vid) == n: break
		ret, frame = cap.read()
		cv.imshow('Input',frame)
		i+=1
		if i%s != 0: continue
		vid.append(frame)
		if cv.waitKey(1) & 0xFF == ord('q'): break
	return vid
def readBoxes(filepath):
	return cPickle.load(open(filepath,'rb'))

def writeBoxes(boxes,filepath):
	cPickle.dump(boxes,open(filepath,'wb'))

def writeVideo(vid,filepath):
	if len(vid) == 0: return
	fourcc = cv.VideoWriter_fourcc(*'mpv4')
	out = cv.VideoWriter(filepath,0x7634706d, 20.0, (vid[0].shape[0],vid[0].shape[1]))
	for frame in vid: out.write(frame)
	out.release()

def endProgram(msg = None):
	if msg: print(msg)
	sys.exit()

if __name__ == "__main__":
	if args['webcam']: vid = readWebCam(args["number_of_frames"], args["skip_rate"])
	elif args['video']: vid = readVideo(os.path.join('..',args["video"]),args["number_of_frames"], args["skip_rate"])
	else: endProgram("No Video Input Given. Use the --video or --webcam flags to provide video input.")
	print("Read video of size", len(vid), "given maximum number of frames =", args["number_of_frames"], "and skip rate =", args["skip_rate"], "frames")
	if args["boxes"]: boxes = readBoxes(os.path.join('..',args["boxes"]))
	else: boxes = getVideoBoxes(vid) 
	if args["track"]: track(boxes)
	else: print("Tracking Disabled")
	drawBoxes(vid,boxes)
	if not args["no_display"]: showVideo(vid)
	else: print("Display Disabled")
	if args["save_boxes"]: writeBoxes(boxes,os.path.join('..',args["save_boxes"]))
	else: print("Saving Boxes Disabled")
	if args["save_video"]: writeVideo(vid,os.path.join('..',args["save_video"])) 
	else: print("Saving Video Disabled")
