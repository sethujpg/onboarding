# GCP CPU/GPU VM Setup Guide

A beginner-friendly guide for creating and using Google Cloud VMs for CPU, single-GPU, and multi-GPU development from VS Code.

> 📌 **Before you start:** Confirm with your mentor that you've been given GCP access and which project to use. Also: **Modal is the easier path to compute at NeoCognition for most ad-hoc GPU work** — see [modal_setup_guide.md](modal_setup_guide.md). Use GCP when you specifically need it (long-running VMs, specific GCP services, etc.).

This guide uses dummy values throughout. Replace them with your own project, VM, zone, user, and IP values.

```text
Example project name: ml-dev-project
Example project ID: ml-dev-project-123456
Example VM name: gpu-dev-vm
Example zone: us-central1-a
Example GPU VM type: a2-ultragpu-2g
Example GPUs: 2 x NVIDIA A100-SXM4-80GB
Example local username: yourname
Example public IP: 203.0.113.10
```

---

## 0. Mental model

A GCP VM is like renting a powerful remote computer in a Google data center. You interact with it from your laptop using SSH or VS Code Remote SSH.

### Storage analogy

Think of the VM like an apartment:

- **Boot disk** — the main apartment. OS, your user folder, conda, packages, normal files.
- **Persistent data disk** — an extra storage room in the same building. Good for datasets, checkpoints, notebooks, model weights, large repos.
- **Local SSD / NVMe** — a fast workbench attached to the desk. Very fast, but temporary. Use for scratch data, not important long-term files.

Example VM storage:

```text
/dev/sda1           -> 1 TB boot disk, mounted at /
/home/yourname      -> lives on the boot disk
/dev/nvme0n1        -> 375 GB local SSD, not mounted by default
/dev/nvme0n2        -> 375 GB local SSD, not mounted by default
```

### What does "mounted" mean?

A disk can physically exist but Linux will not use it until it is attached to a folder.

```text
Disk exists:       /dev/nvme0n1
Mounted at folder: /mnt/localssd
```

After mounting, files written to `/mnt/localssd` go to that disk.

---

## 1. Common use cases

### Use case A: CPU-only development

Choose this for normal Python, notebooks, data processing, or light testing.

```text
Machine family: E2, N2, N2D, C3, or C4
GPU: none
Boot disk: 100 GB to 1 TB depending on data
```

CPU-only is much cheaper and simpler.

### Use case B: Single GPU

Choose this for small model inference, CUDA testing, Stable Diffusion, embeddings, prototyping.

```text
Budget / starter: N1 + T4
Modern inference: G2 + L4
More serious:     A2 Standard + A100
```

### Use case C: Multi-GPU

Choose this for distributed training, large models, multi-GPU inference, or model parallelism.

```text
A2 Ultra: A100 80GB GPUs
A3:       H100 GPUs
Newer accelerator families: depending on region & availability
```

Example: `a2-ultragpu-2g = 2 x NVIDIA A100 80GB`

### Use case D: Changing GPU later

GPU changes usually require stopping the VM. It is often cleaner to create a new VM with the desired machine type and attach/move your persistent data disk:

1. Keep code/data on a separate persistent data disk.
2. Detach data disk from old VM.
3. Attach data disk to new VM.
4. Install/check drivers on the new VM.
5. Continue work.

---

## 2. Before creating the VM

### 2.1 Confirm the right Google Cloud project

```text
Google Cloud Console -> top project selector
```

> Important: **project name** and **project ID** can differ. Use the project **ID** in commands.

From local terminal:

```bash
gcloud projects list
gcloud config set project ml-dev-project-123456
gcloud config get-value project   # expect: ml-dev-project-123456
```

### 2.2 Make sure billing is enabled

GPU VMs will not start unless billing is enabled.

```text
Google Cloud Console -> Billing
```

### 2.3 Check IAM permissions

Typical roles needed:

