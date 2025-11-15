def run_demo(user_input):
    """
    Supply Chain Vulnerabilities Demo
    Checks if the input mentions any unsafe third-party libraries.
    Returns a structured, readable warning or a safe message.
    """
    unsafe_libraries = ["unverified_model_v1", "deprecated_model_xyz"]
    detected = []

    for lib in unsafe_libraries:
        if lib.lower() in user_input.lower():
            detected.append(lib)

    if detected:
        # If one or more unsafe libraries detected, return a formatted warning
        warning_msg = "<strong style='color:red'>⚠️ Warning: Unsafe library detected:</strong><ul>"
        for lib in detected:
            warning_msg += f"<li>{lib}</li>"
        warning_msg += "</ul>"
        return warning_msg

    # Safe case
    return "<span style='color:green'>✅ No supply chain vulnerabilities detected.</span>"
