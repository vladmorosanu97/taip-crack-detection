from services.provider import CnnPredictor


def post(room:dict) -> dict:
    print(room["name"])
    cnn = CnnPredictor(r"C:\Master\TAIP\models\model2.h5")
    result = cnn.get(r"C:\Master\TAIP\test-datasets\cracks\Positive\Screenshot_22.png")
    a = dict()
    a['prediction'] = str(result)
    return a, 200