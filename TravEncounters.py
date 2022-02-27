from bottle import run, get, post, request # or route
from rpg_tools.PyDiceroll import roll
import os
import logging

__author__ = 'Shawn Driscoll <shawndriscoll@hotmail.com>\nshawndriscoll.blogspot.com'
__version__ = '0.0.1'
__app__ = 'TravEncounters ' + __version__

def app():

    space_encounter_DMs = [3, 2, 1, 0, -1, -4]
    d66_space = [
                ['Alien Derelict (possible salvage)', '<b>Solar flare</b> (1d6 x 100 rads)', 'Asteroid (empty rock)', 'Ore-bearing asteroid (possible mining)', 'Alien vessel (on a mission)', 'Rock hermit (inhabited rock)'],
                ['<b>Pirate</b>', 'Derelict vessel (possible salvage)', 'Space station (1–4: derelict)', 'Comet (may be ancient derelict at its core)', 'Ore-bearing asteroid (possible mining)', 'Ship in distress'],
                ['Pirate', 'Free Trader', '<b>Micrometeorite storm</b> (collision!)', '<b>Hostile vessel</b> (roll again for type)', 'Mining Ship', 'Scout ship'],
                ['Alien vessel (1–3: trader, 4–6: explorer, 6: spy)', 'Space junk (possible salvage)', 'Far Trader', 'Derelict (possible salvage)', 'Safari or science vessel', 'Escape pod'],
                ['Passenger liner', 'Ship in distress', 'Colony ship or passenger liner', 'Scout ship', 'Space station', 'X-boat courier'],
                ['<b>Hostile vessel</b> (roll again for type)', 'Garbage ejected from a ship', 'Medical ship or hospital', 'Lab ship or scout', '<b>Patron</b> (roll on the patron table, page 81)', 'Police ship'],
                ['Unusually daring pirate', 'Noble yacht', 'Warship', 'Cargo vessel', 'Navigational buoy or beacon', 'Unusual ship'],
                ['<b>Collision with space junk</b> (collision!)', 'Automated vessel', 'Free Trader', 'Dumped cargo pod (roll on random trade goods)', 'Police vessel', 'Cargo hauler'],
                ['Passenger liner', 'Orbital factory (roll on random trade goods)', 'Orbital habitat', 'Orbital habitat', 'Communications satellite', 'Defence satellite'],
                ['Pleasure craft', 'Space station', 'Police vessel', 'Cargo hauler', 'System defence boat', 'Grand fleet warship']
                ]

    @get('/encounters')
    def chance():
        return '''<html>
<head>
<title>''' + __app__ + '''</title>
<link href='https://shawndriscollrpg.blogspot.com/favicon.ico' rel='icon' type='image/x-icon'/>
</head>
<body>
<br><br>
<h1>''' + __app__ + '''</h1>
<form action="/space" method="get">
    <input value="In Space" type="submit">
</form>
<form action="/land" method="get">
    <input value="On Land" type="submit">
</form>
</body>
</html>'''

    @get('/space') # or @route('/form')
    def choose_space():
        if roll('d6') == 6:
            return '''<html>
<head>
<title>Choose Space Encounter</title>
<link href='https://shawndriscollrpg.blogspot.com/favicon.ico' rel='icon' type='image/x-icon'/>
</head>
<body>
<br><br>
<h1>Choose Space Encounter</h1>
<form action="/space" method="post">
    Select: <select name="space">
        <option value="1">Highport: The space near an orbital starport</option>
        <option value="2">High-Traffic Space: The space near an industrial world with a high-class starport</option>
        <option value="3">Settled Space: Most core worlds in the Imperium</option>
        <option value="4">Border Systems: Outlying worlds near the border, such as the Spinward Marches</option>
        <option value="5">Wild Space: Amber or Red worlds</option>
        <option value="6">Empty Space: Untravelled space or unexplored systems</option>
    </select>
    <input value="Submit" type="submit" />
</form>
</body>
</html>
'''
        else:
            return '''<html>
<head>
<title>There's No Encounter</title>
<link href='https://shawndriscollrpg.blogspot.com/favicon.ico' rel='icon' type='image/x-icon'/>
</head>
<body>
<br><br>
<h1>There's No Encounter</h1>
</body>
</html>
'''

    @post('/space') # or @route('/example', method='POST')
    def space_chosen():
        select_field_data = request.forms.get('space')
        dm = space_encounter_DMs[int(select_field_data) - 1]
        die1 = roll('d6')
        die2 = roll('d6')
        die1 += dm
        if die1 < 0:
            die1 = 0
        d66_rolled = str(die1) + str(die2)
        print(d66_rolled)
        #print(die1, die2)
        space_encounter = '''<html>
<head>
<title>There's An Encounter</title>
<link href='https://shawndriscollrpg.blogspot.com/favicon.ico' rel='icon' type='image/x-icon'/>
</head>
<body>
<br><br>
<h1>There's An Encounter</h1>
<br><br>
'''
        space_encounter += d66_rolled + ' ' + d66_space[die1][die2 - 1]
        space_encounter += '''
</body>
</html>
'''
        return space_encounter
    
    @get('/land') # or @route('/form')
    def forms():
        if roll('1d') >= 3:
            return '''
                <form action="/land" method="post">
                    Select: <select name="Land">
                        <option value="2">a</option>
                        <option value="3">b</option>
                        <option value="4">c</option>
                        <option value="5">d</option>
                    </select>
                    <input value="Submit" type="submit" />
                </form>
            '''
        else:
            return '''
                Nothing.
            '''
        
    run(host='localhost', port='8080')
    
if __name__ == '__main__':
    
    app()