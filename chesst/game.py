from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import string
from werkzeug.exceptions import abort

from chesst.auth import login_required
from chesst.db import get_db

bp = Blueprint('game', __name__)

@bp.route('/')
def index():
    db = get_db()
    games = db.execute("""
        SELECT 
            g.id,
            title,
            played_on,
            author.first_name,
            author.last_name,
            white.first_name AS white_first_name,
            white.last_name AS white_last_name,
            black.first_name AS black_first_name,
            black.last_name AS black_last_name
        FROM game g 
           JOIN player author ON g.author_id = author.id
           JOIN player white ON g.player_white = white.id
           JOIN player black ON g.player_black = black.id
        ORDER BY created DESC
    """
    ).fetchall()
    return render_template('game/list.html', games=games)


@bp.route('/<game_id>')
def game(game_id):
    board_marking_x = list(string.ascii_uppercase[:8])
    board_marking_y = [i for i in range(1, 9)]
    board_marking_y.reverse()

    db = get_db()
    game = db.execute("""
        SELECT 
            g.id AS id,
            title,
            played_on,
            white.first_name AS white_first_name,
            white.last_name AS white_last_name,
            black.first_name AS black_first_name,
            black.last_name AS black_last_name
        FROM game g
           JOIN player white ON g.player_white = white.id
           JOIN player black ON g.player_black = black.id
        ORDER BY created DESC
    """).fetchone()

    moves = db.execute(f"""
        SELECT
            number,
            notation
        FROM move
        WHERE
            move.game_id = {game['id']}
    """).fetchall()

    moves_view = []
    for index, move in enumerate(moves):
        is_white_move = index % 2 == 0
        view_index = int(index/2)

        if (is_white_move):
            moves_view.append({'white': move['notation'], 'white_comment': '', 'black': '', 'black_comment': ''})
        else:
            moves_view[view_index]['black'] = move['notation']

    return render_template(
        'game/game.html',
        player_1=game['white_last_name'] + ' ' + game['white_first_name'][0] + '.',
        player_2=game['black_last_name'] + ' ' + game['black_first_name'][0] + '.',
        board_marking_x = board_marking_x,
        board_marking_y = board_marking_y,
        moves=moves_view,
    )

@bp.route('/create')
def create():
    # create new game in db
    #redirect to game
    return