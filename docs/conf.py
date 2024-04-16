# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
scripts = ['/home/grozd/Desktop/Faks/Programsko inzenjerstvo u otvorenim sustavima/tim09-app',
           '/home/grozd/Desktop/Faks/Programsko inzenjerstvo u otvorenim sustavima/tim09-app/app',
           '/home/grozd/Desktop/Faks/Programsko inzenjerstvo u otvorenim sustavima/tim09-app/app/main'
           ]
if scripts not in sys.path:
    for s in scripts:
        sys.path.append(s)

project = 'TIM09-App'
copyright = '2024, Karlo Mahović, Grgo Lovrić, Robert Štitić, Hrvoje Čaldarević'
author = 'Karlo Mahović, Grgo Lovrić, Robert Štitić, Hrvoje Čaldarević'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
#napoleon_include_private_with_doc = True
#autoclass_content = 'both'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
