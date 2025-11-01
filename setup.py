import os
from setuptools import setup, find_packages

readme_content = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        readme_content = f.read()

setup(
    name="vira-cli",
    version="2.0",
    packages=find_packages(),
    install_requires=[
        "google-generativeai>=0.3.0",
        "pyperclip>=1.8.0",
        "python-dotenv>=1.0.0",
        "rich>=13.0.0",
        "prompt-toolkit>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "vira=vira.main:main",
        ],
    },
    author="Vũ Văn Định",
    author_email="vuvandinh203@gmail.com",
    url="https://github.com/vuvandinh123/vira-cli",
    description="🚀 AI-powered CLI helper: translate natural language into shell commands.",
    long_description=readme_content,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    keywords="cli ai shell gemini google generativeai helper terminal",
)