# syntax=docker/dockerfile:1

FROM continuumio/miniconda3

LABEL fly_launch_runtime="flask"

WORKDIR /code
COPY . .
RUN conda env create -f environment.yml
SHELL ["conda", "run", "-n", "protein", "/bin/bash", "-c"]

EXPOSE 8080

CMD ["conda", "run", "--no-capture-output", "-n", "protein", "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]
