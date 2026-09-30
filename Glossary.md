# Performance Stats
### (SP) Statistical Points
The official statistic used in the UAAP MVP race, which aims to condense the box score statistics into one stat by use of simple weighting systems to account for relative difficulty of a stat. Win bonuses are added when a player plays in a team win, while technical and unsportsmanlike fouls are subtracted.

SP is highly similar to EFF, where counting stats are heavily favored without giving context to pace or team play. SP is also a per-game statistic, and not accumulative over the season.

### (aSP) Adjusted Statistical Points
Personal derivative of SP to take into account games with overtime. SPs are normalized to 200 team minutes per game.

### (USG%) Usage Rate
Estimates the percentage of team possessions 'used' by a player while he is on the floor. A possession is used when the player attempts a field goal, attempts a free throw, or commits a turnover.

USG% is typically used to indicate how many opportunities or touches is given to a player while he is on the floor.

### (EWA) Estimated Wins Added
Estimates the contribution of a player to team success through his statistics and compares it to a 'replacement player' (typically the 12th man on the roster). This is a derivative of PER, adjusting for minutes played.

EWA can indicate the amount of good contribution of a player over the season. Although PER in itself favors highly efficient players regardless of minutes, high EWA can also indicate high-impact players with more minutes. Negative EWA means that the player may perform lower than a replacement player. Moreover, adding the EWA of all players in a team roughly totals to the actual team wins.

*Note: Due to lack of position data, the position replacement level value is simply averaged across the five positions.*

### (PER) Player Efficiency Rating
From John Hollinger, PER estimates the per-minute performance of a player, accounting for the pace of play. This values positive contributions (points, assists, etc.) and penalizes negative contributions (turnovers, missed shots, etc.) before adjusting for pace.

PER is always contextualized over the league's season, such that a league-average PER is always 15.00. In an NBA context, 13+ PER is common for rotation players, 20+ PER is common for all-stars and 25+ PER is common for MVP candidates.

### (WS) Win Shares
From Basketball-Reference, WS aims to 'share' the total team success or wins to each player. In a quick sense, WS uses elaborate formulas to compute the points produced per offensive possession (OWS) and the stops per defensive possession (DWS) to estimate how impactful the player is over the game.

Similar to EWA, WS favors both high-minute and efficient contributors, although no comparison is made to 'replacement level players'. Summing up all WS for a team also roughly totals the actual team wins.

### (GmSc) Game Score
From John Hollinger, GmSc is a simpler version of the PER. It attempts to combine positive and negative contributions into one statistic that is roughly similar in scale to points. No adjustments are made to both minutes and pace, and GmSc is typically a catch-all stat to see how impressive the box score of the player is.

### (EFF) Efficiency
EFF is the simplest performance box score statistic that simply adds all positive basic stats and subtracts all negative basic stats. No weights and adjustments are made.

### (FFI) Four Factors Index
According to Dean Oliver, there are four major factors to basketball success: shooting, turnovers (or rather, taking care of the ball), rebounding and free throws. FFI aims to condense these four factors into one statistic by taking advanced stats for each factor (EFG%, TOR, REB%, FTR; see below for details) and applying weights as fractions of 100% (thus, the scale is from 0-100%).

FFI is mostly used to indicate the biggest factors of the game, although no adjustments are made to minutes or pace. It also highly favors efficient, but not necessarily volume, scorers, while no additions are made for playmakers.

### (PIE) Player Impact Estimate
From NBA, PIE is another catch-all performance stat that aims to adjust for game totals instead of pace. In summary, PIE indicates the percentage of events the player has contributed towards the game. Similar to EFF or GmSc, however, only simple weights are used for each stat. Essentially, PIE is similar to EFF but contextualized over the game totals.

### (AV) Approximate Value
From Dean Oliver, AV is a quick encapsulation of the performance of a player, which is in fact a derivative of EFF. This differentiates itself from EFF by making bigger distinctions from very good, average and poor performances.

### (ORtg) Offensive Rating
Estimates the number of points produced by a player per 100 possessions. Points produced takes into account field goals (direct scoring), assists (indirect scoring), and offensive rebounds (creating more opportunities to score) through various weights and adjustments of individual, team and league statistics. A higher ORtg means the player has produced more points for his teams.

