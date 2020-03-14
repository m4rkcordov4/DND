import numpy
import sys
import pandas as pd

def dice_roller(dice_string):
    dice_string = dice_string.replace("-","+-")
    dice = dice_string.split('+')
    val = 0
    for die in dice:

        if die.find("d")>-1:
            ndie = int(die.split("d")[0])
            nsides = int(die.split("d")[1])
            for n in range(ndie):
                roll = numpy.random.randint(1,nsides+1)
                #print('roll',roll)
                val += roll
                #print('total',val)
        else:
            val += int(die)
                
            
        
            
    return val;
    
def d20(mod):
    roll = numpy.random.randint(1,21)
    if roll == 20:
        print("CRIT!")
    if roll == 1:
        print('CRIT FAIL!')
    return roll+int(mod);

def combat():

    df=pd.DataFrame()
    header = ['NAME','INITIATIVE','HP','TURN']
    cmd = ''
    player_name_on = '%FIRST_TURN%'
    while cmd != 'end':
        try:
            show=False
            cmd = input('combat command:')
            row = pd.DataFrame()
            if cmd[0] == '!':
                roll = cmd[1:]
                print(dice_roller(roll))
            if cmd[0] == '*':
         
                mod=cmd[1:]
                    
                if mod == '':
                    mod=0
                print(d20(mod))
            if cmd.find('+p')==0:
                show=True
                name=input('name:')
                ini=input('initiative:')
                hp = 'UNK'
                row['NAME']=[name]
                row['INITIATIVE']=[int(ini)]
                row['HP'] = [hp]
                row['MAX HP']=[hp]
                df = df.append(row)
            if cmd.find('+n')==0:
                show=True
                name=input('name:')
                addstrs = name.split()
                if len(addstrs) > 1:
                    #print(addstrs)
                    nguys = addstrs[1]
                else:
                    nguys = 1
                mod=input('initiative mod:')
                hpi = input('HP:')
                for n in range(int(nguys)):
                    row = pd.DataFrame()
                    ini = d20(mod)
                    
                    if str(hpi).find('d')>-1:
                        hp = dice_roller(hpi)
                    else:
                        hp=int(hpi)
                    row['NAME']=['%s%s' % (addstrs[0],n+1)]
                    row['INITIATIVE']=[ini]
                    row['HP'] = [hp]
                    row['MAX HP']=[hp]
                    df = df.append(row)
            if cmd.find('hl')==0:
                show=True
                hls = cmd.split()
                hlnam = hls[1]
                hlhp = hls[2]
                newhp = int(df.loc[df['NAME']==hlnam,'HP']+int(hlhp))
                if newhp < int(df.loc[df['NAME']==hlnam,'MAX HP']):
                    df.loc[df['NAME']==hlnam,'HP']=newhp
                else:
                    df.loc[df['NAME']==hlnam,'HP']=int(df.loc[df['NAME']==hlnam,'MAX HP'])
                    
                    
                    
                
            if cmd.find('-')==0:
                show=True
                removes= cmd.split()
                removes = removes[1:]
                for remove in removes:
                    df = df.loc[df['NAME']!=remove]
                    
                    
            if cmd.find("dam")>-1:
                show=True
                damname=cmd.split()[1]
                dampnt=cmd.split()[2]
                total_dam = 0
                for dam in dampnt.split('+'):
                    total_dam += int(dam)
                hp_left = int(df.loc[df['NAME']==damname]['HP']-int(total_dam))
                if hp_left < 1:
                    df = df.loc[df['NAME']!=damname]
                    print(damname,'died!')
                else:
                    df.loc[df['NAME']==damname,'HP']=hp_left
                
            if show:
                df=df.sort_values(by=['INITIATIVE'],ascending=False,ignore_index=True)
                print()
                print(df)
            """
            if cmd.find(">")==0:
                if player_name_on == '%FIRST_TURN%':
                    player_name_on = df.iloc[0]['NAME']
                    turn = 0
                else:
                    turn = df.index[df.loc[df['NAME']==player_name_on]].tolist()[0]
                turn_list = [' ']*df.shape[0]
                turn_list[turn] = '*'
                df['ON'] = turn_list
                print(df)
                if player_name_on == df.iloc[df.shape[0]-1]['NAME']:
                    player_name_on = df.iloc[0]['NAME']
                    turn = 0
            """
        except:
            print('INPUT ERR')
    return;
while True:
    cmd = input("command:")
    
    try:
        if cmd[0] == '!':
            roll = cmd[1:]
            print(dice_roller(roll))
        if cmd[0] == '*':
     
            mod=cmd[1:]
                
            if mod == '':
                mod=0
            print(d20(mod))
        if cmd[0] == '#':
            combat()
        if cmd == 'exit':
            break;
    except:
        print("INPUT ERROR")
        print(sys.exc_info()[0])

