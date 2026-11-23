from setuptools import find_packages, setup

package_name = "restaurant_robot_mission"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="vuloi",
    maintainer_email="dev@restaurant-robot.local",
    description="Mission Manager FSM, multi-stop optimization, and HRI node.",
    license="MIT",
    entry_points={
        "console_scripts": [],
    },
)
