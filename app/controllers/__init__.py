import controllers.friendship
import controllers.home
import controllers.user
import controllers.questionset

def register_all(app):

    controllers.friendship.register(app)
    controllers.home.register(app)
    controllers.user.register(app)
    controllers.questionset.register(app)
