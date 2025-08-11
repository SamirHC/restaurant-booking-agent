# Restaurant Booking System

## Overview

## Getting Started
Install the source code and navigate to the root directory `/restaurant-booking-agent`.

Create a virtual environment and activate it. On Linux:
```
python -m venv venv
source venv/bin/activate
```
Install the dependencies in the virtual environment:
```
pip install -r requirements.txt
```

A `.env` file in the root directory requires populating the following environment variables:
```
BOOKING_API_BASE_URL = http://localhost:8547
BEARER_TOKEN = <the provided bearer token>
OPENAI_API_KEY = <openai api key with sufficient credits for llm inference using the gpt 4 model>
```

To start the app, run:
```
uvicorn web.main:app
```
The app can be accessed from the browser at `http://localhost:8000`.

## Design Rationale
Code is developed to consume the API provided, using the principles of hexagonal architecture for scalable system design. This provides a clean interface for the remainder of the code to access the restaurant booking information. The potential user actions listed in the specification are represented as enums for the agent to decide the user intent and follow up by requesting for required fields, as necessary. Based on the user input, a data object representing the state is maintained, where this information is extracted from the user input and output in a predefined JSON format using the OpenAI GPT-4 model.

### Frameworks/Tools
- The `langgraph` framework is used for the AI agent development. 
- FastAPI is used for the Python backend.
- The web UI is rendered using Jinja templating and basic HTML.

### Design Decisions and Trade-Offs
Conversation state is maintained in memory for this implementation.
Session cookies are used to distinguish between users.

### Scaling for Production

### Limitations and Potential Improvements
Of course, it would be significantly better to maintain state using a dedicated database rather than maintaining everything in memory. This was considered but due to the time limitations was not implemented.
The benefits provided by concurrency through asynchronous code has not been used here as the main focus was to develop the agent. This would improve the user interface.

### Security Considerations and Implementation Strategies
