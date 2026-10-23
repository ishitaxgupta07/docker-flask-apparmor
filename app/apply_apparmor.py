import docker

client = docker.from_env()

print("Docker SDK connected successfully.")

image, build_logs = client.images.build(
    path=".",
    tag="flask-apparmor"
)

print(f"Image ready: {image.tags}")

container = None

try:
    container = client.containers.run(
        "flask-apparmor",
        ports={"5000/tcp": 5000},
        security_opt=["apparmor=my-apparmor-profile"],
        detach=True,
        name="flask-apparmor-sdk-test"
    )

    print(f"Container started: {container.short_id}")

    info = client.api.inspect_container(container.id)
    print("Requested security options:", info["HostConfig"]["SecurityOpt"])

    print(
        "Runtime AppArmor label:",
        container.exec_run("cat /proc/self/attr/current").output.decode().strip()
    )

finally:
    if container is not None:
        container.remove(force=True)
        print("Container removed.")
