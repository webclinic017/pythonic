from flask import Blueprint, render_template

plotting_blueprint = Blueprint('live_plotting', __name__)


@plotting_blueprint.route('/')
def index():
    return render_template('liveplot.html', x_window=100)