def register_teams():
    teams = []
    team_count = int(input("Enter number of teams: "))
    while team_count < 2:
        raise ValueError("At least 2 teams are required.")
    for i in range(team_count):
        team_name = input("Enter team name: ").strip()
        while team_name == "" or team_name.lower() in [name.lower() for name in teams]:
            print("Team name cannot be empty or repeated")
            team_name = input("Enter a different team name: ").strip()
        teams.append(team_name)
    return teams
def play_match(teams, stats, match_count):
    team1 = input("Enter first team: ").strip()
    team2 = input("Enter second team: ").strip()
    if team1 not in teams or team2 not in teams:
        print("Invalid team name")
        return False
    if team1 == team2:
        print("A team cannot play against itself")
        return False
    if team1 < team2:
        pair = (team1, team2)
    else:
        pair = (team2, team1)
    if match_count.get(pair, 0) >= 2:
        print("These teams have already played twice")
        return False

    try:
        runs1 = int(input("Enter runs scored by " + team1 + ": "))
        wickets1 = int(input("Enter wickets lost by " + team1 + ": "))
        overs1 = int(input("Enter completed overs by " + team1 + ": "))
        extra1 = int(input("Enter remaining balls by " + team1 + ": "))

        runs2 = int(input("Enter runs scored by " + team2 + ": "))
        wickets2 = int(input("Enter wickets lost by " + team2 + ": "))
        overs2 = int(input("Enter completed overs by " + team2 + ": "))
        extra2 = int(input("Enter remaining balls by " + team2 + ": "))
    except ValueError:
        print("Enter valid integer values")
        return False
    if runs1 < 0 or runs2 < 0:
        print("Runs cannot be negative")
        return False
    if wickets1 < 0 or wickets1 > 10 or wickets2 < 0 or wickets2 > 10:
        print("Wickets must be between 0 and 10")
        return False
    if overs1 < 0 or overs1 > 20 or overs2 < 0 or overs2 > 20:
        print("Overs must be between 0 and 20")
        return False
    if extra1 < 0 or extra1 > 5 or extra2 < 0 or extra2 > 5:
        print("Remaining balls must be between 0 and 5")
        return False
    if (overs1 == 20 and extra1 > 0) or (overs2 == 20 and extra2 > 0):
        print("No extra balls are allowed after 20 overs")
        return False

    balls1 = overs1 * 6 + extra1
    balls2 = overs2 * 6 + extra2
    if balls1 == 0 or balls2 == 0:
        print("Each team must face at least one ball")
        return False
    balls_for_rate1 = balls1
    balls_for_rate2 = balls2
    if wickets1 == 10:
        balls_for_rate1 = 120
    if wickets2 == 10:
        balls_for_rate2 = 120

    stats[team1]["matches_played"] += 1
    stats[team2]["matches_played"] += 1

    stats[team1]["runs_scored"] += runs1
    stats[team1]["runs_conceded"] += runs2
    stats[team1]["balls_faced"] += balls_for_rate1
    stats[team1]["balls_bowled"] += balls_for_rate2

    stats[team2]["runs_scored"] += runs2
    stats[team2]["runs_conceded"] += runs1
    stats[team2]["balls_faced"] += balls_for_rate2
    stats[team2]["balls_bowled"] += balls_for_rate1
    if runs1 > runs2:
        stats[team1]["won"] += 1
        stats[team1]["points"] += 2
        stats[team2]["lost"] += 1
        print(team1 + " won the match")
    elif runs2 > runs1:
        stats[team2]["won"] += 1
        stats[team2]["points"] += 2
        stats[team1]["lost"] += 1
        print(team2 + " won the match")
    else:
        stats[team1]["tied"] += 1
        stats[team2]["tied"] += 1
        stats[team1]["points"] += 1
        stats[team2]["points"] += 1
        print("The match is tied")
    match_count[pair] = match_count.get(pair, 0) + 1
    return True

def show_points_table(teams, stats):
    points_table = []
    for team in teams:
        faced = stats[team]["balls_faced"]
        bowled = stats[team]["balls_bowled"]
        if faced > 0 and bowled > 0:
            run_rate = (stats[team]["runs_scored"] * 6 / faced) - (stats[team]["runs_conceded"] * 6 / bowled)
        else:
            run_rate = 0
        points_table.append([team, run_rate])

    for i in range(len(points_table)):
        for j in range(len(points_table) - i - 1):
            team1 = points_table[j][0]
            team2 = points_table[j + 1][0]
            if stats[team1]["points"] < stats[team2]["points"] or (stats[team1]["points"] == stats[team2]["points"] and points_table[j][1] < points_table[j + 1][1]):
                points_table[j], points_table[j + 1] = points_table[j + 1], points_table[j]
    print("Position Team Matches Won Lost Tied Points RunsScored RunsGiven OversFaced OversBowled NRR")
    position = 1
    for row in points_table:
        team = row[0]
        faced = stats[team]["balls_faced"]
        bowled = stats[team]["balls_bowled"]
        overs_faced = str(faced // 6) + "." + str(faced % 6)
        overs_bowled = str(bowled // 6) + "." + str(bowled % 6)
        print(position, team, stats[team]["matches_played"], stats[team]["won"], stats[team]["lost"], stats[team]["tied"], stats[team]["points"], stats[team]["runs_scored"], stats[team]["runs_conceded"], overs_faced, overs_bowled, f"{row[1]:.3f}")
        position += 1
teams = register_teams()

stats = {}
for team in teams:
    stats[team] = {"matches_played": 0, "won": 0, "lost": 0, "tied": 0, "points": 0, "runs_scored": 0, "runs_conceded": 0, "balls_faced": 0, "balls_bowled": 0}
match_count = {}
total_matches = len(teams) * (len(teams) - 1)
played_matches = 0
while played_matches < total_matches:
    if play_match(teams, stats, match_count):
        played_matches += 1
complete = True
for i in range(len(teams)):
    for j in range(i + 1, len(teams)):
        if teams[i] < teams[j]:
            pair = (teams[i], teams[j])
        else:
            pair = (teams[j], teams[i])

        if match_count.get(pair, 0) != 2:
            complete = False
if complete:
    print("Tournament completed successfully")
    show_points_table(teams, stats)
else:
    print("Tournament is incomplete")
