from multiprocessing import Manager

class replay_stats(object):

    def __init__(self,main_race = 'Terran',main_race_only = 'True',replay_stats_param = None, minute_goal_today = 50, minute_goal_week = 840):
        manager = Manager()
        if replay_stats_param is None:
            self.replay_stats_dict = manager.dict({
            "games":{
                "TvP":0,
                "TvT":0,
                "TvZ":0,
                "ZvP":0,
                "ZvT":0,
                "ZvZ":0,
                "PvP":0,
                "PvT":0,
                "PvZ":0},
            "wins":{
                "TvP":0,
                "TvT":0,
                "TvZ":0,
                "ZvP":0,
                "ZvT":0,
                "ZvZ":0,
                "PvP":0,
                "PvT":0,
                "PvZ":0},
            "minutes_played_today":{
                "Terran":0.0,
                "Zerg":0.0,
                "Protoss":0.0
                },
            "minutes_played_week":{
                "Terran":0.0,
                "Zerg":0.0,
                "Protoss":0.0
                }
            })
        else:
            self.replay_stats_dict = replay_stats_param
        self.minute_goal_today = minute_goal_today
        self.minute_goal_week = minute_goal_week

        self.main_race = main_race
        self.main_race_only = main_race_only
    
    def get_race(self,matchup):
        if (matchup[0] == 'T'):
            return "Terran"
        elif (matchup[0] == 'P'):
            return "Protoss"
        elif(matchup[0] == 'Z'):
            return "Zerg"
        else:
            raise ValueError("Invalid enemy_race")
        
    def win_rate_dict(self):
        dict_to_return = {}
        for matchup in self.replay_stats_dict["games"]:
            if self.replay_stats_dict["games"][matchup] != 0:
                if ((self.main_race_only and self.get_race(matchup) == self.main_race) or (not self.main_race_only)):
                    dict_to_return[matchup] = {"percent": self.replay_stats_dict["wins"][matchup] / float(self.replay_stats_dict["games"][matchup]), "wins": self.replay_stats_dict["wins"][matchup], "games":self.replay_stats_dict["games"][matchup]}
                
        return dict_to_return
    
    
    @property            
    def replay_stats_dict(self):
        return self._replay_stats_dict
    
    @replay_stats_dict.setter
    def replay_stats_dict(self, new_stats):
        self._replay_stats_dict = new_stats
      
    @property
    def minute_goal_today(self):
        return self._minute_goal_today
    
    @minute_goal_today.setter
    def minute_goal_today(self,value):
        self._minute_goal_today = value
    
    @property
    def minute_goal_week(self):
        return self._minute_goal_week
    
    @minute_goal_week.setter
    def minute_goal_week(self,value):
        self._minute_goal_week = value
    
    @property
    def main_race(self):
        return self._main_race
    
    @main_race.setter
    def main_race(self,value):
        self._main_race = value
    
    @property
    def main_race_only(self):
        return self._main_race_only
    
    @main_race_only.setter
    def main_race_only(self,value):
        self._main_race_only = value
     
    def percentage_minute_played(self):
        if (self.main_race_only):
            return self.replay_stats_dict['minutes_played_today'][self.main_race]/self.minute_goal_today
        else:
            return (self.replay_stats_dict["minutes_played_today"]["Terran"] + self.replay_stats_dict["minutes_played_today"]["Protoss"] + self.replay_stats_dict["minutes_played_today"]["Zerg"])/self.minute_goal_today
                
    def total_minutes_played(self,timeline):
        time = ''
        if (timeline == 'today'):
            time = 'minutes_played_today'
        elif (timeline == 'this_week'):
            time="minutes_played_week"
        else:
            raise ValueError("Invalid timeline")           
            
        if (self.main_race_only):
            return self.replay_stats_dict[time][self.main_race]
        else:
            return self.replay_stats_dict[time]["Terran"] + self.replay_stats_dict[time]["Protoss"] + self.replay_stats_dict[time]["Zerg"]

    