FROM continuumio/miniconda3:latest

WORKDIR /app/

COPY . /app

RUN conda update -n base conda -yq \
&& conda update --all -yq \
&& conda config --append channels conda-forge \
&& conda install --yes --file requirements.txt

EXPOSE 80

CMD ["python", "app.py"]