import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

required = [
    "PyQt5",
    "requests"
]

setuptools.setup(
    name="wf-sentient-tracker",
    version="1.1.0",
    author="Kanjirito",
    author_email="kanjirito@protonmail.com",
    license="GPLv3",
    url="https://github.com/Kanjirito/wf-sentient-tracker",
    description="Qt tray application for warframe sentient anomaly notifications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=required,
    package_data={"wf_sentient_tracker": ["resources/*"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: X11 Applications :: Qt"
    ],
    python_requires=">=3",
    entry_points={
        "gui_scripts": [
            "sentient-tracker=wf_sentient_tracker.main:main"
        ]
    }
)
