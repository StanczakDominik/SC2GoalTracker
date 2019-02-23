from random import shuffle

random_messages={
    "winrate":{
        "low":["Anon: hes shit at {MATCHUP}","Anon: {ENEMY_RACE} is OP", "Anon: {ENEMY_RACE} so easy"],
        "medium":["Anon: eh {MATCHUP} isn't his worst", "Anon: {MATCHUP} is such a coinflip"],
        "high":["Anon: {MATCHUP} so ez", "Anon: {MATCHUP} is boring to watch, he only wins lol"]},
    "minutes_played":{
        "low":["Anon: does he even play anymore?","Anon: musta retired","Anon: no wonder he's bad","Anon: can't even hit the play button"],
        "medium":["Anon: hey he's playing again","Anon: wait he didn't die irl?", "Anon: maybe he's making a comeback?","Anon: he's been getting better recently"],
        "high":["Anon: ByuN lvl commitment","Anon: so fun to watch him play","Anon: gosu","Anon: BONJWA!?","Anon: GSL when?", "Anon: Serral's got competition", "Morgana: Aren't you tired?"]},    
    "twitch":{
        "low":["Anon: people still play this game?","Anon: Kappa","Anon: BW master race","Anon: DAE daed gaem?"],
        "medium":["Anon: LUL", "Anon: ezpz","Anon: GG","Anon: glhf","Anon: follow Liquid'Ret on Twitter","Anon: SPAM THIS DORITO"],
        "high":["Anon: I like this guy"]
    }    
}

def get_race(player,matchup):
    matchup_num = 99999
    if (player == "player"):
        matchup_num = 0
        
    elif(player == "enemy"):    
        matchup_num = 2
    else:
        raise ValueError("Invalid player")
    
    if (matchup[matchup_num] == 'T'):
        return "Terran"
    elif (matchup[matchup_num] == 'P'):
        return "Protoss"
    elif(matchup[matchup_num] == 'Z'):
        return "Zerg"
    else:
        raise ValueError("Invalid enemy_race")
     

def get_message_list(played_percentage,matchup_winrate,twitch_messages_on):
    message_list = []
    if (twitch_messages_on):
        if ( played_percentage  < .33):
            message_list += random_messages["minutes_played"]["low"] + random_messages["twitch"]["low"]
        elif (played_percentage < .90):
            message_list += random_messages["minutes_played"]["medium"] + random_messages["twitch"]["medium"]
        elif(played_percentage >=.90):
            message_list += random_messages["minutes_played"]["high"] + random_messages["twitch"]["high"]
    
    #check if dict is empty or not 
    if (bool(matchup_winrate)):
        for matchup in matchup_winrate:
            message_list += ["SYSTEM: " + matchup + " win rate " + str(matchup_winrate[matchup]["percent"]*100) + "% ("+ str(matchup_winrate[matchup]["wins"]) + "/" + str(matchup_winrate[matchup]["games"])+")"]
            win_rate = "none"
            if (matchup_winrate[matchup]["percent"] < .33):
                win_rate= "low"
            elif (matchup_winrate[matchup]["percent"] < .66):
                win_rate= "medium"
            else:
                win_rate ="high"
            if (twitch_messages_on):
                for message in random_messages["winrate"][win_rate]:
                    temp = message
                    if "{MATCHUP}" in temp:
                        temp = temp.replace("{MATCHUP}",matchup)
                    if "{ENEMY_RACE}" in temp:
                        temp = temp.replace("{ENEMY_RACE}",get_race("enemy",matchup))
                        if (get_race("enemy",matchup) == get_race("player",matchup)):
                            temp = ""
                    if "{PLAYER_RACE}" in temp:
                        temp = temp.replace("{PLAYER_RACE}",get_race("player",matchup))
                    if (temp):
                        message_list +=[temp]
    shuffle(message_list)
    #no message (no games played / no twich messages)
    if (not message_list):
        message_list += ["NO","GAMES","PLAYED"]
    message_list += ["SYSTEM: Created by SwordSCII"]
    return message_list