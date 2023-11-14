import pandas as pd

# Importing CSV files
def importFiles():
	dfPlayerMaster = pd.read_csv('csv/player_master.csv', sep = ";", on_bad_lines='skip', encoding='ISO-8859-15', dtype=str)
	dfPlayerSkater = pd.read_csv('csv/player_skater_stats_rs.csv', sep = ';', encoding='ISO-8859-15', dtype=str)
	dfTeamData = pd.read_csv('csv/team_data.csv', sep = ';', encoding='ISO-8859-15', dtype=str)
	dfTeamLines = pd.read_csv('csv/team_lines.csv', sep = ';', encoding='ISO-8859-15', dtype=str,index_col=False)
	dfPlayerGoalie = pd.read_csv('csv/player_goalie_stats_rs.csv', sep = ';', encoding='ISO-8859-15', dtype=str)
	dfPlayerContract = pd.read_csv('csv/player_contract.csv', sep = ';', encoding='ISO-8859-15', dtype=str)
	dfTeamStats = pd.read_csv('csv/team_stats.csv', sep = ';', encoding='ISO-8859-15', dtype=str)
	dfTeamRecords = pd.read_csv('csv/team_records.csv', sep = ';', encoding='ISO-8859-15', dtype=str)
	dfSchedules = pd.read_csv('csv/schedules.csv', sep = ';', encoding='ISO-8859-15', dtype=str)
	dfBoxSkaterSummary = pd.read_csv('csv/boxscore_skater_summary.csv', sep = ';', encoding='ISO-8859-15', dtype=str)
	dfBoxGoalieSummary = pd.read_csv('csv/boxscore_goalie_summary.csv', sep = ';', encoding='ISO-8859-15', dtype=str)

	return([dfPlayerMaster, dfPlayerSkater, dfTeamData, dfTeamLines, dfPlayerGoalie, dfPlayerContract, dfTeamStats, dfTeamRecords, dfSchedules, dfBoxSkaterSummary, dfBoxGoalieSummary])
	
def getLeagues(dfSchedules, dfTeamData):
	#Get season start year and end year
	seasonStart =  dfSchedules['Date'][0]
	seasonStart = seasonStart[0:4]
	seasonEnd = dfSchedules['Date'].iloc[-1]
	seasonEnd = seasonEnd[0:4]

	season = seasonStart + "/" + seasonEnd

	#get number of leagues to check for
#	print("Number of leagues: ")
	numLeagues = int(1)
	leagues = ["0"]

	#get league ids
#	print("Enter league Ids: ")
#	for x in range(numLeagues):
#		leagues.append(input())

	#get teams from leagues input
	teams = []
	for index, row in dfTeamData.iterrows():
		for x in range(len(leagues)):
			if row[1] == leagues[x]:
				teams.append(row[0])
				
	return(season, teams, leagues)