```text
Compute Admin
Service Account User
Viewer or Browser
```

If you cannot create VMs or change firewall rules, ask the project admin.

---

## 3. Install local tools on your laptop (macOS)

### 3.1 Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

For Apple Silicon Macs:

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
brew --version
```

### 3.2 gcloud CLI

```bash
brew install --cask gcloud-cli
```

If `gcloud` isn't found:

```bash
ls -la /opt/homebrew/share/google-cloud-sdk/bin/gcloud
echo 'export PATH="/opt/homebrew/share/google-cloud-sdk/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
gcloud --version
```

### 3.3 Login

```bash
gcloud auth login
gcloud config set project ml-dev-project-123456
```

---

## 4. Quotas — the most common GPU blocker

GPU VMs often fail to create because the project doesn't have enough quota.

### Symptoms

```text
Quota exceeded
Insufficient quota
GPUS_ALL_REGIONS quota exceeded
NVIDIA_A100_GPUS quota exceeded
Not enough resources available
```

### What you need to check

```text
GPU quota for the GPU family/model
CPU quota
Regional resource quota
Local SSD quota (if the machine type includes local SSD)
```

Example:

```text
VM: a2-ultragpu-2g
GPU: 2 x A100 80GB
Region: us-central1
Zone: us-central1-a
```

You need A100 quota in `us-central1`, plus enough CPUs and other resources.

### Console path

```text
Google Cloud Console -> IAM & Admin -> Quotas
```

Search: `GPU`, `A100`, `NVIDIA`, `CPUs`, `Local SSD`. Filter by region (e.g. `us-central1`).

### Requesting an increase

1. Select the quota → **Edit quotas**
2. Request the needed amount
3. Add a reason, e.g.: *"Need temporary access to 2 x A100 80GB GPUs in us-central1 for ML development and testing on Compute Engine."*

> ⚠️ Do not request only GPUs. Also check CPU and Local SSD quotas. Some accelerator-optimized machine types include local SSD automatically.

---

## 5. Create a VM

### Option A: CPU-only VM

```text
Compute Engine -> VM instances -> Create instance
```

Beginner settings:

```text
Name: cpu-dev-vm
Region/zone: us-central1-a
Machine family: E2 or N2
Machine type: based on CPU/RAM need
Boot disk: Debian 12 or Ubuntu LTS
Boot disk size: 100 GB or larger
External IP: optional
Firewall: do NOT blindly open everything
```

### Option B: Single-GPU VM

```text
N1 + T4   -> cheaper CUDA testing
G2 + L4   -> modern inference / image generation
A2 + A100 -> heavier workloads
```

> GPU availability depends on zone.

### Option C: Multi-GPU VM

```text
Machine type: a2-ultragpu-2g
GPUs: 2 x NVIDIA A100-SXM4-80GB
Zone: us-central1-a
Boot image: Debian 12
Boot disk: 1 TB balanced persistent disk
```

### Boot disk tip

Use **at least 100 GB** for GPU VMs. For ML, **500 GB to 1 TB** is more comfortable — drivers, conda envs, Docker images, PyTorch wheels, and weights add up fast.

---

## 6. SSH access and firewall

### 6.1 Check VM is running

```text
Compute Engine -> VM instances
Status: Running
External IP: present if using normal SSH
```

```bash
gcloud compute instances list
```

### 6.2 SSH from laptop

```bash
gcloud compute ssh gpu-dev-vm --zone=us-central1-a
```

If it works, generate SSH config for normal SSH and VS Code:

```bash
gcloud compute config-ssh
ssh gpu-dev-vm.us-central1-a.ml-dev-project-123456
```

### 6.3 If SSH times out — usually firewall

```bash
gcloud compute firewall-rules list \
  --filter='network~default' \
  --format='table(name,direction,sourceRanges,allowed,disabled,targetTags)'
