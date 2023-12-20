from setuptools import setup
from glob import glob
import os

package_name = 'embedded_led_logging'
with (open('requirements.txt', 'r')) as f:
    reqs = f.read().splitlines()

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    long_description=open('README.md').read(),
    install_requires=reqs,
    zip_safe=True,
    maintainer='tim',
    maintainer_email='tim.dodge64@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
)
