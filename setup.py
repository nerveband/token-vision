from setuptools import setup, find_packages

setup(
    name="token-vision",
    version="0.1.3a1",  # Alpha version
    author="Ashraf Ali",
    author_email="",  # Add your email
    description="A fast, offline token calculator for AI vision models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nerveband/token-vision",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.24.0",
        "pillow>=10.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black",
            "isort",
            "flake8",
        ],
    },
) 