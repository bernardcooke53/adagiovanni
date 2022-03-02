# syntax=docker/dockerfile:1
# Build the API package into a binary
FROM python:3.8 as python_build

WORKDIR /workspace

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock /workspace/poetry.lock
COPY README.md /workspace/README.md
COPY src /workspace/src
COPY pyproject.toml /workspace/pyproject.toml

RUN export PATH="/root/.local/bin:$PATH" && \
    poetry build --format wheel


# Copy that binary over to a fresh container where
# we'll install for a low-privilege user and remove
# the source code away to site-packages, where it's
# less at risk of being clobbered by the running of
# the application.
FROM python:3.8
ARG app_username
ARG app_groupname

COPY --from=python_build /workspace/dist/adagiovanni*.whl /home/${app_username}/app/

WORKDIR /home/${app_username}/app/

# Add the low-privilege user
RUN useradd ${app_username}
RUN chown ${app_username}:${app_groupname} /home/${app_username}/ -R

USER ${app_username}:${app_groupname}

ENV PATH "$PATH:/home/${app_username}/.local/bin"

RUN python3 -m pip install --user ./adagiovanni*.whl
RUN rm ./adagiovanni*.whl
