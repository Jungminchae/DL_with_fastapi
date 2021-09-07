import os
import json
from io import BytesIO
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
import uvicorn
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

model_path = "./model/efn_b0_224_na_5-0.43-0.90.h5"


@app.post("/places/classification")
async def classification(place: UploadFile = File(...)):
    # 기본 uploads 디렉토리에 사진 저장 & 읽기
    save_dir = "./uploads/"
    if os.path.exists(save_dir) is False:
        os.mkdir(save_dir)
    upload_path = save_dir + place.filename
    image = await place.read()
    with open(upload_path, "wb") as f:
        f.write(image)
    place_image = Image.open(BytesIO(image))
    # resize
    place_image = place_image.resize((224, 224))
    # model load
    model = load_model(model_path)
    # label load
    with open("./model/place_55_label.json", "r", encoding="utf-8-sig") as f:
        label_info = json.load(f)
    # prediction
    place_image = np.array(place_image)
    place_image = place_image[np.newaxis, ...]
    pred = model.predict(place_image)
    # pred index
    pred_index = np.argmax(pred)
    pred_index = str(pred_index)

    # label, sentence
    label_sentense = label_info[pred_index]
    label = label_sentense["category"]
    sentence = np.random.choice(label_sentense["sentence"])

    return {"label_name": label, "sentence": sentence}


if __name__ == "__main__":
    uvicorn.run(app, reload=True)
