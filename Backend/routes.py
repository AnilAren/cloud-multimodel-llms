from Azure.azure_gpt_35_turbo import Azure_gpt_35_turbo_Blueprint
from Azure.azure_gpt_4_32k import Azure_Gpt_4_32k_Blueprint
from flask import Flask
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.register_blueprint(Azure_gpt_35_turbo_Blueprint,url_prefix="/azure/gpt-34-turbo")
app.register_blueprint(Azure_Gpt_4_32k_Blueprint,url_prefix="/azure/gpt-4-32k")


if __name__ == '__main__':
    app.run(port=8080,debug=True)