```

If no rule allows `tcp:22`, create one restricted to **your laptop IP**:

```bash
curl ifconfig.me   # get your public IP
```

Tag the VM:

```bash
gcloud compute instances add-tags gpu-dev-vm \
  --zone=us-central1-a \
  --tags=ssh-dev
```

Create the rule:

```bash
gcloud compute firewall-rules create allow-ssh-dev-only \
  --network=default \
  --direction=INGRESS \
  --priority=1000 \
  --action=ALLOW \
  --rules=tcp:22 \
  --source-ranges=203.0.113.10/32 \
  --target-tags=ssh-dev
```

Retry:

```bash
gcloud compute ssh gpu-dev-vm --zone=us-central1-a
```

### Security rule of thumb

❌ Avoid: `0.0.0.0/0 tcp:22` (anyone on the internet can attempt SSH).

✅ Prefer: `YOUR_PUBLIC_IP/32 tcp:22` or use IAP tunneling.

---

## 7. Connect with VS Code

### 7.1 Install extension

VS Code → install **Remote - SSH**.

### 7.2 Generate SSH config

```bash
gcloud compute config-ssh
```

You should see:

```text
You should now be able to use ssh/scp with your instances.
For example:
ssh gpu-dev-vm.us-central1-a.ml-dev-project-123456
```

### 7.3 Connect

```text
Cmd + Shift + P -> Remote-SSH: Connect to Host
```

Choose: `gpu-dev-vm.us-central1-a.ml-dev-project-123456`

Open folder: `/home/yourname` (or `/mnt/data/workspace` later).

### Recommended remote-context VS Code extensions

```text
Python
Jupyter
Remote - SSH
GitLens (optional)
Docker (optional)
```

---

## 8. Install NVIDIA drivers

After creating a GPU VM, check:

```bash
nvidia-smi
```

If `nvidia-smi: command not found`, the driver is missing.

### 8.1 Confirm hardware is visible

```bash
sudo apt-get update
sudo apt-get install -y pciutils python3 curl
lspci | grep -i nvidia
```

### 8.2 Install driver using Google installer

```bash
mkdir -p ~/gpu-install
cd ~/gpu-install
curl -fSsL -O https://storage.googleapis.com/compute-gpu-installation-us/installer/v1.8.0/cuda_installer.pyz
```

For Debian, binary mode may be needed:

```bash
sudo python3 cuda_installer.pyz install_driver --installation-mode=binary
```

If that fails with a branch-related error:

```bash
sudo python3 cuda_installer.pyz install_driver --installation-branch=nfb
```

Reboot and reconnect:

```bash
sudo reboot
# wait, then:
ssh gpu-dev-vm.us-central1-a.ml-dev-project-123456
nvidia-smi
```

Expected:

```text
2 x NVIDIA A100-SXM4-80GB
CUDA available
No running processes found
```

---

## 9. Install Miniconda and create environments

### 9.1 Miniconda

```bash
cd ~
wget -O Miniconda3-Linux-x86_64.sh \
  https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-Linux-x86_64.sh
```

During install:

```text
Press Enter to view license
Press q to exit license viewer
Type yes to accept
Install location: press Enter
Run conda init? yes
```

```bash
source ~/.bashrc
conda --version
```

### 9.2 GPU environment

```bash
conda create -n gpu python=3.11 -y
conda activate gpu
conda install -y jupyterlab ipykernel numpy pandas scipy matplotlib scikit-learn tqdm ipywidgets
python -m ipykernel install --user --name gpu --display-name "Python (gpu)"
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

Test:

```bash
python - <<'PY'
import torch
print('Torch:', torch.__version__)
print('CUDA available:', torch.cuda.is_available())
print('GPU count:', torch.cuda.device_count())
for i in range(torch.cuda.device_count()):
    print(i, torch.cuda.get_device_name(i))
PY
```

Expected:

