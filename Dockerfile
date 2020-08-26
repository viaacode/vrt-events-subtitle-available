FROM python:3.7-slim

# Make a new group and user so we don't run as root.
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup

# This is the location where our files will go in the container.
WORKDIR /app

# Copy all files
COPY . .
RUN chown -R appuser:appgroup /app

# We install all our Python dependencies. Add the extra index url because some
# packages are in the meemoo repo.
RUN pip3 install -r requirements.txt \
    --extra-index-url http://do-prd-mvn-01.do.viaa.be:8081/repository/pypi-all/simple \
    --trusted-host do-prd-mvn-01.do.viaa.be && \
    pip3 install flake8

USER appuser

# This command will be run when starting the container. It is the same one that can be used to run the application locally.
CMD [ "python", "main.py"]