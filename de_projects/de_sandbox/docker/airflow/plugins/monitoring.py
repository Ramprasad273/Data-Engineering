
def on_failure_callback(context):
    """
    This function will be called on task failure.
    """
    print(f"Task {context['task_instance_key_str']} failed.")
    # In a real-world scenario, you would send an alert to a Slack channel or other monitoring tool.
