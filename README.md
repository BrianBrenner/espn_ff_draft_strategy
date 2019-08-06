# espn_ff_draft_strategy
Allows editing of your draft strategy programmatically with a list of player names.
Uses python 3.5+

## To Use
In order for the script to work, you will need to edit some of the variables.

First login to ESPN's fantasy site and go to your teams homepage. The URL should look something
like: https://fantasy.espn.com/football/team?leagueId=12345&teamId=1&seasonId=2019

Edit the variables `LEAGUE_ID` and `TEAM_ID` to match the leagueId and teamId parameters in the URL.
In the case of the above URL, you would set `LEAGUE_ID = '12345'` and `TEAM_ID = '1'`

Next, open the browser console (ctrl+shift+j on chrome), click on Applications -> Cookies -> https://www.espn.com
You want to look for two values, SWID and espn_s2. Copy and paste these as the variables in the code.
For example:
`SWID = '{asfddf-asdfdf-asdfdf}'`
`espn_s2 = 'fdafdfasdlkfjfjfjfjfjjfjf'`

Finally, how you get the player names into the script is up to you. I would recommend parsing a
text file or CSV. Use the find_id_by_name function and replace the lines:

```
player_id = find_id_by_name(players, 'Texans', 'D/ST')
selected_players = [player_id]
```

with something you write to populate the `selected_players` array.
