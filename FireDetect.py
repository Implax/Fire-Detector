import cv2
import numpy as np
import playsound
import smtplib #Sending emails
from datetime import datetime
from collections import deque

camera_deque = deque([])

def show_hash(hashTable): 
      
    for i in range(len(hashTable)): 
        print(i, end = " ") 
          
        for j in hashTable[i]: 
            print("-->", end = " ") 
            print(j, end = " ") 
              
        print() 
  
# Creating Hashtable as  
# a nested list. 
HashTable = [[] for _ in range(10)] 
  
# Hashing Function to return  
# key for every value. 
def Hashing(keyvalue): 
    return keyvalue % len(HashTable) 

# Insert Function to add 
# values to the hash table 
def insert(Hashtable, keyvalue, value): 
      
    hash_key = Hashing(keyvalue) 
    Hashtable[hash_key].append(value) 
  
# Driver Code 
insert(HashTable, 2, 'richard.clottey@ashesi.edu.gh') 
insert(HashTable, 5, 'steven.attipoe@ashesi.edu.gh') 
insert(HashTable, 8, 'gerald.akita@ashesi.edu.gh') 

Fire_Status = 0
Alarm_Sound = False

def play_alarm():
    playsound.playsound("C:/Users/HP/Desktop/Machine Learning/Final/fire_alarm_sound.mp3", True)

def send_email():

    recipientEmail = "juniorclottey@gmai"
    recipientEmail = recipientEmail.lower()

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("dsapythongroup@gmail.com", 'dsagroup')
        server.sendmail('dsapythongroup@gmail.com', recipientEmail, "Warning A Fire Accident has been reported at ABC Company")
        print("sent to {}".format(recipientEmail))
        server.close()
    except Exception as e:
    	print(e)

firevid = cv2.VideoCapture("C:/Users/HP/Desktop/Machine Learning/Final/test4.mp4")
amount = 0

# Frame Analyzation
while True:
    # firevid.read() returns a boolean if frame is read correctl
    ret, frame = firevid.read()
    
    frame = cv2.resize(frame, (1000,600))
    
    blur = cv2.GaussianBlur(frame, (21,21),0) #Removes noises from video
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV) #Converts video output to HSV colorspace

    lower = [18,50,50]
    upper = [35,255,255]

    #Using numpy array to store lower and upper lists as 8bit integers
    lower = np.array(lower,dtype='uint8')
    upper = np.array(upper,dtype='uint8')

    mask = cv2.inRange(hsv, lower, upper) #Specifies range for lower and upper values in hsv format from video given
    #Here, we are masking the image. This includes both the HSV format and the original image.
    output = cv2.bitwise_and(frame,hsv,mask=mask)

    # COunts number of non-zero pixels in video frame
    pixel_number = cv2.countNonZero(mask)
    if int(pixel_number) > 5000:
        Fire_Status += 1

        if Fire_Status >= 1:
            if Alarm_Sound == False:
                play_alarm()
                send_email()
                Alarm_Sound = True

            camera_deque.append(str(datetime.now()))

            amount = amount + 1
            if amount == 100:
                camera_deque.popleft()
                amount = amount - 1
                Alarm_Sound = True

    # if video frames are not captured correctly, break the code since we can't work with incorrect frames
    if ret == False:
        break
    
    #Displays video frame in specified window
    cv2.imshow("Output", output)

    #If specified key is pressed, stop program
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

print(camera_deque)
print(amount)

cv2.destroyAllWindows()
firevid.release()


