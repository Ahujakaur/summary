# AI Text Summarization API

A production-ready FastAPI microservice that provides text summarization capabilities using open-source AI models.

## Features

- Query processing endpoint
- Text summarization using DistilBART
- Async API design
- Comprehensive error handling
- Structured logging
- Docker support
- Unit tests

## Table of Contents

1. [Setup](#setup)
2. [Implementation Steps](#implementation-steps)
3. [API Endpoints](#api-endpoints)
   - [Health Check](#health-check)
   - [Query Processing](#query-processing)
   - [Text Summarization](#text-summarization)
4. [Testing](#testing)
5. [Docker Deployment](#docker-deployment)
6. [Performance Considerations](#performance-considerations)

## Setup

1. Clone the repository:
   ```bash
   git clone <url>
   cd fast_proj
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

4. Build the Docker image:
   ```bash
   docker build -t ai-summarizer .
   ```

5. Run the Docker container:
   ```bash
   docker run -p 8000:8000 ai-summarizer
   ```

## Performance and Limitations

### Inference Latency
- **Model Loading Time**: The initial loading time for the DistilBART model can be significant, especially on the first request. Subsequent requests benefit from the model being cached in memory.
- **Response Time**: The average response time for summarization requests varies depending on the input length. For short texts (less than 500 characters), the response time is typically under 200 milliseconds. For longer texts (up to 10,000 characters), the response time can increase to several seconds, depending on the complexity of the text and the hardware capabilities.
- **Asynchronous Processing**: The FastAPI application is designed to handle requests asynchronously, which helps improve responsiveness under load. However, the actual inference time remains a bottleneck due to the model's complexity.

### Computational Requirements
- **Hardware Requirements**:
  - **CPU**: The application can run on a standard CPU, but inference times will be longer compared to running on a GPU. For production use, it is recommended to deploy on a machine with a dedicated GPU to speed up model inference.
  - **Memory**: The DistilBART model requires a significant amount of RAM (at least 4GB is recommended) to load the model and handle multiple requests efficiently. Insufficient memory may lead to performance degradation or crashes.
  
### Limitations
- **Input Length**: The maximum input length for the summarization model is limited to 10,000 characters. Inputs exceeding this limit will result in an error response. It is advisable to preprocess and truncate text before sending it for summarization.
- **Summary Quality**: While DistilBART provides good summarization results, the quality of the summary may vary based on the complexity and structure of the input text. It may not always capture the most important points, especially in very long or complex documents.
- **Error Handling**: The application includes basic error handling, but edge cases (e.g., extremely short texts or malformed requests) may require additional validation and handling to improve user experience.

### Recommendations for Optimization
- **Batch Processing**: For applications with high throughput requirements, consider implementing batch processing of requests to reduce the overall inference time by processing multiple texts simultaneously.
- **Model Optimization**: Explore options for model quantization or distillation to reduce the model size and improve inference speed without significantly sacrificing accuracy.
- **Caching**: Implement caching mechanisms for frequently requested summaries to reduce redundant processing and improve response times.

By understanding these performance characteristics and limitations, you can better plan for deployment and usage scenarios, ensuring that the application meets user expectations and performs efficiently under various load conditions.

