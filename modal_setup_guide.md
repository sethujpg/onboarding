# Modal + VS Code — Developer Setup Guide

**Modes covered:** Interactive & Non-Interactive · Single GPU · Multi-GPU · CPU-only

> 📌 **Before you start:** Check with your mentor that you've been added to the Modal workspace (e.g. `neocognition-dev`). Without that, `modal setup` won't find a workspace to link to.

> 💡 **Why Modal:** It's significantly easier to get compute on Modal than on GCP at NeoCognition. Default to Modal for ad-hoc GPU work — only reach for GCP when you specifically need it.

---

## 1. Prerequisites & One-Time Setup

Complete these steps once. You will not need to repeat them.

### 1.1 Install Python & Modal

Open your **local** terminal (not VS Code) and run:

```bash
# macOS — install Python via Homebrew if not already installed
brew install python

# Add Python scripts to PATH (paste into ~/.zshrc)
export PATH="/Users/$USER/Library/Python/3.9/bin:$PATH"

# Reload shell config
source ~/.zshrc

# Install Modal
pip3 install modal
```

### 1.2 Authenticate with Modal

Link your local machine to your Modal workspace:

```bash
modal setup
```

A browser window will open. Log in and select your workspace (e.g. `neocognition-dev`). You should see:

```
Token is connected to the neocognition-dev workspace.
Token verified successfully!
```

> ℹ️ You only need to run `modal setup` once per machine. The token is saved to `~/.modal.toml`.

### 1.3 Install VS Code Extensions

Install these two extensions in your local VS Code:

- **Remote - Tunnels** (`ms-vscode.remote-server`)
- **Remote - SSH** (`ms-vscode-remote.remote-ssh`) — optional but useful

To install: open VS Code → Extensions sidebar (`Cmd+Shift+X`) → search the names above → Install.

---

## PART A — Interactive Setup (VS Code connected to a Modal container)

Interactive mode gives you a full VS Code environment running inside a Modal container — terminal, file explorer, debugger — all connected to real GPU hardware.

### 2. Interactive — Single GPU

#### 2.1 Launch the container

In your **local** terminal:

```bash
modal shell --gpu H100
```

You will drop into a bash shell inside the container:

```
Welcome to Modal's debug shell!
root / →
```

#### 2.2 Install the VS Code tunnel

Inside the Modal shell:

```bash
curl -Lk 'https://code.visualstudio.com/sha/download?build=stable&os=cli-alpine-x64' \
     -o vscode_cli.tar.gz
tar -xf vscode_cli.tar.gz
./code tunnel
```

The CLI will prompt you to authenticate via GitHub and name the machine:

```
How would you like to log in? · GitHub Account
Go to https://github.com/login/device and enter code: XXXX-XXXX
What would you like to call this machine? · my-modal-gpu

  Visual Studio Code Tunnel v1.120.0
  ➜  Tunnel: my-modal-gpu
  ➜  Open:   https://vscode.dev/tunnel/my-modal-gpu
```

#### 2.3 Connect local VS Code

1. Press `Cmd+Shift+P` in VS Code
2. Type: **Remote Tunnels: Connect to Tunnel**
3. Sign in with the same GitHub account
4. Select `my-modal-gpu` from the list

VS Code is now fully connected to the H100 container. The terminal inside VS Code runs on the remote machine.

> ⚠️ **Keep the local terminal window running `modal shell` open.** Closing it kills the container and disconnects VS Code.

#### 2.4 Verify the GPU

In the VS Code terminal (which is now running inside the container):

```bash
nvidia-smi
python3 -c "import torch; print(torch.cuda.get_device_name(0))"
```

#### 2.5 Stop the session

When done, press `Ctrl+C` in the local terminal running `modal shell`. The container shuts down automatically.

### 3. Interactive — Multi-GPU

For multi-GPU sessions you need a Python script because `modal shell` only supports a single GPU flag.

#### 3.1 Create the script

Save this as `dev_shell.py` on your local machine:

```python
import modal

app = modal.App("dev-shell-multi")

image = (
    modal.Image.debian_slim()
    .pip_install("torch", "torchvision")
)

@app.function(
    image=image,
    gpu="H100:2",      # 2x H100 — change number as needed
    timeout=7200,
)
def shell():
    modal.interact()
```

#### 3.2 Run it

```bash
modal run -i dev_shell.py::shell
```

Then follow steps 2.2–2.4 to install the VS Code tunnel and connect.

#### 3.3 GPU count options

```python
gpu="H100:1"   # single H100
gpu="H100:2"   # two H100s
gpu="H100:4"   # four H100s
gpu="H100:8"   # full node (8x H100)
```

> ℹ️ Multi-GPU containers cost more per second and may have longer cold starts. Use the minimum count you need.

### 4. Interactive — CPU Only

For tasks that don't need a GPU (data processing, debugging, light inference):

