# Oracle Cloud Always Free Deployment Guide — Akshaya Embroidery Design Selection

Complete step-by-step guide to hosting **Akshaya Embroidery Design Selection** on **Oracle Cloud Always Free Tier** for a permanent, 100% free live web URL with HTTPS SSL.

---

## 📌 Why Oracle Cloud Always Free?
- **Cost**: **$0.00 / month (Permanently Free)**.
- **Resource**: **Ampere A1 ARM Compute** (2 OCPUs, 12 GB RAM, 50 GB Storage) + **Permanent Static Public IP Address**.
- **No Expiration**: Always Free resources do not expire after trial.

---

## STEP 1: Create Your Oracle Cloud Always Free Account

1. Go to **[Oracle Cloud Free Tier Signup](https://www.oracle.com/cloud/free/)**.
2. Click **"Start for free"**.
3. Fill in your details:
   - **Country**: Choose your home country.
   - **Name & Email**: Use your primary email address.
4. **Select Home Region**:
   - Choose a region close to your business (e.g. *India West (Mumbai), Singapore, US East (Ashburn)*).
   - *Note: Choose carefully, Home Region cannot be changed later.*
5. **Add Payment Method**:
   - Oracle requires a Credit Card / Debit Card to verify identity.
   - A temporary small hold (~$1 USD) will be charged and immediately refunded. You will **NOT** be billed.
6. Complete account registration and log into the **Oracle Cloud Console**.

---

## STEP 2: Create Always Free ARM Instance (VM)

1. In the Oracle Cloud Console menu, click **Compute** $\rightarrow$ **Instances**.
2. Click **Create Instance**.
3. Configure the VM:
   - **Name**: `akshaya-embroidery-ai`
   - **Image**: Select **Ubuntu 22.04 LTS** or **Ubuntu 24.04 LTS (Minimal)**.
   - **Shape**: Click **Edit Shape** $\rightarrow$ Select **Ampere (ARM)** $\rightarrow$ Choose **VM.Standard.A1.Flex**.
     - Set **OCPUs**: `2`
     - Set **Memory**: `12 GB`
     - *(This is 100% Always Free eligible).*
4. **Networking**:
   - Select **Create new virtual cloud network (VCN)**.
   - Ensure **Assign a public IPv4 address** is selected as **Yes**.
5. **Save SSH Keys**:
   - Click **Save Private Key** (download `.key` / `.pem` file to your PC).
6. Click **Create**.
7. Wait 1-2 minutes until instance status shows **Running** and note down your **Public IP Address** (e.g. `129.213.x.x`).

---

## STEP 3: Open Port 80 & 443 in Oracle Ingress Rules

By default, Oracle Cloud blocks incoming web traffic. You must open HTTP (80) and HTTPS (443):

1. In your Instance details page, click on your **Subnet** link under Primary VNIC.
2. Click on the **Default Security List** for your VCN.
3. Click **Add Ingress Rules**:
   - **Source CIDR**: `0.0.0.0/0`
   - **IP Protocol**: `TCP`
   - **Destination Port Range**: `80, 443`
   - **Description**: `Web HTTP and HTTPS`
4. Click **Add Ingress Rules**.

---

## STEP 4: Connect to Your VM & Deploy Code

### 1. Connect via SSH (from Windows PowerShell)

```powershell
ssh -i "path\to\your\ssh-key.key" ubuntu@YOUR_PUBLIC_IP
```

### 2. Clone / Copy Your Codebase

```bash
# Clone your repository or upload files
git clone https://github.com/your-username/design_selection.git
cd design_selection
```

### 3. Run One-Click Deployment Script

```bash
# Make script executable & run
chmod +x deployment/deploy_oracle.sh
./deployment/deploy_oracle.sh
```

The script automatically installs Docker, configures `iptables` rules, builds your app, and launches the web app!

---

## STEP 5: Get a Permanent Free Custom Domain & HTTPS SSL URL

To give your customers a permanent branded link (e.g. `https://akshaya-embroidery.duckdns.org` or `https://akshayaembroidery.com`):

### Option A: Free Permanent Subdomain (DuckDNS)
1. Go to **[DuckDNS.org](https://www.duckdns.org/)** (Log in with Google/GitHub).
2. Create a free domain name: e.g. `akshaya-embroidery`.
3. Set the IP address to your **Oracle VM Public IP**.
4. Your permanent free URL will be: **`http://akshaya-embroidery.duckdns.org`**.

### Option B: Free HTTPS SSL Certificate (Let's Encrypt)
Run this command on your VM to add free SSL encryption:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d akshaya-embroidery.duckdns.org
```

Now your shop application will be live 24/7 with a secure **`https://`** URL!
