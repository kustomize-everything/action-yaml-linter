# action-yaml-linter

This repository is a [fork of karancode/yamllint-github-action](https://github.com/karancode/yamllint-github-action), tailored for running `yamllint` within GitHub Actions. Particularly useful for projects utilizing Kustomize, this action ensures that YAML files, which are extensively used in Kustomize for Kubernetes resource management, adhere to best practices and maintain consistent syntax and structure.

## Significance in Kustomize Projects

Using Kustomize means dealing with a multitude of YAML files. Linting these files is crucial because it:

- **Ensures Uniformity:** Keeps formatting consistent across all YAML files.
- **Detects Errors:** Identifies syntax issues and accidental typos early.
- **Upholds Standards:** Maintains high-quality, readable, and maintainable Kubernetes configurations.

## Features

- **Adaptable:** Can be configured for different directories via the GitHub Actions YAML file.
- **Pull Request Integration:** Automatically comments on pull requests with `yamllint` findings.
- **Success Indicator:** Successful execution is marked by an exit code of `0`.

## Usage

### Basic Usage

For general use, including linting all YAML files in the repository, use the following configuration in your GitHub Actions workflow:

```yaml
name: 'YAML Lint'
on: [push, pull_request]
jobs:
  yamllint:
    name: 'Run Yamllint on All Files'
    runs-on: ubuntu-latest
    steps:
      - name: 'Checkout Code'
        uses: actions/checkout@master
      - name: 'Run Yamllint'
        uses: kustomize-everything/yamllint-github-action@main
        with:
          yamllint_file_or_dir: '.'
          yamllint_strict: false
          yamllint_comment: true
        env:
          GITHUB_ACCESS_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

This configuration sets up a workflow that triggers on both push and pull request events, linting every YAML file in the repository.

## Configuration

### Inputs

Tailor the action with these inputs:

| Parameter                  | Default | Description                                                                       |
|----------------------------|---------|-----------------------------------------------------------------------------------|
| `yamllint_file_or_dir`     | `.`     | (Optional) Target file or directory for `yamllint`. Defaults to all YAML files.   |
| `yamllint_strict`          | `false` | (Optional) Toggle strict mode.                                                    |
| `yamllint_config_filepath` | `empty` | (Optional) Custom config file path.                                               |
| `yamllint_config_datapath` | `empty` | (Optional) Custom config as YAML source.                                          |
| `yamllint_format`          | `auto`  | (Optional) Specify output format.                                                 |
| `yamllint_comment`         | `false` | (Optional) Enable/disable commenting on GitHub PRs.                               |

### Outputs

- `yamllint_output`: The linting output from the action.

### Secrets

- `GITHUB_ACCESS_TOKEN`: (Optional) For GitHub API use, needed to comment on PRs if `yamllint_comment` is `true`.

## Development

### Testing

Test using the [bats](https://github.com/bats-core/bats-core) framework. After installing [bats](https://github.com/bats-core/bats-core#installation), run tests with `./tests/run.bats`.
