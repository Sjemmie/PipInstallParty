# Understanding Python Virtual Environments (venv)

A Python virtual environment, or `venv`, is a tool that helps you create isolated environments for your Python projects. Each environment has its own dependencies and libraries, ensuring that projects don't interfere with each other. This is especially useful when working on multiple projects that require different versions of libraries or Python itself.

## Why Use a Virtual Environment?

- **Dependency Management**: Keeps project dependencies separate, avoiding conflicts.
- **Isolation**: Prevents global Python installations from affecting your project.
- **Reproducibility**: Ensures the same environment can be recreated on another system.

## Creating and Using a Virtual Environment

To create a virtual environment, run the following command:
```bash
python -m venv <env_name>
```

To activate it run in your terminal which can be located at the top of your navigation bar
```bash
<env_name>\Scripts\activate
```

When the environment is active you can install your dependencies using:
```bash
pip install <package_name>
```

To save a list of all installed dependencies, use:
```bash
pip freeze > requirements.txt
```


To install dependencies from a requirements.txt file in another environment or system, run:
```bash
pip install -r requirements.txt
```