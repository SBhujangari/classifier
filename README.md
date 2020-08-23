# Doom or Animal Crossing?

## AI based classification between Doom and Animal Crossing subreddits from images and titles

### Demo
- https://www.youtube.com/watch?v=3CjeY-TyJSI

### Requirements
- Python 3.7.4, NPM

### Files explanation
- Inside of the API folder, `api.py` contains the frontend code written in Flask
- The peddie.py file has all of the model inference code, where we pass a string and an image to make predictions on
- All model training is done in [our Kaggle notebook](https://devpost.com/software/animal-crossing-or-doom-this-ai-will-tell-you?ref_content=user-portfolio&ref_feature=in_progress), which can be accessed by clicking the link.

### How to use
- Download the models from [our Kaggle notebook](https://devpost.com/software/animal-crossing-or-doom-this-ai-will-tell-you?ref_content=user-portfolio&ref_feature=in_progress) (This also has all of our training code for the models)
- Clone our GitHub repo, and put the models inside of the folder
- Execute in terminal `pip install -r requirements.txt`
- Finally, `execute npm run flask-start-api`

Trained using an Nvidia Tesla P100 provided by Kaggle.
