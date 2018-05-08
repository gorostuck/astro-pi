from sense_hat import SenseHat
import time
import subprocess
import random

sense = SenseHat()

# Constant variables
NAME = 0
TEMP_OPT = 1
TEMP_MIN = 2
TEMP_MAX = 3
HUMI_OPT = 4
HUMI_MIN = 5
HUMI_MAX = 6

STATE_TEMPERATURE = 0
STATE_HUMIDITY = 1
STATE_LIFE = 2
STATE_BEST = 3

# Important variables
selected_species = 0
selected_state = 0
max_species = 0
db = []
current_data= []
change = 0


# General functions
def change_species(num):
  global selected_species
  selected_species += num
  if selected_species == max_species:
    selected_species = 0
  if selected_species == -1:
    selected_species = max_species
  sense.show_message(db[selected_species][NAME], scroll_speed=0.05)
  
def change_state(num):
  global selected_state
  selected_state += num
  if selected_state == 3:
    selected_state = STATE_TEMPERATURE
  if selected_state == -1:
    selected_state = STATE_LIFE

def read_temperature():
  # HERE WE WILL NEED TO CONSIDER THE ERROR !
  cpu_temp = float(subprocess.check_output(['vcgencmd','measure_temp']).decode('utf-8')[5:8])
  read_temp = sense.get_temperature()
  return read_temp - (cpu_temp - read_temp)/3 
  return sense.get_temperature()

def show_score():
  global selected_species
  global selected_state
  global current_data
  color = 0
  score = 0
  if selected_state == STATE_TEMPERATURE:
    score = current_data[selected_species][0][0]
    color = [255, 0, 0]
  if selected_state == STATE_HUMIDITY:
    score = current_data[selected_species][1][0]
    color = [0, 0, 255]
  if selected_state == STATE_LIFE:
    score = (current_data[selected_species][0][0]+current_data[selected_species][1][0])/2
    color = [0, 255, 0]
  
  score_64 = 64*score
  x = 0
  y = 0
  while x <= 7:
    while y <= 7:
      if x*8+y < score_64:
        sense.set_pixel(x,y, color)
      else:
        sense.set_pixel(x,y, 0, 0, 0)
      y+=1
    y=0
    x+=1

def write_data():
  global current_data
  global post_db
  post_db.write(time.ctime()+'\n')
  for species in current_data:
    line = '{:4} {:6} {:4} {:6}\n'.format(round(species[0][0], 2), round(species[0][1], 2), round(species[1][0], 2), round(species[1][1], 2))
    post_db.write(line)
  current_data = []


# Experiment functions
def score_temperature(current_species, temp_ins):
  temp_opt = db[current_species][TEMP_OPT]
  temp_min = db[current_species][TEMP_MIN]
  temp_max = db[current_species][TEMP_MAX]
  score = 0
  if temp_ins < temp_opt and temp_ins > temp_min:
    score = (temp_ins - temp_min)/(temp_opt - temp_min)
  elif temp_ins < temp_max and temp_ins > temp_opt:
    score = (temp_ins - temp_max)/(temp_opt - temp_max)
  return [score, temp_opt - temp_ins]
  
def score_humidity(current_species, humi_ins):
  humi_ins = sense.get_humidity()
  humi_opt = db[current_species][HUMI_OPT]
  humi_min = db[current_species][HUMI_MIN]
  humi_max = db[current_species][HUMI_MAX]
  score = 0
  if humi_ins < humi_opt and humi_ins > humi_min:
    score = (humi_ins - humi_min)/(humi_opt - humi_min)
  elif humi_ins < humi_max and humi_ins > humi_opt:
    score = (humi_ins - humi_max)/(humi_opt - humi_max)
  return [score, humi_opt - humi_ins]

  

# Read the database and gather the info about the species
fc = open('predb.txt').readlines()
for line in fc:
  words = line.split()
  db.append([])
  j=0
  for word in words:
    if j > 0:
      db[max_species].append(float(word))
    else:
      db[max_species].append(word)
    j += 1
  max_species += 1
max_species += -1
post_db = open("postdb.txt", "w")

while True:
  for index, current_species in enumerate(db):
    current_data.append([])
    current_data[index].append(score_temperature(index, read_temperature()))
    current_data[index].append(score_humidity(index, sense.get_humidity()))
  show_score()
  write_data()
  
  for event in sense.stick.get_events():
    if event.action == "released":
      if event.direction == "right":
        change_species(1)
      if event.direction == "left" :
        change_species(-1)
      if event.direction == "down":
        change_state(-1)
      if event.direction == "up":
        change_state(1)
  time.sleep(1)
  change += 1
  if change == 10:
      change = 0
      selected_species = random.randint(0, max_species)
      selected_state   = random.randint(0, 2)
      change_species(0)
      