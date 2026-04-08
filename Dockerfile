FROM python:3.10-slim

WORKDIR /app

COPY . .

# Install all dependencies including uvicorn
RUN pip install --no-cache-dir openenv-core pydantic openai uvicorn fastapi

# Make sure server/app.py is in the right place
RUN ls -R server/

EXPOSE 7860

# Command to start the server correctly for HF Spaces
CMD ["python", "-m", "server.app", "--host", "0.0.0.0", "--port", "7860"]
