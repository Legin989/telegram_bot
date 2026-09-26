from .person_talk import router as person_talk_router
from .common import router as common_router
from .gpt import router as gpt_router
from .quiz import router as quiz_router
from .random_fact import  router as random_fact_router
#from .translate import router as translate_router
from .recommend import router as recommend_router

routers = [
    person_talk_router,
    common_router,
    gpt_router,
    quiz_router,
    random_fact_router,
    recommend_router,
]