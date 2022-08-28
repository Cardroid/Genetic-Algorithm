import setuptools

required_packages = [
    "tqdm",
    "colorlog",
    "matplotlib",
]

setuptools.setup(
    name="genetic-alg",
    version="0.0.1",
    author="cardroid",
    author_email="carbonsindh@gmail.com",
    description="The Easy to use genetic algorithms.",
    install_requires=required_packages,
    license="MIT",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    entry_points={"console_scripts": ["gene=genetic_alg.entry:main"]},
)
