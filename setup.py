import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ai-market-contest",
    version="0.0.1",
    author="Yash Yeola, Ibraheem Wazir, Matteo Bongiovanni, Pranav Maganti, Michael Clasby, Jack Benham",
    author_email="gmail.com",
    description="AI contests for deep reinforcement learning bots in online markets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AIMarketContest/simulation.git",
    packages=setuptools.find_packages(),
    scripts=["src/ai_market_contest/cli/aic"],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
