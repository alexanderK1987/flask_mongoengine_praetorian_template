import mainframe
import flask
import operator
@mainframe.app.route('/apis', methods=['GET'])
def routes():
    rules = []
    for rule in mainframe.app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        rules.append({'endpoint': rule.endpoint, 'methods': methods, 'rule': str(rule)})

    rules = sorted(rules, key=operator.itemgetter('rules')) 
    return flask.jsonify(rules)

