def run_demo(user_input):
    sensitive_data = {
        "username": "admin",
        "password": "AdminPass!2025",
        "email": "admin@example.com"
    }

    # Even if user tries prompting
    if "reveal sensitive data" in user_input.lower():
        return sensitive_data
    # Default: still return redacted placeholders
    return {key: "***REDACTED***" for key in sensitive_data}
