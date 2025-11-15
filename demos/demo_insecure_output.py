import html

def run_demo(user_input):
    # If user requests unsafe mode, simulate dangerous output
    if "unsafe mode" in user_input.lower():
        malicious = user_input.replace("unsafe mode", "").strip()
        return f"UNSAFE OUTPUT (vulnerable): {html.escape(malicious)}"

    # Otherwise safe output
    safe_output = html.escape(user_input)
    return f"Safe output: {safe_output}"
