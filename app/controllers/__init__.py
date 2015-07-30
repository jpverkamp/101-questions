import controllers.campaign
import controllers.home
import controllers.user
import controllers.questionset

def register_all(app):

    controllers.campaign.register(app)
    controllers.home.register(app)
    controllers.user.register(app)
    controllers.questionset.register(app)
