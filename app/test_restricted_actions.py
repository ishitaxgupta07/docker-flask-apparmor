import docker

client = docker.from_env()
container = None

try:
    container = client.containers.run(
        "flask-apparmor",
        security_opt=["apparmor=my-apparmor-profile"],
        detach=True,
        name="flask-apparmor-restriction-test"
    )

    print(f"Container started: {container.short_id}")

    tests = [
        ("Read /etc/passwd", "cat /etc/passwd"),
        ("Execute /bin/sh", "/bin/sh -c 'echo shell-execution-succeeded'")
    ]

    for description, command in tests:
        result = container.exec_run(command)
        print(f"\nTest: {description}")
        print(f"Exit code: {result.exit_code}")
        print(result.output.decode(errors="replace"))

finally:
    if container is not None:
        container.remove(force=True)
        print("Container removed.")
