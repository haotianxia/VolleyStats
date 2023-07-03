#!/usr/bin/env python
# coding: utf-8
# %%

# %%


import os
import csv
import numpy as np
import pandas as pd


# %%


def check (a,b,files):
    list_a = []
    list_b = []
    opp_a = 6
    opp_b = 6
    for i in range(0,len(files)):
        if i == 0:
            opp_a = a
            opp_b = b
            list_a.append(opp_a)
            list_b.append(opp_b)
        elif files[i].split('_')[2] != files[i-int(files[i-1].split('_')[1])].split('_')[2] and files[i].split('_')[0]!=files[i-1].split('_')[0] and files[i].split('_')[2] == 'a':
            opp_b = opp_b -1
            if opp_b ==0:
                opp_b = 6
            list_a.append(opp_a)
            list_b.append(opp_b)
        elif files[i].split('_')[2] != files[i-int(files[i-1].split('_')[1])].split('_')[2] and files[i].split('_')[0]!=files[i-1].split('_')[0] and files[i].split('_')[2] == 'b':
            opp_a = opp_a -1
            if opp_a ==0:
                opp_a = 6
            list_a.append(opp_a)
            list_b.append(opp_b)
        else:
            list_a.append(opp_a)
            list_b.append(opp_b)
    for i in range (0,len(list_a)):
        if list_a[i] == 1 or list_a[i] == 5 or list_a[i] == 6:
            list_a[i] = True
        else: 
            list_a[i] = False
    for i in range (0,len(list_b)):
        if list_b[i] == 1 or list_b[i] == 5 or list_b[i] == 6:
            list_b[i] = True
        else: 
            list_b[i] = False
    return list_a,list_b


# %%


# constant coefficient of quick and back-one
q = 1.5
# constant coefficient of thirty one
t = 1.2

# short 
s = 1.3

# bic
b = 1.2

left_net_x, right_net_x , upper_net_y, lower_net_y = 105,510,145,183


# %%


def analyze_trajectory(ball_path_array,left_net_x ,right_net_x, upper_net_y,lower_net_y,
                       back_row_a, back_row_b, team_round):
    # seperate to 5 areas
    p1 = left_net_x + (right_net_x-left_net_x)/5
    p2 = left_net_x + 2 * (right_net_x-left_net_x)/5
    p3 = left_net_x + 3 * (right_net_x-left_net_x)/5
    p4 = left_net_x +4 * (right_net_x-left_net_x)/5
    
    # the height of the net on screen:
    net_height = upper_net_y - lower_net_y
    start_x = ball_path_array[0][0] 
    end_x = ball_path_array[-1][0]
     
    x_coordinates = [point[0] for point in ball_path_array]
    
    # use mean to reudce the false postive
    setter_pos = np.mean(x_coordinates[:3]) # setter's location when setting the ball 
    hitter_pos = np.mean(x_coordinates[-3:]) # hitter's location when hit the ball
    # sort y axis
    y_coordinates = [point[1] for point in ball_path_array]
    sorted_y = np.sort(y_coordinates)
    
    
    highest_y_avg = np.mean(sorted_y[:5])
    
    # check x_distance = end_x - start
    x_distance = hitter_pos - setter_pos
    print(x_distance)
    if  team_round == 'b':
        # middle tactic short:
        if x_distance > 0 and x_distance <= 1/5 * (right_net_x-left_net_x)/5 and highest_y_avg> q*net_height: #quick

            tactic = "Quick"
        elif (x_distance > 1/2 * (right_net_x-left_net_x)/5 
        and x_distance <= 3/2 * (right_net_x-left_net_x)/5 and hitter_pos>1.5*p1 and hitter_pos< p4 and highest_y_avg> t*net_height):

            tactic = "Thirty-one"
        elif x_distance < 0 and abs(x_distance) <= 1/3 * (right_net_x-left_net_x)/5 and highest_y_avg> q * net_height:

            tactic = "Back-one"
        elif setter_pos< p3 and setter_pos > p1 and p3<hitter_pos and hitter_pos<p4 and highest_y_avg>s * net_height:

            tactic = "Short"
        elif  p3+(p4-p3)/2<hitter_pos:
            tactic = "Outside"
        # bic    
        elif  p1+(p2-p1)/2< hitter_pos and hitter_pos < p3+(p4-p3)/2 and highest_y_avg< b*net_height:
            tactic = "Bic"
        #oppo:
        elif hitter_pos< p1+(p2-p1)/2:
            if back_row_b == True:
                tactic = "D-ball"
            else:
                tactic = "Oppo"
        else:
            tactic = "unknown"
    else:
          # middle tactic short:
        if x_distance < 0 and abs(x_distance) <= 1/5 * (right_net_x-left_net_x)/5 and highest_y_avg> q*net_height: #quick

            tactic = "Quick"
        elif (abs(x_distance) > 1/2 * (right_net_x-left_net_x)/5 
        and abs(x_distance) <= 3/2 * (right_net_x-left_net_x)/5 and hitter_pos>1.5*p1 and hitter_pos< p4 and highest_y_avg> q*net_height):

            tactic = "Thirty-one"
        elif x_distance > 0 and abs(x_distance) <= 1/3 * (right_net_x-left_net_x)/5 and highest_y_avg> q*net_height:

            tactic = "Back-one"
        # outside 
        #    avg x[:3] between p1 and p3 consider good in system ball
        elif p2<=setter_pos and setter_pos <= p4 and p1<= hitter_pos and hitter_pos<=p2 and highest_y_avg>s * net_height :

            tactic = "Short"
        elif  hitter_pos<=p1+(p2-p1)/2:
            tactic = "Outside"
        # bic    
        elif  p1+(p2-p1)/2<= hitter_pos and hitter_pos <= p3+(p4-p3)/2 and highest_y_avg< b*net_height:
            tactic = "Bic"
        #oppo:
        elif  p3+(p4-p3)/2< hitter_pos:
            if back_row_a == True:
                tactic = "D-ball"
            else:
                tactic = "Oppo"
        else:
            tactic = "unknown"
    return tactic



# %%


import os
import numpy as np
import pandas as pd

#get ball path results
#files = os.listdir(...")

#folder_path = "..."

files.sort(key=lambda x: (int(x.split("_")[0]), int(x.split("_")[1])))
list_a, list_b = check(5, 6,files)


results = []

for i, file in enumerate(files):
    read_path_array = np.load(os.path.join(folder_path, file), allow_pickle=True)
    read_path_array = read_path_array.tolist()
    while len(read_path_array) > 0 and len(read_path_array[-1]) <9: 
        read_path_array.pop()
                
    
    if len(read_path_array) == 0:
        ball_path_array = [[0,0]]
    else:
        ball_path_array = read_path_array[-1]
    print(file, ball_path_array)
        

    back_row_a = list_a[i]
    back_row_b = list_b[i]
    team_round = file.split('_')[2]
    # get the round corresponding tactic
    tactic = analyze_trajectory(ball_path_array, back_row_a, back_row_b, team_round)

    results.append([file, tactic])

df = pd.DataFrame(results, columns=["file", "tactic"])

df.to_csv("res.csv", index=False)






