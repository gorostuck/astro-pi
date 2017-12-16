from sense_hat import SenseHat

sense = SenseHat()

def experimento_temperatura(t_o, t_min, t_max):
    q = 0
    t = sense.get_temperature()
    if t > t_min and t < t_o:
        q = (t-t_min)/(t_o-t_min)
    elif t < t_max and t > t_o:
        q = (t-t_max)/(t_o-t_max)
    return(q)  
  
while True:
    print(experimento_temperatura(35, 5, 45))
