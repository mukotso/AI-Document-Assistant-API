# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        default-mysql-client \
        python3-dev \
        default-libmysqlclient-dev \
        pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.20+8/OpenJDK11U-jdk_x64_linux_hotspot_11.0.20_8.tar.gz -o openjdk-11_linux-x64_bin.tar.gz \
    && tar -xzf openjdk-11_linux-x64_bin.tar.gz -C /opt \
    && ln -s /opt/jdk-11/bin/java /usr/bin/java \
    && ln -s /opt/jdk-11/bin/javac /usr/bin/javac \
    && rm openjdk-11_linux-x64_bin.tar.gz



# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model and install pyspellchecker
RUN python -m spacy download en_core_web_sm
RUN pip install pyspellchecker

# Copy the Django project
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
