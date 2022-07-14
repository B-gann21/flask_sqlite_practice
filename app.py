from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://wrwnbkzackdsni:8e88a89fff327947211f69dcc94ef166d24f10c94e14c619a2015d08238655cb@ec2-34-235-198-25.compute-1.amazonaws.com:5432/d6je4or6mi5odn"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)

    def __repr__(self):
        return '<Post %s>' % self.title

class PostSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "content")
        model = Post

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

class PostListResource(Resource):
    def get(self):
        posts = Post.query.all()
        json = []
        counter = 0
        for p in posts:
            data = {
                "id": p.id,
                "title": p.title,
                "content": p.content
            }
            json.append(data)
        return json

    def post(self):
        new_post = Post(
            title=request.json['title'],
            content=request.json['content']
        )
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post)

api.add_resource(PostListResource, '/posts')

class PostResource(Resource):
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post_schema.dump(post)

    def patch(self, post_id):
        post = Post.query.get_or_404(post_id)

        if 'title' in request.json:
            post.title = request.json['title']
        if 'content' in request.json:
            post.content = request.json['content']

        db.session.commit()
        return post_schema.dump(post)

    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return '', 204

api.add_resource(PostResource, '/posts/<int:post_id>')

if __name__ == '__main__':
    app.run(debug=False)

