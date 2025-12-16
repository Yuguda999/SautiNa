# Deploy N-ATLaS on Modal with vLLM

This guide demonstrates how to deploy the **N-ATLaS** model as an OpenAI-compatible API endpoint on **Modal** using **vLLM**.

We use the **FP8-quantized version** for optimal performance on H100 GPUs.

## 📋 Prerequisites

-   A [Modal](https://modal.com/) account.
-   Modal CLI installed:
    ```bash
    pip install modal
    ```
-   Modal setup:
    ```bash
    python3 -m modal setup
    ```

## 💻 The Code

Create a Python file named `natlas_serve.py`:

```python
import modal

vllm_image = (
    modal.Image.from_registry("nvidia/cuda:12.8.0-devel-ubuntu22.04", add_python="3.12")
    .entrypoint([])
    .uv_pip_install(
        "vllm==0.11.2",
        "huggingface-hub==0.36.0",
        "flashinfer-python==0.5.2",
    )
    .env({"HF_XET_HIGH_PERFORMANCE": "1"})
)

# use MODEL_NAME = "tosinamuda/N-ATLaS-FP8" if interested in the 8-bit quantized version 
MODEL_NAME = "NCAIR1/N-ATLaS"

hf_cache_vol = modal.Volume.from_name("huggingface-cache", create_if_missing=True)
vllm_cache_vol = modal.Volume.from_name("vllm-cache", create_if_missing=True)

FAST_BOOT = True

app = modal.App("natlas-vllm")

N_GPU = 1
MINUTES = 60
VLLM_PORT = 8000


@app.function(
    image=vllm_image,
    gpu=f"H100:{N_GPU}",
    scaledown_window=15 * MINUTES,
    timeout=10 * MINUTES,
    volumes={
        "/root/.cache/huggingface": hf_cache_vol,
        "/root/.cache/vllm": vllm_cache_vol,
    },
)
@modal.concurrent(max_inputs=32)
@modal.web_server(port=VLLM_PORT, startup_timeout=10 * MINUTES)
def serve():
    import subprocess

    cmd = [
        "vllm",
        "serve",
        MODEL_NAME,
        "--served-model-name", "n-atlas",
        "--host", "0.0.0.0",
        "--port", str(VLLM_PORT),
        "--uvicorn-log-level=info",
    ]

    cmd += ["--enforce-eager" if FAST_BOOT else "--no-enforce-eager"]
    cmd += ["--tensor-parallel-size", str(N_GPU)]

    print(cmd)
    subprocess.Popen(" ".join(cmd), shell=True)
```

## 🚀 Deploy

Run the following command to deploy the app:

```bash
modal deploy natlas_serve.py
```

After deployment, you'll receive a URL similar to:
`https://your-workspace--natlas-vllm-serve.modal.run`

## 🔌 Usage

The endpoint is OpenAI-compatible. You can use it with any OpenAI client.

### Python Example

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://your-workspace--natlas-vllm-serve.modal.run/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="n-atlas",
    messages=[
        {"role": "user", "content": "Bawo ni? Se o le so Yoruba?"}
    ]
)

print(response.choices[0].message.content)
```

### cURL Example

```bash
curl https://your-workspace--natlas-vllm-serve.modal.run/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "n-atlas",
    "messages": [{"role": "user", "content": "Kini oruko re?"}]
  }'
```

### Streaming Example

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://your-workspace--natlas-vllm-serve.modal.run/v1",
    api_key="not-needed"
)

stream = client.chat.completions.create(
    model="n-atlas",
    messages=[{"role": "user", "content": "Tell me about Yoruba culture"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

## ⚙️ Configuration Options

-   **GPU Selection**: The default uses H100. For lower cost, try A100:
    ```python
    gpu="A100:1"
    ```
-   **Scale-down Window**: How long the server stays up without requests (default 15 minutes):
    ```python
    scaledown_window=5 * MINUTES  # Scale down faster to save cost
    ```
-   **Fast Boot vs Performance**: Set `FAST_BOOT = False` for better throughput if you keep the server running:
    ```python
    FAST_BOOT = False  # Better performance, slower cold starts
    ```

## 💰 Costs

Modal charges per second of GPU usage. An H100 costs roughly **$0.001/second**. With the default 15-minute scaledown window, expect:

1.  **First request**: Cold start (~2-3 minutes).
2.  **Subsequent requests**: Fast responses.
3.  **Idle cost**: Up to 15 minutes of GPU time after the last request.

> **Tip**: Set a shorter `scaledown_window` to reduce idle costs.

## ℹ️ About N-ATLaS

**N-ATLaS** is an 8B parameter multi-lingual model fine-tuned from Llama-3-8B for English and major Nigerian languages. The FP8 quantized version reduces memory usage by 50% while maintaining quality, optimized for H100 GPUs.

-   **Original model**: `NCAIR1/N-ATLaS`
-   **FP8 version**: `tosinamuda/N-ATLaS-FP8`