```text
CUDA available: True
GPU count: 2
0 NVIDIA A100-SXM4-80GB
1 NVIDIA A100-SXM4-80GB
```

### 9.3 CPU-only environment

```bash
conda create -n cpu python=3.11 -y
conda activate cpu
conda install -y jupyterlab ipykernel numpy pandas scipy matplotlib scikit-learn tqdm ipywidgets
python -m ipykernel install --user --name cpu --display-name "Python (cpu)"
pip install torch torchvision torchaudio
```

---

## 10. Interactive Jupyter setup

### 10.1 Start Jupyter on VM

```bash
conda activate gpu
mkdir -p ~/workspace
cd ~/workspace
jupyter lab --no-browser --ip=127.0.0.1 --port=8888
```

Copy the URL printed (it contains a token).

### 10.2 SSH tunnel from laptop

```bash
ssh -L 8888:localhost:8888 gpu-dev-vm.us-central1-a.ml-dev-project-123456
```

Open: `http://localhost:8888` and paste the token.

### 10.3 Use from VS Code Remote SSH

1. Connect to VM
2. Open `/home/yourname/workspace` or `/mnt/data/workspace`
3. Create `.ipynb` file
4. Select kernel: `Python (gpu)`

> ⚠️ Do not expose Jupyter directly to the internet. Avoid opening port `8888` publicly. Use SSH tunneling.

---

## 11. Non-interactive setup

### Run script directly

```bash
conda activate gpu
python train.py
```

### Run and save logs

```bash
conda activate gpu
python train.py 2>&1 | tee train.log
```

### Keep running after disconnect with `tmux`

```bash
sudo apt-get update
sudo apt-get install -y tmux
tmux new -s train
conda activate gpu
python train.py 2>&1 | tee train.log
# detach: Ctrl+b, then d
# reattach:
tmux attach -t train
```

### Run on one specific GPU

```bash
CUDA_VISIBLE_DEVICES=0 python train.py
CUDA_VISIBLE_DEVICES=1 python train.py
```

Inside Python, the selected GPU appears as `cuda:0`.

### Multi-GPU with PyTorch (DDP)

```bash
torchrun --nproc_per_node=2 train.py
```

Quick GPU count check:

```bash
python - <<'PY'
import torch
print(torch.cuda.device_count())
PY
```

---

## 12. Changing GPU usage in code

### CPU only

```python
import torch
device = torch.device('cpu')
```

Or force no GPU from shell:

```bash
CUDA_VISIBLE_DEVICES="" python script.py
```

### Single GPU

```bash
CUDA_VISIBLE_DEVICES=0 python script.py
```

```python
import torch
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
```

### Multi-GPU simple DataParallel (quick tests)

```python
import torch
import torch.nn as nn

model = MyModel()
model = nn.DataParallel(model)
model = model.cuda()
```

### Multi-GPU recommended (DDP — for serious training)

```bash
torchrun --nproc_per_node=2 train.py
```

---

## 13. Storage improvements

### Check current storage

```bash
df -h /
lsblk
```

Example:

```text
/dev/sda1   985G   17G   928G   2% /
nvme0n1     375G
nvme0n2     375G
```

### Resize boot disk to 1 TB

From laptop:

```bash
gcloud compute disks resize gpu-dev-vm \
  --zone=us-central1-a \
  --size=1024GB
```

Inside VM, if Linux didn't expand automatically:

```bash
sudo apt-get update
sudo apt-get install -y cloud-guest-utils
sudo growpart /dev/sda 1
sudo resize2fs /dev/sda1
df -h /
```

### Add a separate persistent data disk

From laptop (1 TB):

```bash
gcloud compute disks create gpu-dev-data-ssd \
  --zone=us-central1-a \
  --type=pd-ssd \
  --size=1024GB
```

For 2 TB, use `--size=2048GB`.

Attach:

```bash
gcloud compute instances attach-disk gpu-dev-vm \
  --zone=us-central1-a \
  --disk=gpu-dev-data-ssd
```