### (Floor%) Floor Percentage
A derivative of ORtg, Floor% estimates the percentage of offensive possessions where the player actually scores or has assisted on.

### (DRtg) Defensive Rating
Estimates the number of points a player has allowed per 100 possessions. This boils down to how many stops the player has induced on defense, taking into account both counting defensive stats (blocks, steals and defensive rebounds) and forced errors on opponents (opponent turnovers and misses). A lower defensive rating indicates that the player is a better individual defender.

### (Stop%) Stop Percentage
A component of DRtg, Stop% estimates the percentage of defensive possessions a player has induced a stop. A higher Stop% means that the player has had more stops.

### (OWS) Offensive Win Shares and (DWS) Defensive Win Shares
The ORtg and DRtg are adjusted to take into account team play and league play. These adjustments are called marginal offense and marginal defense. In a sense, these marginal stats tell how much better the player is compared to league average. The marginal stats are then credited using marginal points per win which takes into account team pace (as more possessions mean more opportunities). OWS and DWS are then added together to form WS. Note that both OWS and DWS may be negative.

# Scoring Stats
### (EFG%) Effective Field Goal %
This is a simple adjustment from the FG% to take into account that three-pointers are worth one more point than a two-pointer. This enables to better estimate the scoring percentage of the player.

### (TS%) True Shooting %
TS% is an extension of EFG%, where free throw attempts are also taken into consideration. Note that a weight is added to free throw attempts, as not all trips to the free throw line are the same.

### (PPWS) Points per Weighted Shot
PPWS is similar to the TS%, but eliminates the 2x factor of the denominator. In essence, this estimates how many points the player will score per shot attempt.

### (FTR) Free Throw Rate
Estimates how aggressive a player is at drawing fouls relative to how many shot attempts were not fouled. A higher FTR could mean that the player is more effective at going to the foul line.

# Playmaking Stats
### (AST/TO) Assist-to-Turnover Ratio
A simple division of the two stats, the AST/TO estimates how good a player is at creating plays for his team while taking care of the ball.

### (AR) Assist Rate
Estimates the percentage of the possessions a player is in where he contributes an assist. This is more dependent on how fast the team plays.

### (TOR) Turnover Rate
Estimates the percentage of the possessions a player is in where he commits a turnover. It actually has a similar formula to AR, with the TO swapped in for AST.

### (pAST%) Assist Percentage
Estimates the percentage of field goals of the team in which the player has assisted on. This is more dependent on how many field goals is actually made by the team.

### (PPR) Pure Point Rating
Condenses the assist and turnover statistic into one and adjusts for pace. PPR can be treated as an adjusted AST/TO.

# Rebounding Stats
### (REB%) Rebounding Percentage
Estimates the percentage of available rebounds a player has grabbed while he is on the floor.

### (OREB%) Offensive Rebounding Percentage
Estimates the percentage of available offensive rebounds (accounted for by either team offensive rebounds or opponent defensive rebounds) a player has grabbed while he is on the floor.

### (DREB%) Defensive Rebounding Percentage
Estimates the percentage of available defensive rebounds (accounted for by either team defensive rebounds or opponent offensive rebounds) a player has grabbed while he is on the floor.

# Team Advanced Stats
### PACE
Estimates how many possessions a team has per game. Possessions, in this case, is computed using box scores only, and thus, is an estimate as well based on field goals, rebounds, and turnovers.

### (OFF) Team Offensive Rating
Estimates the number of points scored by a team per 75 possessions to take into account pace of play.

### (DEF) Team Defensive Rating
Estimates the number of points allowed by a team per 75 possessions to take into account pace of play.

### (NET) Net Rating
Differential between OFF and DEF.

### (HHI) Herfindahl-Hirschman Index
Based from concepts in finance, HHI attempts to measure the scoring balance of a team. A lower HHI means that the points scored by a team is spread more evenly across its players, while a higher HHI indicates that the scoring is more top-heavy.

### (Py-W) Pythagorean Wins
Estimated number of games a team 'should have won' based on the points scored and points allowed. This counteracts the fact that a blowout win counts the same as a close game.