```bash
modal shell
```

No `--gpu` flag means CPU-only. Much cheaper and faster to start.

Or via script:

```python
import modal

app = modal.App("dev-shell-cpu")

image = modal.Image.debian_slim().pip_install("pandas", "numpy")

@app.function(image=image, timeout=3600)
def shell():
    modal.interact()
```

### 5. Switching GPU Types

Modal supports many GPU types. Change the `--gpu` flag or the `gpu=` parameter:

```bash
modal shell --gpu A10G     # A10G — good for inference, cheaper
modal shell --gpu A100     # A100 80GB — large model training
modal shell --gpu H100     # H100 — fastest, most expensive
modal shell --gpu T4       # T4 — cheapest GPU option
modal shell                # CPU only — no GPU
```

| GPU | VRAM | Best for | Modal string |
|---|---|---|---|
| T4 | 16 GB | Light inference, prototyping | `"T4"` |
| A10G | 24 GB | Inference, fine-tuning | `"A10G"` |
| A100 | 80 GB | Large model training | `"A100"` |
| H100 | 80 GB | Fastest training, largest models | `"H100"` |
| CPU | — | Data processing, no GPU needed | omit `gpu=` |

> 💡 Start with T4 or A10G for development and switch to H100 only for full training runs. The cost difference is significant.

---

## PART B — Non-Interactive Setup (run scripts directly)

Non-interactive mode is for running jobs end-to-end without a live session. Write a Python script, run it with `modal run`, and Modal executes it remotely. No VS Code tunnel needed.

### 6. Non-Interactive — Single GPU

#### 6.1 Write the job script

Save this as `job.py`:

```python
import modal

app = modal.App("my-job")

image = (
    modal.Image.debian_slim()
    .pip_install("torch", "torchvision")
)

@app.function(
    image=image,
    gpu="H100",
    timeout=3600,
)
def run_job():
    import torch
    print("GPU:", torch.cuda.get_device_name(0))
    # your training / inference code here
    return "done"

@app.local_entrypoint()
def main():
    result = run_job.remote()
    print(result)
```

#### 6.2 Run it

```bash
modal run job.py
```

Logs stream to your terminal in real time. The job runs remotely and exits when complete.

### 7. Non-Interactive — Multi-GPU

For distributed training or parallel jobs across multiple GPUs:

```python
import modal

app = modal.App("multi-gpu-job")

image = modal.Image.debian_slim().pip_install("torch")

@app.function(
    image=image,
    gpu="H100:4",   # 4x H100
    timeout=86400,  # 24 hours
)
def train():
    import torch
    print(f"GPUs available: {torch.cuda.device_count()}")
    # your multi-GPU training code here

@app.local_entrypoint()
def main():
    train.remote()
```

```bash
modal run multi_gpu_job.py
```

### 8. Non-Interactive — CPU Only

Remove the `gpu=` parameter entirely:

```python
import modal

app = modal.App("cpu-job")
image = modal.Image.debian_slim().pip_install("pandas")

@app.function(image=image, timeout=600)
def process_data():
    import pandas as pd
    # data processing here
    return "done"

@app.local_entrypoint()
def main():
    process_data.remote()
```

```bash
modal run cpu_job.py
```

---

## 9. Persisting Files Across Sessions

Modal containers are **ephemeral** — files are lost when the session ends. Use a **Volume** to persist data:

```python
import modal

app = modal.App("persistent-dev")
vol = modal.Volume.from_name("my-workspace", create_if_missing=True)

@app.function(
    image=modal.Image.debian_slim(),
    gpu="H100",
    volumes={"/workspace": vol},
    timeout=3600,
)
def shell():
    modal.interact()
```

Everything saved to `/workspace` persists between container sessions. Set your VS Code workspace folder to `/workspace`.

> 💡 Always save code and outputs to `/workspace`. The rest of the filesystem (pip installs, `/tmp`, etc.) resets every session.

---

## 10. Quick Reference

| What you want | Command |
|---|---|
| Interactive shell, single H100 | `modal shell --gpu H100` |
| Interactive shell, A10G | `modal shell --gpu A10G` |
| Interactive shell, CPU only | `modal shell` |
| Interactive multi-GPU (via script) | `modal run -i dev_shell.py::shell` |
| Run a job, single GPU | `modal run job.py` |
| Run a job, CPU only | `modal run cpu_job.py` |
| Run a job, multi-GPU | `modal run multi_gpu_job.py` |
| Stop any session | `Ctrl+C` in local terminal |

> ⚠️ **Always keep your local terminal open** while using interactive mode. Closing it terminates the container and disconnects VS Code immediately.

> 💡 **Cost tip:** Modal charges per second of container runtime. Always `Ctrl+C` when done. CPU containers cost ~10× less than H100 — use CPU for development and GPU only for actual compute.
