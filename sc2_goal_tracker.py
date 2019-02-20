from kivy.app import App

from kivy.uix.label import Label
from kivy.clock import Clock,mainthread
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Quad,Color,Rectangle
from kivy.config import Config
from kivy.animation import Animation

from watchdog.observers import Observer

from replay_analyzer import replay_analyzer
from replay_stats import replay_stats
from file_observer import file_observer
from win32api import GetSystemMetrics
import message_feed


class TestApp(App):
    def build(self):
        self.load_settings()
        self.replay_analyze = replay_analyzer(self.replay_folder,self.player_id)
        self.message_feed_label = Label(text="",pos = (650,50),font_size='20sp',color=[1,1,1],outline_color=[0,0,0],outline_width=5,markup=True)
        self.anim = Animation(x=700,duration=0.0)+  Animation(x=50,duration=0.3) + Animation(x=50,duration=2) + Animation(x=-700,duration=0.3)
        self.f = FloatLayout()
        self.message_num = 0
        self.percent_played = 0.0
        self.replay_stats = replay_stats(self.main_race,self.main_race_only,self.replay_analyze.get_already_played(),self.today_goal,self.week_goal)
        self.percent_played_label = Label(text="[b][i]" + ("%.1f" % (self.percent_played*100)) + "%[/i][/b]",size=(50,50),pos_hint={"x": .34, 'top':.95},font_size='90sp',color=[1,0,0],outline_color=[0,0,0],outline_width=5,markup=True)
        self.message_feed_label = Label(text="",pos = (650,45),font_size='20sp',color=[1,1,1],outline_color=[0,0,0],outline_width=5,markup=True)
        self.new_percent_played = self.replay_stats.percentage_minute_played()
        self.replay_stats.replay_stats_dict["games"]["tvt"] = 5
        self.message_list = message_feed.get_message_list(self.replay_stats.percentage_minute_played(),self.replay_stats.win_rate_dict(),self.twitch_messages_on)
        self.message_feed_label.bind(size=self.message_feed_label.setter('text_size'))
        self.message_feed_animate()
        self.goal_title = Label(text="[b]Today's goal:[/b]",size=(50,50),pos_hint={"x": -.25, 'top':1.3},font_size='50sp',color=[1,1,1],outline_color=[0,0,0],outline_width=5,markup=True)
        self.minutes_today_label = Label(text="Minutes played today: " + str("%.2f" % self.replay_stats.total_minutes_played('today')) +  "(Goal:" + str(self.replay_stats.minute_goal_today) + ")",pos=(20,18))
        self.minutes_today_label.bind(size=self.minutes_today_label.setter('text_size'))
        self.minutes_week_label = Label(text="Minutes played this week: " + str("%.2f" % self.replay_stats.total_minutes_played('this_week')) +  "(Goal:" + str(self.replay_stats.minute_goal_week) + ")",pos=(20,0))
        self.minutes_week_label.bind(size=self.minutes_week_label.setter('text_size'))

        with self.f.canvas:
            #create border
            Color(1,1,1,1)
            Quad(points=[45,80,40,130,460,137,455,75])
            Color(0,0,0,1)
            Quad(points=[48,83,45,123,445,125,445,80])
            #percentage bar
            Color(1,0,0,1)
            self.percent_played_bar = Rectangle(pos=(55,90),size=((385*(self.replay_stats.percentage_minute_played())),28))
        self.f.add_widget(self.percent_played_label)
        self.f.add_widget(self.goal_title)
        self.f.add_widget(self.minutes_today_label)
        self.f.add_widget(self.minutes_week_label)
        self.f.add_widget(self.message_feed_label)
        Window.add_widget(self.f)
        Window.size = (700,200)
        if (self.auto_anchor):
            Window.left = GetSystemMetrics(0) - Window.width + self.auto_anchor_left_right_offset  if self.auto_anchor_corner.split(" ")[1] == "right" else 0 + self.auto_anchor_left_right_offset
            Window.top = (GetSystemMetrics(1) - Window.height - 40 + self.auto_anchor_bottom_top_offset) if self.auto_anchor_corner.split(" ")[0] == "bottom" else 0 + self.auto_anchor_bottom_top_offset
        observer = Observer()
        observer.schedule(file_observer(self.update), self.replay_folder, recursive=True)
        observer.start()
        Clock.schedule_once(self.increase_percent, 0.01)
    
       
    def load_settings(self):
        settings_file = open("settings.SC2GT","r")
        for line in settings_file:
            contents = line.split("=")
            contents[1] = contents[1].replace("\n","")
            if contents[0] == "[main_race_only]":
                self.main_race_only = validate_bool(contents[1])
            elif(contents[0] == "[main_race]"):
                self.main_race = validate_race(contents[1])
            elif(contents[0] == "[player_id]"):
                self.player_id = int(contents[1])
            elif(contents[0] == '[twitch_messages_on]'):    
                self.twitch_messages_on = validate_bool(contents[1])
            elif(contents[0] == '[replay_folder]'):
                self.replay_folder = contents[1]
            elif(contents[0] == '[today_goal]'):
                self.today_goal = int(contents[1])
            elif(contents[0] == '[week_goal]'):
                self.week_goal = int(contents[1])
            elif(contents[0] == "[auto_anchor]"):
                self.auto_anchor = validate_bool(contents[1])
            elif(contents[0] == "[auto_anchor_corner]"):
                self.auto_anchor_corner = validate_corner(contents[1])
            elif(contents[0]=="[auto_anchor_left_right_offset]"):
                self.auto_anchor_left_right_offset = int(contents[1])
            elif(contents[0]=="[auto_anchor_bottom_top_offset]"):
                self.auto_anchor_bottom_top_offset = int(contents[1])
        settings_file.close()
                
        
    def message_feed_animate(self,*args):
        self.message_feed_label.text = self.message_list[self.message_num]        
        self.message_num = self.message_num+1 if self.message_num < len(self.message_list)-1 else 0
        self.anim = Animation(x=700,duration=0.0)+  Animation(x=50,duration=0.3) + Animation(x=50,duration=2) + Animation(x=-700,duration=0.3)
        self.anim.bind(on_complete=self.message_feed_animate)
        self.anim.start(self.message_feed_label)
    
    def increase_percent(self,dt):
        if (self.percent_played < self.new_percent_played-0.001):
            self.percent_played += 0.001
            self.percent_played_label.text = "[b][i]" + ("%.1f" % (self.percent_played*100)) + "%[/i][/b]"
            self.percent_played_bar.size = ((385*(self.percent_played),28))
            Clock.schedule_once(self.increase_percent,0.01)
        
    @mainthread
    def update(self, *args,**kwargs):
        try:
            if ('new_replay' in kwargs):
                self.anim.cancel(self.message_feed_label)
                #in case percent animation was still going
                self.percent_played_label.text = "[b][i]" + ("%.1f" % (self.new_percent_played*100)) + "%[/i][/b]"
                self.percent_played = self.new_percent_played
                #assume new replay is from today
                self.replay_stats.replay_stats_dict = self.replay_analyze.minutes_in_replay(kwargs['new_replay'],self.replay_stats.replay_stats_dict,True)  
                self.minutes_today_label.text = "Minutes played today: " + str("%.2f" % self.replay_stats.total_minutes_played('today')) +  "(Goal:" + str(self.replay_stats.minute_goal_today) + ")"  
                self.minutes_week_label.text = "Minutes played this week: " + str("%.2f" % self.replay_stats.total_minutes_played('this_week')) +  "(Goal:" + str(self.replay_stats.minute_goal_week) + ")"
                self.new_percent_played = self.replay_stats.percentage_minute_played()
                self.message_list = message_feed.get_message_list(self.replay_stats.percentage_minute_played(),self.replay_stats.win_rate_dict(),self.twitch_messages_on)
                self.message_feed_animate()
                Clock.schedule_once(self.increase_percent, 0.01)
        except Exception as e:
            Window.add_widget(Label(text=(
                e.message if getattr(e, r'message', None) else str(e)
            )))

#bad that I have to duplicate this
def validate_bool(value):
    if (value == "False"):
        return False
    elif (value == "True"):
        return True
    else:
        raise ValueError("Invalid parameter " + value)
    
def validate_corner(value):
    if (value == "bottom left" or value == "bottom right" or value == "top left" or value == "top right"):
        return value
    else:
        raise ValueError("Invalid parameter " + value)

def validate_race(value):
    if (value == "Terran" or value == "Protoss" or value == "Zerg"):
        return value
    else:
        raise ValueError("Invalid parameter " + value)

if __name__ == '__main__':   
    #bad that I have to duplicate this
    settings_file = open("settings.SC2GT","r")
    for line in settings_file:
        contents = line.split("=")
        contents[1] = contents[1].replace("\n","")
        if (contents[0] == "[auto_anchor]" and validate_bool(contents[1])):
            Config.set('graphics', 'fullscreen', 'fake')
            
    test = TestApp();
    #put down here cause kivy and multiprocessing seems like it doesnt play together well
    from kivy.core.window import Window
    test.run()
