def main():
	files = importFiles()
	season, teams, leagues = getLeagues(files[8], files[2])
	simplifyFiles(files, season, teams, leagues)
