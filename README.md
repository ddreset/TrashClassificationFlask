## A Simple Flask Application for Trash Classification

Try this demo [here](https://trash-recognition.herokuapp.com/).
***
### What I did:
1. Retained Inception-v3 with [Garbage classification](https://www.kaggle.com/asdasdasasdas/garbage-classification).
2. Modified TensorFlow example to accept Base64 String.
3. Added human friendly GUI to read images from url or devices.
(4. Deployed on Heroku, that's why there are Gemfiles) 
***
To run it on windows:
```
set FLASK_APP=webapp.py
set FLASK_ENV=development
flask run
```
Human friendly GUI：http://localhost:5000/

Model:Inception-v3

__Note:__ label_image.py is from [TensorFlow Example](https://raw.githubusercontent.com/tensorflow/tensorflow/master/tensorflow/examples/label_image/label_image.py)

Dataset:[Garbage classification](https://www.kaggle.com/asdasdasasdas/garbage-classification)

