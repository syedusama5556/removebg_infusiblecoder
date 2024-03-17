FROM python:3.10-slim

WORKDIR /removebg_infusiblecoder

RUN pip install --upgrade pip

COPY . .

# RUN python -m pip install ".[cli]" --extra-index-url https://download.pytorch.org/whl/cpu
RUN python -m pip install ".[cli]"
RUN removebg_infusiblecoder d

EXPOSE 5000
ENTRYPOINT ["removebg_infusiblecoder"]
CMD ["s"]