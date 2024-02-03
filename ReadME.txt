
# Best Practices for API Requests with Language Models (LLMs)

When interacting with Language Models like OpenAI's GPT models, it's essential to adhere to best practices for API requests:

- **POST Requests**: Utilize POST requests for generating text or processing large input data. This approach ensures practicality and security by allowing the inclusion of extensive data within the request body.
  
- **Avoiding Large URLs**: GET requests can result in unwieldy and potentially insecure URLs, especially with substantial data payloads.

## Git Commit Standards

Follow these commit standards to maintain consistency and clarity in your Git commits:

- **feat**: Introduce new features.
- **fix**: Address bug fixes.
- **docs**: Documentation changes, such as README updates.
- **style**: Style or formatting adjustments.
- **perf**: Enhancements related to code performance.
- **test**: Implementation of tests for features.

## Handling JSON in Streamlit Apps

In Streamlit applications, use the `.json()` method to parse HTTP responses formatted in JSON. This functionality facilitates the conversion of JSON data into Python objects, typically dictionaries or lists.

## Azure Implementation

Integrate Azure's GPT-3.5-Turbo and GPT-4-32k models with modularity in mind to accommodate additional models seamlessly. Implement a singleton architecture to instantiate LLM Objects and clients only once for efficiency.

- **LLM Parameters**:
    1. `top_p`
    2. `temperature`
    3. `max_tokens`

For image generation, leverage DALL-E 2.

## AWS Integration

For AWS integration, utilize Boto3, the AWS SDK for Python, to interact with AWS services. Employ Object-Oriented Programming (OOP) to organize models into Cohere, Anthropic, AI21, and Meta categories.

### Cohere
- `cohere.command-text-v14`

### Anthropic
- `anthropic.claude-v1`
- `anthropic.claude-v2`
- `anthropic.claude-instant-v1`

### AI21
- `ai21.j2-ultra-v1`
- `ai21.j2-mid-v1`

### Meta
- `meta.llama2-13b-chat-v1`

Implement a singleton pattern to ensure a single client and object instantiation for each model, enhancing efficiency and resource management.

