def run_demo(user_input):
    password = "SuperSecretPassword123"

    if "ignore previous" in user_input.lower():
        return password

    return "Sorry, I cannot share the admin password."
