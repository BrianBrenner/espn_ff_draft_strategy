#!/usr/bin/env python3
import json
import requests


def get_players():
    res = requests.get(
        'https://fantasy.espn.com/apis/v3/games/ffl/seasons/2019/segments/0/leagues/{}?scoringPeriodId=0&view=kona_player_info'.format(LEAGUE_ID),
        cookies={
            'SWID': SWID,
            'espn_s2': espn_s2
        }
    )

    assert res.status_code == 200, 'Unable to fetch player data'

    players = res.json()['players']
    simple_players = [p['player'] for p in players]

    return simple_players


def find_id_by_name(players, first_name, last_name):
    player = [p for p in players
              if p['firstName'].lower() == first_name.lower() and p['lastName'].lower() == last_name.lower()]

    if len(player) == 0:
        raise Exception('Unable to find player with name ' + first_name + ' ' + last_name)
    if len(player) > 1:
        raise Exception('Multiple players with name ' + first_name + ' ' + last_name)

    return player[0]['id']


# selected players is an array of ID's
def format_post_data(all_players, selected_players):
    player_ids = [p['id'] for p in all_players]

    non_selected = [{"playerId": p_id} for p_id in player_ids if p_id not in selected_players]
    formatted_selected = [{"playerId": p_id} for p_id in selected_players]

    assert len(formatted_selected) + len(non_selected) == len(player_ids)

    payload = {
        'draftStrategy': {
            'draftList': formatted_selected + non_selected
        }
    }

    return json.dumps(payload)


def update_rankings(payload):
    res = requests.post(
        'https://fantasy.espn.com/apis/v3/games/ffl/seasons/2019/segments/0/leagues/{}/teams/{}'.format(LEAGUE_ID, TEAM_ID),
        data=payload,
        headers={'Content-Type': 'application/json'},
        cookies={
            'SWID': SWID,
            'espn_s2': espn_s2
        },
    )

    assert res.status_code == 200, 'Unable to update rankings: ' + res.text


if __name__ == "__main__":
    # Get these by going ESPN's fantasy site, then open the console (ctrl+shift+j on chrome),
    # click on Applications -> Cookies -> https://www.espn.com
    # Copy and paste their value as strings here.
    # ex:
    # SWID = '{asfddf-asdfdf-asdfdf}'
    # espn_s2 = 'fdafdfasdlkfjfjfjfjfjjfjf'
    SWID = ''
    espn_s2 = ''

    # Get this by going to your league's home on the fantasy site and looking at the URL.
    # if the URL was http://fantasy.espn.com/football/league?leagueId=12345
    # https://fantasy.espn.com/football/team?leagueId=12345&teamId=1&seasonId=2019
    # then the league id is '12345' and team id is 1
    LEAGUE_ID = ''
    TEAM_ID = ''

    assert len(SWID) > 0 and len(espn_s2) > 0, 'You must enter your SWID and espn_s2 cookie. Read the comments for instructions'
    assert len(LEAGUE_ID) > 0, 'You must enter your league id. Read the comments for instructions'

    # Gets player data, we need these so we can map from player name to player id
    players = get_players()

    # Create array of player ids here using the find_id_by_name funciton.
    # You could do this with a csv or txt file
    # NOTE: for defenses first name is the team name and last name is D/ST
    # ex: 'Texans', 'D/ST'

    # The next two lines should get replaced by your own function
    player_id = find_id_by_name(players, 'Texans', 'D/ST')
    selected_players = [player_id]

    payload = format_post_data(players, selected_players)
    update_rankings(payload)

    print('Updated succesfully!')
