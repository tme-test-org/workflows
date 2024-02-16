# Prompt Multiplexor

This Python script is used to interact with the Copy.ai API. It sends a request to the API and outputs the response in several formats.

## Setup

- Setup and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

- Install the required Python packages:

```bash
pip install -r requirements.txt
```

- Set your Copy.ai API key and workflow ID an environment variables:

```bash
export COPYAI_API_KEY="your-api-key"
export COPYAI_WF_ID="your-workflow-id"
```

## Usage

Run the script with Python:

```bash
python3 prompt_mux.py
```

The script will send a request to the Copy.ai API and print the status of the request. When the status changes to 'COMPLETE', it will print the output to your shell, a Markdown file and a PDF file.
