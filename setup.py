from setuptools import setup, find_packages

setup(
    name="audioclast",
    version="0.1.0",
    description="Real-time audio loopback and monitoring tool with TUI",
    author="ndjuric",
    author_email="metod303@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "rich",
        "textual"
    ],
    entry_points={
        "console_scripts": [
            "audioclast=ui.tui.tui:main",
        ]
    },
    python_requires=">=3.8",
    include_package_data=True,
)
