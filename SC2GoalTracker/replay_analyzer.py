import mpyq
from s2protocol import versions
from os import listdir, path
from multiprocessing import Process, Pool
from datetime import datetime, timedelta
import ast
from replay_stats import replay_stats

class replay_analyzer:
    def __init__(self,replay_folder,player_id):
        self.replay_folder = replay_folder
        self.player_id = player_id
    
    #args used to see if replay is within a week old
    def minutes_in_replay(self,filename,rs,*args): 
        archive = mpyq.MPQArchive(filename)
        contents = str(archive.header['user_data_header']['content'])
        metadata = ast.literal_eval(archive.read_file('replay.gamemetadata.json'))
        #figure out build version of replay
        header = versions.latest().decode_replay_header(contents)
        baseBuild = header['m_version']['m_baseBuild']
        protocol = versions.build(baseBuild)
        
        contents = archive.read_file('replay.initData')
        initData = protocol.decode_replay_initdata(contents)

        #data only matters if it's a 1v1
        if (initData['m_syncLobbyState']['m_gameDescription']['m_gameOptions']['m_competitive'] and initData['m_syncLobbyState']['m_gameDescription']['m_maxPlayers'] == 2):
            contents = archive.read_file('replay.details')
            details = protocol.decode_replay_details(contents)
            
            player_race = ""
            enemy_race = ""
            result = ""
            for player in details['m_playerList']:
                if (player['m_toon']['m_id'] == self.player_id):
                    player_race = player['m_race']
                    for meta_player in metadata['Players']:
                        if meta_player['PlayerID'] == player['m_workingSetSlotId'] + 1:
                            result = meta_player["Result"]
                    
                    #Have to make a copy because nested dicts don't update for Manager dicts
                    contents = archive.read_file('replay.game.events')
                    game_events = protocol.decode_replay_game_events(contents)

                    for event in game_events:
                        if event['_event'] == 'NNet.Game.SGameUserLeaveEvent':
                            #could possible use metadata 'duration'?
                            #possibly more accurate: first player leave vs duration of replay
                            game_duration = (event['_gameloop']/22.44444/60)
                            break  
                    #needs to be done out of / after for loop due to weird behavior with syncing dict
                    minutes_played_today_copy = rs["minutes_played_today"]
                    minutes_played_week_copy = rs["minutes_played_week"]
                    minutes_played_week_copy[player_race] += game_duration
                    if (args):
                        minutes_played_today_copy[player_race] += game_duration
                    rs["minutes_played_today"] = minutes_played_today_copy      
                    rs["minutes_played_week"] = minutes_played_week_copy  
                else:
                    enemy_race = player['m_race']
                    
            #Have to make a copy because nested dicts don't update for Manager dicts
            copy_wins = rs["wins"]
            copy_games = rs["games"]
            if (player_race == "Terran"):
                if (enemy_race == "Terran"):
                    copy_games["TvT"] += 1
                    if (result == "Win"):
                        copy_wins["TvT"] +=1
                elif (enemy_race == "Zerg"):
                    copy_games["TvZ"] += 1
                    if (result == "Win"):
                        copy_wins["TvZ"] +=1
                else:
                    copy_games["TvP"] += 1
                    if (result == "Win"):
                        copy_wins["TvP"] +=1
            elif (player_race == "Zerg"):
                if (enemy_race == "Terran"):
                    copy_games["ZvT"] += 1
                    if (result == "Win"):
                        copy_wins["ZvT"] +=1
                elif (enemy_race == "Zerg"):
                    copy_games["ZvZ"] += 1
                    if (result == "Win"):
                        copy_wins["ZvZ"] +=1
                else:
                    copy_games["ZvP"] += 1
                    if (result == "Win"):
                        copy_wins["ZvP"] +=1
            elif (player_race == "Protoss"):
                if (enemy_race == "Terran"):
                    copy_games["PvT"] += 1
                    if (result == "Win"):
                        copy_wins["PvT"] +=1
                elif (enemy_race == "Zerg"):
                    copy_games["PvZ"] += 1
                    if (result == "Win"):
                        copy_wins["PvZ"] +=1
                else:
                    copy_games["PvP"] += 1
                    if (result == "Win"):
                        copy_wins["PvP"] +=1
            rs["wins"] = copy_wins
            rs["games"] = copy_games       
        return rs
        
    
    def get_already_played(self):    
        rs = replay_stats()
        
        processes = []
        for files in listdir(self.replay_folder):
            if (path.splitext(files)[1] == '.SC2Replay'):
                archive = mpyq.MPQArchive(self.replay_folder +'\\'+ files)
                contents = str(archive.header['user_data_header']['content'])
            
                #figure out build version of replay
                header = versions.latest().decode_replay_header(contents)
                baseBuild = header['m_version']['m_baseBuild']
                protocol = versions.build(baseBuild)
                
                #decode game events
                contents = archive.read_file('replay.details')
                details = protocol.decode_replay_details(contents)
                datetime_of_replay = datetime.utcfromtimestamp(((details['m_timeUTC']) / (10000000) - 11644473600 + ((details['m_timeLocalOffset']) / 10000000)))
                p1 = Process()
                if (datetime_of_replay.date() == datetime.today().date()):
                    p1 = Process(target=self.minutes_in_replay, args=((self.replay_folder +'\\'+ files),rs.replay_stats_dict,True))
                #start of week credit https://stackoverflow.com/questions/39441639/getting-the-date-of-the-first-day-of-the-week?rq=1
                elif(datetime_of_replay.date() >= (datetime.today() - timedelta(days=datetime.today().isoweekday() % 7)).date()):
                    p1 = Process(target=self.minutes_in_replay, args=((self.replay_folder +'\\'+ files),rs.replay_stats_dict))
                
                processes.append(p1)
                p1.start()
        for process in processes:
            process.join()
        return rs.replay_stats_dict
