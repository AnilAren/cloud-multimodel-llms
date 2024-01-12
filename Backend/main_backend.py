from Azure.azure_gpt import Azure_GPT_Blueprint
from Azure.azure_dall_e_2 import Azure_Image_Blueprint
from AWS.aws_routes import AWS_text_llm_Blueprint
from flask import Flask
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.register_blueprint(Azure_GPT_Blueprint,url_prefix="/azure")
app.register_blueprint(Azure_Image_Blueprint, url_prefix="/azure/image")
app.register_blueprint(AWS_text_llm_Blueprint, url_prefix = '/aws')


if __name__ == '__main__':
    app.run(port=8080,debug=True)