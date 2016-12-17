from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
app.config['SWAGGER'] = {
    "headers": [
    ],
    "specs": [
        {
            "version": "1.0.1",
            "title": "UReR's API",
            "endpoint": 'spec',
            "route": '/spec',
            "rule_filter": lambda rule: True  # all in
        }
    ],
    "static_url_path": "/apidocs",
    "static_folder": "swaggerui",
    "specs_route": "/specs"
}
Swagger(app)


@app.route('/recommendations', methods=['GET'])
def basic_action():
    """
    UReR API for recommendations
    ---
    tags:
      - Recommendations
    responses:
      200:
        description: Recommendations

    """
    data = {
        "recommendations": [
            {"social": "Your friends are at shopping mall"},
            {"transportation": "Bus 28 arrives in 5 minutes"},
            {"tourism": "Citadel Stefan cel Mare is at a distance of 1.4 km northeast"}
        ]
    }
    return jsonify(data)


@app.route('/user/socialnetwork/<int:id>', methods=['POST'])
def social_network(id):
    """
    UReR API for user's social network
    ---
    tags:
      - Users
    parameters:
      - name: id
        in: path
        type: int
        required: true
        description: The id of the social network (1 - Facebook ; 2 - Twitter ; 3 - Instagram ; 4 - Quora)
    responses:
      500:
        description: The id is unknown
      200:
        description: The social network
        schema:
          id: social network
          properties:
            id:
              type: int
              description: The social network's id
              default: ok

    """
    social_networks = {
        1: "facebook",
        2: "twitter",
        3: "instagram",
        4: "quora"
    }

    if id not in social_networks:
        return "Invalid id", 500

    return jsonify(social_network=social_networks[id])


@app.route('/user/post/<int:id>/<string:action>', methods=['POST'])
def user_post_action(id, action):
    """
    UReR API for a specific user's post
    ---
    tags:
      - Users
    parameters:
      - name: id
        in: path
        type: int
        required: true
        description: The post id
      - name: action
        in: path
        type: string
        required: true
        description: The action to be taken (swipe, seen)
    responses:
      500:
        description: The action is unknown or the id is inexistent
      200:
        description: A post
        schema:
          id: post
          properties:
            action:
              type: string
              description: The post's action
              default: ok
            id:
              type: int
              description: The post's id
              default: 1

    """
    action = action.lower().strip()
    if action not in ["swipe", "seen"]:
        return "Invalid action for user", 500

    if not 1 <= id <= 100:
        return "The post id is inexistent", 500

    return jsonify(id=id, action=action)


@app.route('/user/location', methods=['POST'])
def user_location():
    """
    UReR API for user's location
    ---
    tags:
      - Users
    parameters:
        - name: long
          in: query
          type: float
          description: the longitude
          default: 25.4
        - name: lat
          in: query
          type: float
          description: the longitude
          default: 18.1
    responses:
      500:
        description: The longitude or latitude are unknown
      200:
        description: The location
        schema:
          id: return_location
          properties:
            long:
              type: float
              description: the longitude
              default: 25.4
            lat:
              type: float
              description: the latitude
              default: 18.3

    """
    longitude = float(request.args.get('long', -1.0))
    latitude = float(request.args.get('lat', -1.0))

    if longitude == -1.0 or latitude == -1.0:
        return "Invalid longitude or latitude", 500

    return jsonify({"long": longitude, "lat": latitude, "status": "Location updated"})


@app.route('/user/interest', methods=['POST'])
def user_interest():
    """
    UReR API for user's interest
    ---
    tags:
      - Users
    parameters:
        - name: interest
          in: query
          type: string
          description: the interest
          default: programming
    responses:
      500:
        description: The interest is unknown
      200:
        description: The interest
        schema:
          id: return_interest
          properties:
            interest:
              type: string
              description: the interest
              default: computer science

    """
    interest = str(request.args.get('interest', None))

    if interest is None:
        return "Invalid interest", 500

    return jsonify({"interest": interest, "status": "Interest updated"})


@app.route('/user/feed', methods=['POST'])
def user_feed():
    """
    UReR API for user's feed
    ---
    tags:
      - Users
    parameters:
        - name: feed
          in: query
          type: string
          description: the feed
          default: feedly.com
    responses:
      500:
        description: The feed is unknown
      200:
        description: The feed
        schema:
          id: return_feed
          properties:
            feed:
              type: string
              description: the feed
              default: feedly.com

    """
    feed = str(request.args.get('feed', None))

    if feed is None:
        return "Invalid feed", 500

    return jsonify({"feed": feed, "status": "Interest updated"})


@app.route('/user/follow/<int:id>', methods=['POST'])
def user_follow_user(id):
    """
    UReR API for follow
    ---
    tags:
      - Users
    parameters:
      - name: id
        in: path
        type: int
        required: true
        description: The id of a user to follow
    responses:
      500:
        description: The id is unknown
      200:
        description: Follow
        schema:
          id: follow
          properties:
            id:
              type: int
              description: The follower's id
              default: 24

    """
    if not 1 <= id <= 100:
        return "The post id is inexistent", 500

    return jsonify({"user": id, "status": "Following"})


@app.route('/user/follow/<int:id>', methods=['DELETE'])
def user_unfollow_user(id):
    """
    UReR API for deleting a followee
    ---
    tags:
      - Users
    parameters:
      - name: id
        in: path
        type: int
        required: true
        description: The id of a user to unfollow
    responses:
      500:
        description: The id is unknown
      200:
        description: Follow
        schema:
          id: follow
          properties:
            id:
              type: int
              description: The follower's id
              default: 24

    """
    if not 1 <= id <= 100:
        return "The post id is inexistent", 500

    return jsonify({"user": id, "status": "Unfollowing"})


app.run(debug=True)
