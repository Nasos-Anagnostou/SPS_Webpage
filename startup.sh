#!/bin/bash

if [ ${STREAMLIT_SECRET+x} ]; then
	mkdir -p /app/.streamlit
	echo ${STREAMLIT_SECRET} | base64 --decode > /app/.streamlit/secrets.toml
fi

streamlit run Home_Page.py --server.port=8501 --server.address=0.0.0.0
