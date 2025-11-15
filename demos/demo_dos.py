from time import sleep

request_count = 0
RATE_LIMIT = 5
COOLDOWN = 10  # simulated seconds

def run_demo(user_input):
    global request_count

    request_count += 1

    # Rate limit exceeded
    if request_count > RATE_LIMIT:
        return f"""
        <div style='color:red; font-weight:bold; font-size:18px;'>
            ⚠️ Rate Limit Exceeded
        </div>
        <p style='margin:6px 0;'>
            You have exceeded the allowed number of requests.
        </p>
        <p>Please wait <b>{COOLDOWN} seconds</b> before trying again.</p>
        """

    # Normal response
    return """
    <div style='color:green; font-weight:bold; font-size:18px;'>
         Request processed successfully
    </div>
    """
