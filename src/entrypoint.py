import os
import subprocess
import json
import requests
import uuid

def set_multiline_output(name, value):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        delimiter = uuid.uuid1()
        print(f'{name}<<{delimiter}', file=fh)
        print(value, file=fh)
        print(delimiter, file=fh)

def parse_inputs():
    env = os.environ

    file_or_dir = env.get('INPUT_YAMLLINT_FILE_OR_DIR', '')
    strict = '--strict' if env.get('INPUT_YAMLLINT_STRICT') in ['1', 'true'] else ''
    config_filepath = f"--config-file {env['INPUT_YAMLLINT_CONFIG_FILEPATH']}" if 'INPUT_YAMLLINT_CONFIG_FILEPATH' in env else ''
    config_datapath = f"--config-data {env['INPUT_YAMLLINT_CONFIG_DATAPATH']}" if 'INPUT_YAMLLINT_CONFIG_DATAPATH' in env else ''
    format_opt = f"--format {env['INPUT_YAMLLINT_FORMAT']}" if 'INPUT_YAMLLINT_FORMAT' in env else ''

    comment = '1' if env.get('INPUT_YAMLLINT_COMMENT') in ['1', 'true'] else '0'

    return file_or_dir, strict, config_filepath, config_datapath, format_opt, comment

def yaml_lint(file_or_dir, strict, config_filepath, config_datapath, format_opt, comment):
    print(f"lint: info: yamllint on {file_or_dir}.")
    cmd = f"yamllint {strict} {config_filepath} {config_datapath} {format_opt} {file_or_dir}"

    try:
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True, check=True)
        lint_comment_status = "Success"
        print(f"lint: info: successful yamllint on {file_or_dir}.")
    except subprocess.CalledProcessError as e:
        result = e
        lint_comment_status = "Failed"
        print(f"lint: error: failed yamllint on {file_or_dir}.")

    lint_result = result.stdout if result.stdout else result.stderr
    print(lint_result)

    if os.environ.get("GITHUB_EVENT_NAME") == "pull_request" and comment == "1" and lint_comment_status == "Failed":
        comment_wrapper = create_comment(file_or_dir, lint_comment_status, lint_result)
        post_comment(comment_wrapper)

    set_multiline_output("yamllint_output", lint_result)

    return result.returncode

def create_comment(file_or_dir, status, result):
    return f"""#### `yamllint` {status}
<details><summary>Show Output</summary>
```
{result}
```
</details>

*Workflow: `{os.environ.get('GITHUB_WORKFLOW')}`, Action: `{os.environ.get('GITHUB_ACTION')}`, Lint: `{file_or_dir}`*"""

def post_comment(comment_wrapper):
    lint_payload = {"body": comment_wrapper}
    lint_comment_url = json.loads(os.environ["GITHUB_EVENT_PATH"]).get("pull_request", {}).get("comments_url")
    if lint_comment_url:
        headers = {"Authorization": f"token {os.environ['GITHUB_ACCESS_TOKEN']}", "Content-Type": "application/json"}
        try:
            response = requests.post(lint_comment_url, headers=headers, json=lint_payload)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to post comment on the pull request: {e}")

def main():
    file_or_dir, strict, config_filepath, config_datapath, format_opt, comment = parse_inputs()
    exit_code = yaml_lint(file_or_dir, strict, config_filepath, config_datapath, format_opt, comment)
    exit(exit_code)

if __name__ == "__main__":
    main()
