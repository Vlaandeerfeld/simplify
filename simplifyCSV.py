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
	dfBoxGameSummary = pd.read_csv('csv/boxscore_summary.csv', sep = ';', encoding='ISO-8859-15', dtype=str)
	dfBoxScoringSummary = pd.read_csv('csv/boxscore_period_scoring_summary.csv', sep = ';', encoding='ISO-8859-15', dtype=str)
	dfBoxPenaltiesSummary = pd.read_csv('csv/boxscore_period_penalties_summary.csv', sep = ';', encoding='ISO-8859-15', dtype=str)
	dfPlayerRatings = pd.read_csv('csv/player_ratings.csv', sep = ';', encoding='ISO-8859-15', dtype=str)
	dfConferences = pd.read_csv('csv/conferences.csv', sep = ';', encoding='ISO-8859-15', dtype=str)
	dfDivisions = pd.read_csv('csv/divisions.csv', sep = ';', encoding='ISO-8859-15', dtype=str)
	dfLeague = pd.read_csv('csv/league_data.csv', sep = ';', encoding='ISO-8859-15', dtype=str)

	return([dfPlayerMaster, dfPlayerSkater, dfTeamData, dfTeamLines, dfPlayerGoalie, dfPlayerContract, dfTeamStats, dfTeamRecords, dfSchedules, dfBoxSkaterSummary, dfBoxGoalieSummary, dfBoxGameSummary, dfBoxScoringSummary, dfBoxPenaltiesSummary, dfPlayerRatings, dfConferences, dfDivisions, dfLeague])
	
def getLeagues(dfSchedules, dfTeamData):
	#Get season start year and end year
	seasonStart =  dfSchedules['Date'][0]
	seasonStart = seasonStart[0:4]
	seasonEnd = dfSchedules['Date'].iloc[-1]
	seasonEnd = seasonEnd[0:4]

	season = seasonStart + "/" + seasonEnd

	#get number of leagues to check for
	print("Number of leagues: ")
	numLeagues = int(input())
	leagues = []

	#get league ids
	print("Enter league Ids: ")
	for x in range(numLeagues):
		leagues.append(input())

	#get teams from leagues input
	teams = []
	for index, row in dfTeamData.iterrows():
		for x in range(len(leagues)):
			if row[1] == leagues[x]:
				teams.append(row[0])
				
	return(season, teams, leagues)

