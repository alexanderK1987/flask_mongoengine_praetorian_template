import mainframe
import flask

@mainframe.app.route('/apis', methods=['GET'])
def routes():
    rules = []
    for rule in mainframe.app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        rules.append({'endpoint': rule.endpoint, 'methods': methods.split(','), 'rule': str(rule)})

    return flask.jsonify(rules)

