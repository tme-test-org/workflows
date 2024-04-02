import requests
import json
import time
import sys
import os
# from pdfdocument.document import PDFDocument
from pathlib import Path

api_key = os.getenv('COPYAI_API_KEY_v2')
workflow_id = os.getenv('COPYAI_WF_ID_v2')

url = f"https://api.copy.ai/api/workflow/{workflow_id}/run"

cb = Path('tmp/cb.txt').read_text()
ctb = Path('tmp/ctb.txt').read_text()
ctx = Path('tmp/ctx.txt').read_text()

research_statement = Path('tmp/research_statement.txt').read_text()

payload = {
    "startVariables" : {},
    "metadata" : {"api": True},
}
payload["startVariables"]["content_type"] = ctb
payload["startVariables"]["background_prompt"] = """You are a technical content writer for a software vendor called Aviatrix."""
payload["startVariables"]["content_brief"] = cb
payload["startVariables"]["context"] = ctx
payload["startVariables"]["research_statement"] = research_statement

headers = {
	"Content-Type": "application/json",
    "x-copy-ai-api-key": api_key
}

response = requests.post(url, json=payload, headers=headers)


# Parse the response text to a dictionary
response_dict = json.loads(response.text)

if 'data' in response_dict:
    if 'id' in response_dict['data']:
        print("Workflow Run ID: " + response_dict['data']['id'])
    else:
        print("'id' not found in 'data'.")
else:
    print("'data' not found in the response.")


# Extract the run_id
run_id = response_dict['data']['id']

# Create the URL for tracking the workflow run
track_url = f"https://api.copy.ai/api/workflow/{workflow_id}/run/{run_id}"

# Track the response
track_response = requests.get(track_url, headers=headers)


x = True #Build a timeout function. Something like x = time. If time - x = > 5m: break

while True:
    track_response = requests.get(track_url, headers=headers)
    track_response_dict = json.loads(track_response.text)

    if 'data' in track_response_dict:

        if 'status' in track_response_dict['data']:
            status = track_response_dict['data']['status']
            sys.stdout.write('\r' + "Status: " + status + "...")
            sys.stdout.flush()
            if (status == "FAILED" or x == False):
                print("There was an issue obtaining a response from Copy.AI")
                exit(1)

        # Wait for the status to change to 'COMPLETE' and print the output
        if track_response_dict['data']['status'] == 'COMPLETE':
            output_dict = track_response_dict['data']['output']
            if 'use_prompt_input' in output_dict:
                print("\n\n")
                # print("\n\n##############################")
                # print("########### OUTPUT ###########")
                # print("##############################")
                print(output_dict['use_prompt_input'])



                content = output_dict['use_prompt_input']

### MD Generation ###
                with open("output.md", "w") as f:
                    # Add the content to the Markdown file
                    f.write(content)


### PDF GENERATION ###

                # Create a new PDF document
                # pdf = PDFDocument("output.pdf")

                # Add the content to the PDF document
                # pdf.init_report()
                # pdf.h2('Output')
                # pdf.p(content)

                # Save the PDF document
                # pdf.generate()

                #print("Output saved to output.pdf")

            else:
                print("'use_prompt_input' not found in 'output'.")
                print(json.dumps(output_dict, indent=4))
            break

    else:
        print("'data' not found in the response.")

    time.sleep(5)