def simplifyFiles(files, season, teams, leagues):
	
	dfPlayerMaster, dfPlayerSkater, dfTeamData, dfTeamLines, dfPlayerGoalie, dfPlayerContract, dfTeamStats, dfTeamRecords, dfSchedules, dfBoxSkaterSummary, dfBoxGoalieSummary, dfBoxGameSummary, dfBoxScoringSummary, dfBoxPenaltiesSummary, dfPlayerRatings, dfConferences, dfDivisions, dfLeague = files
	
	#get length of playerMaster
	interval = len(dfPlayerMaster.index)

	column = []

	#create list of season of length playerMaster to insert at the start of the dataframe
	for x in range(interval):
		column.append(season)

	dfConferencesSimplified = dfConferences[dfConferences['League Id'].isin(leagues)] 
	
	dfDivisionsSimplified = dfDivisions[dfDivisions['League Id'].isin(leagues)]
	dfDivisionsSimplified = dfDivisionsSimplified.drop(columns=["Conference Id"], axis=1)
	
	dfLeagueSimplified = dfLeague[dfLeague['LeagueId'].isin(leagues)]
	dfLeagueSimplified = dfLeagueSimplified.rename(columns={'LeagueId': 'League Id', 'Name': 'NameLeague', 'Abbr': 'LeagueAbbr'})

	dfConferenceDivisionSimplified = pd.merge(dfConferencesSimplified, dfDivisionsSimplified, on = "League Id", suffixes = ('Conference', 'Division'))
	dfConferenceDivisionLeagueSimplified = pd.merge(dfConferenceDivisionSimplified, dfLeagueSimplified, on = 'League Id')

	interval1 = len(dfConferenceDivisionLeagueSimplified.index)
	column1 = []

	for x in range(interval1):
		column1.append(season)

	dfConferenceDivisionLeagueSimplified.insert(0, 'Season',  value=column1)

	dfConferenceDivisionLeagueSimplified.to_csv('simplifiedCSV/league.csv', index=False)

	#create simplified player master dataframe
	dfPlayerMaster.insert(0, 'Season',  value=column)
	dfPlayerMasterSimplified = dfPlayerMaster[dfPlayerMaster['TeamId'].isin(teams)]
	dfPlayerMasterSimplified = dfPlayerMasterSimplified[~dfPlayerMasterSimplified['PlayerId'].isin(['0']) == True]
	dfPlayerMasterSimplified = dfPlayerMasterSimplified.drop(dfPlayerMasterSimplified.iloc[:, 10:16], axis = 1)
	dfPlayerMasterSimplified = pd.merge(dfPlayerMasterSimplified, dfPlayerRatings, on = "PlayerId")

	dfPlayerMasterSimplified.to_csv('simplifiedCSV/players.csv', index=False)

	#simplify player skater dataframe
	dfPlayerSkater = dfPlayerSkater[dfPlayerSkater['TeamId'].isin(teams)]
	dfPlayerSkater = dfPlayerSkater[~dfPlayerSkater['PlayerId'].isin(['0']) == True]
	dfPlayerSkater = dfPlayerSkater.drop(columns=["FranchiseId", "TeamId"], axis=1)

	#simplify player goalie dataframe
	dfPlayerGoalie = dfPlayerGoalie[dfPlayerGoalie['TeamId'].isin(teams)]
	dfPlayerGoalie = dfPlayerGoalie[~dfPlayerGoalie['PlayerId'].isin(['0']) == True]
	dfPlayerGoalie = dfPlayerGoalie.drop(columns=["FranchiseId", 'TeamId'], axis = 1)

	#create simplified player dataframe from player master simplified and player skater
	dfPlayerSimplified = pd.merge(dfPlayerMasterSimplified, dfPlayerSkater, on = "PlayerId")

	#simplify player contracts dataframe
	dfPlayerContract = dfPlayerContract[dfPlayerContract['Team'].isin(teams)]
	dfPlayerContract = dfPlayerContract[~dfPlayerContract['PlayerId'].isin(['0']) == True]
	dfPlayerContractSimplified = dfPlayerContract.drop(dfPlayerContract.iloc[:, 6:7], axis = 1)

	#get length of dataframe
	interval1 = len(dfPlayerContractSimplified.index)

	column1 = []

	#create list to add season to start of dataframe
	for x in range(interval1):
		column1.append(season)

	dfPlayerContractSimplified.insert(0, 'Season',  value=column1)	
	dfPlayerContractSimplified.to_csv('simplifiedCSV/contract.csv', index=False)

	#merge player simplified and contract simplified to make player stats simplified
	dfPlayerSimplified = dfPlayerSimplified.drop(columns=['Season'], axis = 1)

	dfPlayerStatsSimplified = pd.merge(dfPlayerSimplified, dfPlayerContractSimplified, on = "PlayerId")

	#merge player master and player goalie to create goalie simplified
	dfGoalieSimplified = pd.merge(dfPlayerMasterSimplified, dfPlayerGoalie, on = "PlayerId")

	#merge goalie simplified and player contract to make goalie stats simplified
	dfGoalieSimplified = dfGoalieSimplified.drop(columns=['Season'], axis = 1)
	dfGoalieSimplified = dfGoalieSimplified.drop(columns=['FranchiseId'], axis = 1)

	dfGoalieStatsSimplified = pd.merge(dfGoalieSimplified, dfPlayerContractSimplified, on = "PlayerId")

	#create simplified team data
	dfTeamDataSimplified = dfTeamData[dfTeamData['TeamId'].isin(teams)]

	#get length of dataframe
	interval2 = len(dfTeamDataSimplified.index)

	column2 = []

	#create list to add season to start of dataframe
	for x in range(interval2):
		column2.append(season)

	dfTeamDataSimplified.insert(0, 'Season',  value=column2)

	dfTeamDataSimplified.to_csv('simplifiedCSV/teams.csv', index=False)

	#get team lines and simplify to list for comparing playerid to player last name

	dfTeamDataSimplified1 = dfTeamDataSimplified.drop(columns = ['Season', 'Name'], axis = 1)
	dfTeamLines = pd.merge(dfTeamDataSimplified1, dfTeamLines, on = "TeamId")

	df1 = dfTeamLines[dfTeamLines['TeamId'].isin(teams) == True]
	df1 = df1.drop(df1.iloc[:, 20:93], axis = 1)
	df1 = df1.drop(columns = ['Extra Attacker 1', 'Extra Attacker 2'], axis = 1)

	list1 = df1.values.tolist()
	list2 = dfPlayerMasterSimplified.values.tolist()
	list3 = dfGoalieStatsSimplified.values.tolist()

	for x in range(len(list1)):
		for z in range(2, len(list1[x])):
			for a in range(len(list2)):
				if list1[x][z] == list2[a][1]:
					list1[x][z] = list2[a][5]

			for b in range(len(list3)):
				if list1[x][z] == list3[b][1]:
					list1[x][z] = list3[b][5]

	#export back to dataframe and re label columns				
	dfTeamLinesSimplified = pd.DataFrame(list1)
	dfTeamLinesSimplified = dfTeamLinesSimplified.rename(columns={0: "TeamId", 1: "FranchiseId", 2: "LW1", 3: "C1", 4: "RW1", 5: "LD1", 6: "RD1", 7: "LW2", 8: "C2", 9: "RW2", 10: "LD2", 11: "RD2", 12: "LW3", 13: "C3", 14: "RW3", 15: "LD3", 16: "RD3", 17: "LW4", 18: "C4", 19: "RW4", 20: "G1", 21: "G2"})

	dfTeamLinesSimplified = dfTeamLinesSimplified.drop(22, axis = 1)

	#get length of dataframe
	interval = len(dfTeamLinesSimplified.index)

	column = []

	#create list to add season to start of dataframe
	for x in range(interval):
		column.append(season)

	#add season to beginning of dataframe
	dfTeamLinesSimplified.insert(0, 'Season',  value=column)	
	dfTeamLinesSimplified.to_csv('simplifiedCSV/team_lines.csv', index=False)

	#simplify team stats
	dfTeamStats = dfTeamStats[dfTeamStats['TeamId'].isin(teams)]
	dfTeamStats = dfTeamStats.drop(dfTeamStats.iloc[:, 19:], axis = 1)

	#simplify team records
	dfTeamRecords = dfTeamRecords[dfTeamRecords['Team Id'].isin(teams)]
	dfTeamRecords = dfTeamRecords.drop(columns = ['League Id', 'Conf Id', 'Div Id'])
	dfTeamRecords = dfTeamRecords.rename(columns = {'Team Id': 'TeamId'})

	#double merge to create team simplified
	df1 = pd.merge(dfTeamDataSimplified, dfTeamRecords, on = 'TeamId')
	dfTeamSimplified = pd.merge(df1, dfTeamStats, on = 'TeamId')

	#create simplified schedule
	dfSchedulesSimplified = dfSchedules[dfSchedules['League Id'].isin(leagues)]
	dfBoxGameSummarySimplified1 = dfBoxGameSummary[dfBoxGameSummary['Team Home'].isin(teams)]
	dfBoxGameSummarySimplified2 = dfBoxGameSummary[dfBoxGameSummary['Team Away'].isin(teams)]
	dfBoxGameSummarySimplified = pd.concat([dfBoxGameSummarySimplified1, dfBoxGameSummarySimplified2], ignore_index = True)
	dfBoxScoringSummarySimplified = dfBoxScoringSummary[dfBoxScoringSummary['TeamId'].isin(teams)]
	dfBoxPenaltiesSummarySimplified = dfBoxPenaltiesSummary[dfBoxPenaltiesSummary['TeamId'].isin(teams)]

	dfBoxGameSummarySimplified = dfBoxGameSummarySimplified.drop(columns = ['Team Home', 'Team Away', 'Score Home', 'Score Away', 'Date Year', 'Date Month', 'Date Day', 'Type'])
	dfBoxScoringSummarySimplified = dfBoxScoringSummarySimplified.drop(columns = ['TeamId'])
	dfBoxPenaltiesSummarySimplified = dfBoxPenaltiesSummarySimplified.drop(columns = ['TeamId'])

	dfSchedulesGameSimplified = pd.merge(dfSchedulesSimplified, dfBoxGameSummarySimplified, on = "Game Id")
	dfSchedulesGameScoringSimplified = pd.merge(dfSchedulesGameSimplified, dfBoxScoringSummarySimplified, on = "Game Id")
	dfSchedulesGameScoringPenaltiesSimplified = pd.merge(dfSchedulesGameScoringSimplified, dfBoxPenaltiesSummarySimplified, on = "Game Id",  suffixes = ('OnGoal', 'OnPenalty'))

	dfSchedulesGameScoringPenaltiesSimplified['HomeSQ0SQ1SQ2SQ3SQ4'] = dfSchedulesGameScoringPenaltiesSimplified[dfSchedulesGameScoringPenaltiesSimplified.columns[50:54]].apply(lambda x: ','.join(x.dropna().astype(str)), axis=1)
	dfSchedulesGameScoringPenaltiesSimplified['AwaySQ0SQ1SQ2SQ3SQ4'] = dfSchedulesGameScoringPenaltiesSimplified[dfSchedulesGameScoringPenaltiesSimplified.columns[55:60]].apply(lambda x: ','.join(x.dropna().astype(str)), axis=1)

	dfSchedulesGameScoringPenaltiesSimplified = dfSchedulesGameScoringPenaltiesSimplified.drop(dfSchedulesGameScoringPenaltiesSimplified.iloc[:, 50:60], axis = 1)

	print(dfSchedulesGameScoringPenaltiesSimplified.columns)

	dfSchedulesGameScoringPenaltiesSimplified.to_csv('simplifiedCSV/games.csv', index=False)

	#simplify dataframes to merge into game_id_player and game_id_goalie
	dfBoxSkaterSummarySimplified = dfBoxSkaterSummary[dfBoxSkaterSummary['TeamId'].isin(teams)]
	dfBoxGoalieSummarySimplified = dfBoxGoalieSummary[dfBoxGoalieSummary['TeamId'].isin(teams)]

	dfGameIdGoalie = pd.merge(dfSchedulesSimplified, dfBoxGoalieSummarySimplified, on='Game Id')
	dfGameIdGoalie = dfGameIdGoalie[~dfGameIdGoalie['Played'].isin(['0']) == True]
	dfGameIdGoalie = dfGameIdGoalie.drop(columns = ['Played', 'Home', 'Score Home', 'Away', 'Score Away', 'Overtime', 'Shootout'])

	dfGameIdPlayer = pd.merge(dfSchedulesSimplified, dfBoxSkaterSummarySimplified, on='Game Id')
	dfGameIdPlayer = dfGameIdPlayer.drop(dfGameIdPlayer.iloc[:, 34:50], axis=1)
	dfGameIdPlayer = dfGameIdPlayer[~dfGameIdPlayer['Played'].isin(['0']) == True]
	dfGameIdPlayer = dfGameIdPlayer.drop(columns = ['Played', 'Home', 'Score Home', 'Away', 'Score Away', 'Overtime', 'Shootout', 'Team OZ Starts', 'Team NZ Starts', 'Team DZ Starts'])

	dfGameIdPlayer.to_csv('simplifiedCSV/player_stats.csv', index=False)

	dfGameIdGoalie.to_csv('simplifiedCSV/goalie_stats.csv', index=False)

def main():
	files = importFiles()
	season, teams, leagues = getLeagues(files[8], files[2])
	simplifyFiles(files, season, teams, leagues)

if __name__ == "__main__":
	main()
