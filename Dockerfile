# Use an official Miniconda runtime as a parent image
FROM continuumio/miniconda3:latest
# Set the working directory to /app
WORKDIR /app/
# Copy the current directory contents into the container at /app
COPY . /app

RUN conda update -n base conda -yq \
&& conda update --all -yq \
&& conda config --append channels conda-forge \
&& conda install --yes --file requirements.txt
# Make port 80 available to the world outside this container
EXPOSE 80
# Run app.py when the container launches
CMD ["python", "app.py"]