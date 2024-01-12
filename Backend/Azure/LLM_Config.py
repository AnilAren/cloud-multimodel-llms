from openai import AzureOpenAI
import os
from icecream import ic
from dotenv import load_dotenv
load_dotenv()
# Using Sigleton ---> means same object is getting used every time for a session(i.e untill we restart out backend code)

class LLMConfigSingleton:
    _instances = None

    def __new__(cls, ):
        if  not cls._instances:
            cls._instances = super(LLMConfigSingleton, cls).__new__(cls)
            cls._instances.__init__()
        return cls._instances

    def __init__(self):
        try:
            if not getattr(self, "_initialized", False):
                api_key_var = "AZURE_OPENAI_API_KEY" 
                endpoint_var = 'AZURE_OPENAI_API_BASE'
                version_var = 'AZURE_OPENAI_API_VERSION'
                ic(os.getenv(api_key_var))
                self.llm_instance = AzureOpenAI(
                    api_key=os.getenv(api_key_var),
                    azure_endpoint=os.getenv(endpoint_var),
                    api_version=os.getenv(version_var)
                )
                self._initialized = True
        except Exception as e:
            return {"status_code": 500, "status": "error", "message": str(e)}


def Azure_gpt_config():
    ic("Entering Azure LLM ")
    llm_singleton = LLMConfigSingleton()
    ic(llm_singleton.llm_instance)
    ic("Exiting Azure LLM CONFIG")
    return llm_singleton.llm_instance

if __name__ == '__main__':
    for i in range(10):
        print(Azure_gpt_config())