def simplifyFiles(files, season, teams, leagues):
	
	dfPlayerMaster, dfPlayerSkater, dfTeamData, dfTeamLines, dfPlayerGoalie, dfPlayerContract, dfTeamStats, dfTeamRecords, dfSchedules, dfBoxSkaterSummary, dfBoxGoalieSummary = files
	
	#get length of playerMaster
	interval = len(dfPlayerMaster.index)

	column = []

	#create list of season of length playerMaster to insert at the start of the dataframe
	for x in range(interval):
		column.append(season)

	#create simplified player master dataframe
	dfPlayerMaster.insert(0, 'Season',  value=column)
	dfPlayerMasterSimplified = dfPlayerMaster[dfPlayerMaster['TeamId'].isin(teams)]
	dfPlayerMasterSimplified = dfPlayerMasterSimplified[~dfPlayerMasterSimplified['PlayerId'].isin(['0']) == True]
	dfPlayerMasterSimplified = dfPlayerMasterSimplified.drop(dfPlayerMasterSimplified.iloc[:, 10:16], axis = 1)
	dfPlayerMasterSimplified = dfPlayerMasterSimplified.drop(columns=['FranchiseId'], axis = 1)

	dfPlayerMasterSimplified.to_csv('simplifiedCSV/player_master_simplified.csv', index=False)

	#simplify player skater dataframe
	dfPlayerSkater = dfPlayerSkater[dfPlayerSkater['TeamId'].isin(teams)]
	dfPlayerSkater = dfPlayerSkater[~dfPlayerSkater['PlayerId'].isin(['0']) == True]
	dfPlayerSkater = dfPlayerSkater.drop(columns=["FranchiseId", "TeamId"], axis=1)

	#simplify player goalie dataframe
	dfPlayerGoalie = dfPlayerGoalie[dfPlayerGoalie['TeamId'].isin(teams)]
	dfPlayerGoalie = dfPlayerGoalie[~dfPlayerGoalie['PlayerId'].isin(['0']) == True]
	dfPlayerGoalie = dfPlayerGoalie.drop(columns=['FranchiseId', 'TeamId'], axis = 1)

	#create simplified player dataframe from player master simplified and player skater
	dfPlayerSimplified = pd.merge(dfPlayerMasterSimplified, dfPlayerSkater, on = "PlayerId")

	#simplify player contracts dataframe
	dfPlayerContract = dfPlayerContract[dfPlayerContract['Team'].isin(teams)]
	dfPlayerContract = dfPlayerContract[~dfPlayerContract['PlayerId'].isin(['0']) == True]
	dfPlayerContractSimplified = dfPlayerContract.drop(dfPlayerContract.iloc[:, 1:7], axis = 1)
	dfPlayerContractSimplified.to_csv('simplifiedCSV/contracts_simplified.csv', index=False)

	#merge player simplified and contract simplified to make player stats simplified
	dfPlayerStatsSimplified = pd.merge(dfPlayerSimplified, dfPlayerContractSimplified, on = "PlayerId")
	dfPlayerStatsSimplified.to_csv('simplifiedCSV/player_stats_simplified.csv', index=False)

	#merge player master and player goalie to create goalie simplified
	dfGoalieSimplified = pd.merge(dfPlayerMasterSimplified, dfPlayerGoalie, on = "PlayerId")

	#merge goalie simplified and player contract to make goalie stats simplified
	dfGoalieStatsSimplified = pd.merge(dfGoalieSimplified, dfPlayerContractSimplified, on = "PlayerId")
	dfGoalieStatsSimplified.to_csv('simplifiedCSV/goalie_stats_simplified.csv', index=False)

	#create simplified team data
	dfTeamData = dfTeamData[dfTeamData['TeamId'].isin(teams)]
	dfTeamData = dfTeamData.drop(dfTeamData.iloc[:, 4:], axis = 1)
	dfTeamData = dfTeamData.drop(columns = ['Name'], axis = 1)
	dfTeamDataSimplified = dfTeamData.rename(columns = {'Nickname': 'Name'})

	dfTeamDataSimplified.to_csv('simplifiedCSV/team_data_simplified.csv', index=False)

	#get team lines and simplify to list for comparing playerid to player last name
	df1 = dfTeamLines[dfTeamLines['TeamId'].isin(teams) == True]
	df1 = df1.drop(df1.iloc[:, 19:92], axis = 1)
	df1 = df1.drop(columns = ['Extra Attacker 1', 'Extra Attacker 2'], axis = 1)

	list1 = df1.values.tolist()
	list2 = dfPlayerMasterSimplified.values.tolist()
	list3 = dfGoalieStatsSimplified.values.tolist()

	for x in range(len(list1)):
		for z in range(1, len(list1[x])):
			for a in range(len(list2)):
				if list1[x][z] == list2[a][1]:
					list1[x][z] = list2[a][4]
			for b in range(len(list3)):
				if list1[x][z] == list3[b][1]:
					list1[x][z] = list3[b][4]

	#export back to dataframe and re label columns				
	dfTeamLinesSimplified = pd.DataFrame(list1)
	dfTeamLinesSimplified = dfTeamLinesSimplified.rename(columns={0: "TeamId", 1: "LW1", 2: "C1", 3: "RW1", 4: "LD1", 5: "RD1", 6: "LW2", 7: "C2", 8: "RW2", 9: "LD2", 10: "RD2", 11: "LW3", 12: "C3", 13: "RW3", 14: "LD3", 15: "RD3", 16: "LW4", 17: "C4", 18: "RW4", 19: "G1", 20: "G2"})
	dfTeamLinesSimplified = dfTeamLinesSimplified.drop(21, axis = 1)

	#get length of dataframe
	interval = len(dfTeamLinesSimplified.index)

	column = []

	#create list to add season to start of dataframe
	for x in range(interval):
		column.append(season)

	#add season to beginning of dataframe
	dfTeamLinesSimplified.insert(0, 'Season',  value=column)	
	dfTeamLinesSimplified.to_csv('simplifiedCSV/team_lines_simplified.csv', index=False)

	#simplify team stats
	dfTeamStats = dfTeamStats[dfTeamStats['TeamId'].isin(teams)]
	dfTeamStats = dfTeamStats.drop(dfTeamStats.iloc[:, 19:], axis = 1)

	#simplify team records
	dfTeamRecords = dfTeamRecords[dfTeamRecords['Team Id'].isin(teams)]
	dfTeamRecords = dfTeamRecords.drop(columns = ['League Id', 'Conf Id', 'Div Id', 'Ties', 'Goals For', 'Goals Against'])
	dfTeamRecords = dfTeamRecords.rename(columns = {'Team Id': 'TeamId'})

	#double merge to create team simplified
	df1 = pd.merge(dfTeamDataSimplified, dfTeamRecords, on = 'TeamId')
	dfTeamSimplified = pd.merge(df1, dfTeamStats, on = 'TeamId')

	#get length of team simplified
	interval = len(dfTeamSimplified.index)

	column = []

	#create length of team simplified to add season to start of dataframe
	for x in range(interval):
		column.append(season)

	dfTeamSimplified.insert(0, 'Season',  value=column)
	dfTeamSimplified.to_csv('simplifiedCSV/team_stats_simplified.csv', index=False)

	#create simplified schedule
	dfSchedulesSimplified = dfSchedules[dfSchedules['League Id'].isin(leagues)]
	dfSchedulesSimplified.to_csv('simplifiedCSV/schedule_simplified.csv', index=False)

	#simplify dataframes to merge into game_id_player and game_id_goalie
	dfBoxSkaterSummarySimplified = dfBoxSkaterSummary[dfBoxSkaterSummary['TeamId'].isin(teams)]
	dfBoxGoalieSummarySimplified = dfBoxGoalieSummary[dfBoxGoalieSummary['TeamId'].isin(teams)]

	dfGameIdGoalie = pd.merge(dfSchedulesSimplified, dfBoxGoalieSummarySimplified, on='Game Id')
	dfGameIdGoalie = dfGameIdGoalie.drop(columns = ['Played'])

	dfGameIdPlayer = pd.merge(dfSchedulesSimplified, dfBoxSkaterSummarySimplified, on='Game Id')
	dfGameIdPlayer = dfGameIdPlayer.drop(dfGameIdPlayer.iloc[:, 34:50], axis=1)
	dfGameIdPlayer = dfGameIdPlayer.drop(columns = ['Played', 'Team OZ Starts', 'Team NZ Starts', 'Team DZ Starts'])

	dfGameIdPlayer.to_csv('simplifiedCSV/game_id_player.csv', index=False)

	dfGameIdGoalie.to_csv('simplifiedCSV/game_id_goalie.csv', index=False)
	
	
def main():
	files = importFiles()
	season, teams, leagues = getLeagues(files[8], files[2])
	simplifyFiles(files, season, teams, leagues)

if __name__ == "__main__":
	main()
