from setuptools import find_packages, setup

install_requires = ("Django>=4.2",)
setup(
    name="queryset_annotations",
    version="1",
    description="Django Smart Queryset Annotations",
    url="https://github.com/GefMar/django_queryset_annotations",
    author="Sergei (Gefest) Romanchuk",
    license="MIT",
    packages=find_packages(),
    install_requires=install_requires,
    python_requires=">=3.8",
)