Inside VM:

```bash
lsblk
ls -l /dev/disk/by-id/ | grep google

sudo mkfs.ext4 -F /dev/disk/by-id/google-gpu-dev-data-ssd
sudo mkdir -p /mnt/data
sudo mount -o discard,defaults /dev/disk/by-id/google-gpu-dev-data-ssd /mnt/data
sudo chown -R yourname:yourname /mnt/data
df -h /mnt/data
```

Make persistent across reboot:

```bash
sudo blkid /dev/disk/by-id/google-gpu-dev-data-ssd
sudo nano /etc/fstab
```

Add:

```fstab
UUID=YOUR_UUID_HERE /mnt/data ext4 discard,defaults,nofail 0 2
```

Test:

```bash
sudo mount -a
df -h /mnt/data
```

### Recommended workspace layout

```bash
mkdir -p /mnt/data/workspace
mkdir -p /mnt/data/datasets
mkdir -p /mnt/data/models
mkdir -p /mnt/data/checkpoints
```

Optional symlink:

```bash
mv ~/workspace ~/workspace_old 2>/dev/null || true
ln -s /mnt/data/workspace ~/workspace
```

---

## 14. Change VM machine type / GPU type

You usually need to stop the VM before changing machine type, GPU, or service account scopes.

```bash
gcloud compute instances stop  gpu-dev-vm --zone=us-central1-a
# Compute Engine -> VM instances -> gpu-dev-vm -> Edit
gcloud compute instances start gpu-dev-vm --zone=us-central1-a
```

### Better pattern for big changes

If you switch between CPU, single GPU, and multi-GPU often:

1. Keep important data on `/mnt/data` persistent disk
2. Stop old VM
3. Detach data disk
4. Create new VM with desired CPU/GPU
5. Attach the same data disk
6. Mount it at `/mnt/data`
7. Reinstall/check NVIDIA drivers if it's a GPU VM

---

## 15. Cloud Storage access — read-only vs write

If VM details show:

```text
Storage: Read Only
```

That **doesn't** mean you can't write local files. You can still create `.py`, `.ipynb`, logs, model files, folders. It only affects **Google Cloud Storage** API access from the VM (e.g. `gsutil cp file.txt gs://bucket/`).

To allow GCS writes, stop the VM and set scope:

```bash
gcloud compute instances stop gpu-dev-vm --zone=us-central1-a

gcloud compute instances set-service-account gpu-dev-vm \
  --zone=us-central1-a \
  --service-account=PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --scopes=https://www.googleapis.com/auth/cloud-platform

gcloud compute instances start gpu-dev-vm --zone=us-central1-a
```

Grant IAM only as needed. For writing to buckets:

```bash
gcloud projects add-iam-policy-binding ml-dev-project-123456 \
  --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --role=roles/storage.objectAdmin
```

---

## 16. Debugging checklist

### `gcloud: command not found`

```bash
brew list --cask
ls -la /opt/homebrew/share/google-cloud-sdk/bin/gcloud
echo 'export PATH="/opt/homebrew/share/google-cloud-sdk/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### SSH times out — usually firewall

```bash
gcloud compute firewall-rules list \
  --filter='network~default' \
  --format='table(name,direction,sourceRanges,allowed,disabled,targetTags)'
