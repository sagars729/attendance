# Automating Classroom Attendance

This repository has all the code from my independent research project at TJHSST's Computer Systems Lab on Automating Classroom Attendance Using Facial Recognition and Interactive Machine Learning. 

<p align="center">
  <img src="/test.png" alt="Test" width="80%"/>
</p>

1. [Useful Links](#useful-links) - Includes the link to the paper, poster, and presentation associated with this project (submitted for TJStar) as well as useful resources I found while developing this project and a link to a card on my former website describing this project. 
2. [Abstract](#abstract) - Abstract from the paper I wrote on this project. 
3. [Code Overview](#code-overview) - Simple overview of all code in this project and worfkflow.
4. [Model](#model) - Simple diagram showcasing the ML model I used for this project. 

## Useful Links 

Project Website: https://user.tjhsst.edu/2019ssaxena/documents/attendance_paper.pdf  
Paper: https://user.tjhsst.edu/2019ssaxena/attendance  
Poster: https://user.tjhsst.edu/2019ssaxena/documents/attendance_poster.pdf  
Presentation: https://user.tjhsst.edu/2019ssaxena/documents/attendance_presentation.pdf  
Resources: https://user.tjhsst.edu/2019ssaxena/documents/attendance_resources.pdf  

## Abstract

Everyday, teachers across the nation engage in the crucial activity of taking attendance. By taking classroom attendance, teachers not only quantify the effort and dedication of individual students, but also motivate students to come to school by rewarding them for their dedication. Furthermore, the process of attendance allows schools to keep track of each student as they progress through their day and is a basic standard for maintaining the safety of each individual student. This process, however, can come at the cost of valuable instructional time. For example, take Thomas Jefferson High School for Science and Technology, one of the nation’s top high schools. Every week approximately 1700 students at TJHSST traverse through 25 periods. Assuming that the process of attendance takes 5 minutes per class, TJ, as a whole, spends 212500 minutes or 3542 hours each week on attendance. Attendance is a task that is replicated frequently everyday and is therefore a task that is prime for automation. This paper assumes a novel approach to classroom attendance by treating it as an extension of Multi-View Group Facial Recognition In The Wild.

## Code Overview

<p align="center">
  <img src="/workflow.png" alt="Workflow" width="80%"/>
</p>

**Workflow.** The complete workflow of how each program interacts with every other program and system in this project.
- **read_and_classify.sh** - bash script for reading input data (a video) and classifying all faces found within that video
- **detection.py** - detects and tracks faces in a input video
- **tag.py** - tags batches of pictures using their tracking labels for training or testing
- **class_train.py** - trains a facial recognition model for a specific class
- **read_and_classify_web.sh** - bash script for reading input data given by the web interface and classifying all faces found within that video
- **website/app.js** - server code that hosts the web interface
- **website/Run/index.hbs** - hbs code that renders the web interface

## Model

<p align="center">
  <img src="https://user.tjhsst.edu/2019ssaxena/landing/css/model.png" alt="Machine Learning Model For Classifying Faces" width="40%"/>
</p>

**Machine Learning Model For Classifying Faces.** This model consists of 5 Convolutional Layers, 3 Fully Connected Layers, and 3 Max Pooling Layers. It was inspired from AlexNet. 
