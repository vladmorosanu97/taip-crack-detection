
import connexion
from connexion.resolver import RestyResolver

from services.provider import CnnPredictor

# cnn = CnnPredictor(r"C:\Master\TAIP\models\modeltf")
# print(cnn.get(r"C:\Master\TAIP\test-datasets\cracks\Positive\Screenshot_22.png"))

if __name__ == '__main__':
    app = connexion.App(__name__, port=9090, specification_dir='swagger/')
    app.add_api('my_super_app.yaml', resolver=RestyResolver('api'))
    app.run()