```

Make sure a rule allows `tcp:22` from your IP to your VM tag.

### SSH permission denied — usually key/user/IAM

```bash
gcloud compute ssh gpu-dev-vm --zone=us-central1-a --troubleshoot
gcloud compute config-ssh
```

### `nvidia-smi: command not found`

Driver missing — install and reboot (section 8).

### GPU not visible in PyTorch

```bash
nvidia-smi
conda activate gpu
python - <<'PY'
import torch
print(torch.__version__)
print(torch.cuda.is_available())
print(torch.cuda.device_count())
PY
```

Common causes: wrong PyTorch build, driver not installed, conda env not activated, `CUDA_VISIBLE_DEVICES` is empty.

### Jupyter not opening

```bash
jupyter lab --no-browser --ip=127.0.0.1 --port=8888
# from laptop:
ssh -L 8888:localhost:8888 gpu-dev-vm.us-central1-a.ml-dev-project-123456
# open http://localhost:8888
```

### Disk shows in `lsblk` but cannot use it

Probably not mounted. Check `lsblk`. If no mount point, format/mount and add to `/etc/fstab`.

### Out of space

```bash
df -h
lsblk
```

Fixes: resize boot disk, add data disk, move conda envs and datasets to `/mnt/data`, clean pip/conda caches, remove old Docker images.

---

## 17. Cost and safety tips

GPU VMs are expensive.

### Always stop when not using

```bash
gcloud compute instances stop  gpu-dev-vm --zone=us-central1-a
gcloud compute instances start gpu-dev-vm --zone=us-central1-a
```

> Stopped VMs generally stop compute/GPU charges, but **persistent disks still cost money while they exist**.

### Check what's running

```bash
gcloud compute instances list   # only running VMs incur compute/GPU charges
nvidia-smi                      # GPU processes on a VM
```

### Avoid public ports

Avoid opening `22`, `8888`, or random app ports to `0.0.0.0/0`. Use SSH tunnels or restricted IP ranges.

---

## 18. Quick command summary

### Local laptop

```bash
gcloud config set project ml-dev-project-123456
gcloud compute instances list
gcloud compute ssh gpu-dev-vm --zone=us-central1-a
gcloud compute config-ssh
ssh gpu-dev-vm.us-central1-a.ml-dev-project-123456
```

### Inside VM

```bash
nvidia-smi
conda activate gpu
python - <<'PY'
import torch
print(torch.__version__)
print(torch.cuda.is_available())
print(torch.cuda.device_count())
PY
```

### Start Jupyter (with tunnel)

VM:

```bash
conda activate gpu
cd ~/workspace
jupyter lab --no-browser --ip=127.0.0.1 --port=8888
```

Laptop:

```bash
ssh -L 8888:localhost:8888 gpu-dev-vm.us-central1-a.ml-dev-project-123456
# open http://localhost:8888
```

---

## 19. Recommended beginner workflow

1. Confirm project is correct.
2. Confirm quotas are available.
3. Create VM.
4. Add safe SSH firewall rule.
5. SSH in using `gcloud compute ssh`.
6. Generate SSH config with `gcloud compute config-ssh`.
7. Connect from VS Code Remote SSH.
8. Install NVIDIA driver if GPU VM.
9. Install Miniconda.
10. Create `gpu` and/or `cpu` conda environments.
11. Test `nvidia-smi` and PyTorch.
12. Use Jupyter through SSH tunnel.
13. Run long jobs in `tmux`.
14. Keep important data on persistent storage.
15. Stop VM when done.

---

## 20. Crisp tips for a new person

- Always check the active project before creating resources.
- Pick the zone based on **GPU availability**, not convenience.
- GPU quota errors are normal — request quota early.
- Use small/cheap GPUs for setup testing before creating expensive A100/H100 VMs.
- Do not open SSH or Jupyter to the whole internet.
- Use VS Code Remote SSH for interactive development.
- Use `tmux` for long-running jobs.
- Use `CUDA_VISIBLE_DEVICES=0` to force single-GPU runs.
- Use `torchrun --nproc_per_node=N` for proper multi-GPU training.
- Keep datasets and checkpoints on a separate persistent disk if possible.
- Local SSD is fast but temporary.
- Persistent disks still cost money when the VM is stopped.
- Stop GPU VMs when not actively using them.
- Run `nvidia-smi` often to see GPU usage.
- Run `df -h` often to avoid disk surprises.
- Keep a setup log with commands that worked.
