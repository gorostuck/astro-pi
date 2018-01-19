from sense_hat import SenseHat

sense = SenseHat()

def experimento_temperatura():
    q = 0
    f = open('predb.txt')
    l = f.read().split()
    t_o = float(l[1])
    t_min = float(l[2])
    t_max = float(l[3])

    t = sense.get_temperature()
    if t > t_min and t < t_o:
        q = (t-t_min)/(t_o-t_min)
    elif t < t_max and t > t_o:
        q = (t-t_max)/(t_o-t_max)
    f.close()
    return(q)  
    
  
while True:
    print(experimento_temperatura())
