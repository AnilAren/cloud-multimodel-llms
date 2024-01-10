from openai import AzureOpenAI
import os
from icecream import ic
from dotenv import load_dotenv
load_dotenv()
# Using Sigleton ---> means same object is getting used every time for a session(i.e untill we restart out backend code)

class LLMConfigSingleton:
    _instances = {}

    def __new__(cls, config_name):
        if config_name not in cls._instances:
            cls._instances[config_name] = super(LLMConfigSingleton, cls).__new__(cls)
            cls._instances[config_name].__init__(config_name)
        return cls._instances[config_name]

    def __init__(self,config_name):
        try:
            if not getattr(self, "_initialized", False):
                api_key_var = f'{config_name}_OPENAI_API_KEY'
                endpoint_var = f'{config_name}_OPENAI_API_BASE'
                version_var = f'{config_name}_OPENAI_API_VERSION'
                ic(os.getenv(api_key_var))
                self.llm_instance = AzureOpenAI(
                    api_key=os.getenv(api_key_var),
                    azure_endpoint=os.getenv(endpoint_var),
                    api_version=os.getenv(version_var)
                )
                self._initialized = True
        except Exception as e:
            return {"status_code": 500, "status": "error", "message": str(e)}


def Azure_gpt_config(config_name):
    ic(f"Entering Azure LLM ({config_name})")
    llm_singleton = LLMConfigSingleton(config_name)
    ic(llm_singleton.llm_instance)
    ic(f"Exiting Azure LLM CONFIG ({config_name})")
    return llm_singleton.llm_instance

# Config Settings:
# Azure_GPT_35_turbo 
# Azure_GPT_4_32k