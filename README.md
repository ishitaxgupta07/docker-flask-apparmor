# Docker Security with AppArmor and Python

## Objective

Explore Docker container security using AppArmor concepts, a Flask application, and the Docker SDK for Python.

## Project Structure

```text
docker-flask-apparmor/
├── profiles/
│   └── my-apparmor-profile
└── app/
    ├── app.py
    ├── Dockerfile
    ├── requirements.txt
    ├── apply_apparmor.py
    └── test_restricted_actions.py
```

## Technologies

- Python
- Flask
- Docker
- Docker SDK for Python
- AppArmor

## Build the Docker Image

From the app directory:

```bash
docker build -t flask-apparmor .
```

## Run the Flask Application

```bash
docker run -d --name flask-apparmor-test -p 5000:5000 flask-apparmor
```

Test the endpoint:

```bash
curl http://localhost:5000/
```

Expected response:

```text
Hello, this is a secure Flask application running inside a Docker container!
```

Remove the test container:

```bash
docker rm -f flask-apparmor-test
```

## Docker SDK Scripts

Install the SDK:

```bash
python -m pip install docker
```

Run the profile-inspection script:

```bash
python apply_apparmor.py
```

Run the restricted-action tests:

```bash
python test_restricted_actions.py
```

## Observed Test Results

| Test | Observed result |
|---|---|
| Flask image build | Successful |
| Flask HTTP endpoint | Successful |
| Docker SDK container management | Successful |
| Requested security option | `apparmor=my-apparmor-profile` |
| Runtime AppArmor label | `kernel` |
| Read `/etc/passwd` | Allowed, exit code 0 |
| Execute `/bin/sh` | Allowed, exit code 0 |

## Security Limitation

The current Docker Desktop environment reported `seccomp` and `cgroupns` as security options. In Ubuntu WSL, AppArmor reported that its filesystem was not mounted and its enabled flag was `N`.

The custom AppArmor profile was not demonstrated to be loaded and enforcing its rules. The restricted-action tests succeeded, so these results must not be interpreted as proof of AppArmor enforcement.

To verify actual enforcement, repeat the tests in a Linux environment where AppArmor is enabled, the custom profile is loaded, and the container's runtime label confirms that profile.

## Conclusion

This exercise demonstrates Flask containerization, Docker SDK usage, container inspection, and security testing. Actual custom AppArmor enforcement remains unverified in the current environment.
