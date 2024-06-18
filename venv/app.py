import requests
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = "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"

# Function to get the mechanism of action from RxClass API
def get_mechanism_of_action(drug_name):
    url = f"https://rxnav.nlm.nih.gov/REST/rxclass/class/byDrugName.json?drugName={drug_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'rxclassDrugInfoList' in data:
            for item in data['rxclassDrugInfoList']['rxclassDrugInfo']:
                if 'minConcept' in item and 'className' in item['minConcept']:
                    return item['minConcept']['className']
        return "No mechanism of action found."
    else:
        return "Error fetching data from RxClass API."

# Function to generate GPT prompt
def generate_prompt(drug_name):
    mechanism = get_mechanism_of_action(drug_name)
    prompt = f"The mechanism of action of {drug_name} is: {mechanism}"
    return prompt

# Function to call GPT-4
def get_gpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

@app.route('/drug-info', methods=['POST'])
def drug_info():
    data = request.get_json()
    drug_name = data.get('drug_name', 'Aspirin')
    prompt = generate_prompt(drug_name)
    gpt_response = get_gpt_response(prompt)
    return jsonify({'response': gpt_response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
