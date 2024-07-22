import datetime
import random
import re

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Show app title and description.
st.set_page_config(page_title="Home", page_icon="💡")

with open('README.md') as f: content = f.read()

st.markdown(content)