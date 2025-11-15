from flask import Flask, request, jsonify, send_from_directory
from demos.demo_prompt_injection import run_demo as run_prompt_injection
from demos.demo_data_leakage import run_demo as run_data_leakage
from demos.demo_insecure_output import run_demo as run_insecure_output
from demos.demo_dos import run_demo as run_dos
from demos.demo_supply_chain import run_demo as run_supply_chain

app = Flask(__name__, static_folder="web")

@app.get("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

# Endpoint to run demos
@app.post("/run_demo")
def run_demo_endpoint():
    data = request.json
    demo_type = data.get("demo")
    user_text = data.get("input")

    if demo_type == "prompt_injection":
        result = run_prompt_injection(user_text)
    elif demo_type == "data_leakage":
        result = run_data_leakage(user_text)
    elif demo_type == "insecure_output":
        result = run_insecure_output(user_text)
    elif demo_type == "dos":
        result = run_dos(user_text)
    elif demo_type == "supply_chain":
        result = run_supply_chain(user_text)
    else:
        result = "Demo not implemented yet."

    return jsonify({"output": result})

if __name__ == "__main__":
    app.run(debug=True)
