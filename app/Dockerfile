FROM python:3-onbuild

# Combine javascript files
# This is awesomely ugly
RUN mkdir static
RUN echo "\$(function() {" >> static/core.js
RUN cat js/*.js >> static/core.js
RUN echo "\n});" >> static/core.js

CMD python 101-questions.py
