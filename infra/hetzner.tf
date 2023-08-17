data "template_file" "user_data" {
  template = file("cloud-init.yaml")
  vars = {
    AWS_ACCESS_KEY_ID     = var.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = var.AWS_SECRET_ACCESS_KEY
    AWS_DEFAULT_REGION    = var.AWS_DEFAULT_REGION
  }
}

# Create a server
resource "hcloud_server" "costprediction" {
  name        = "costprediction"
  image       = "docker-ce"
  server_type = "cx21"
  location    = "fsn1"
  user_data   = data.template_file.user_data.rendered
  public_net {
    ipv4_enabled = true
    ipv6_enabled = true
  }
  ssh_keys = [hcloud_ssh_key.cost_prediction_ssh.id]
}

# Create a new SSH key

resource "tls_private_key" "ssh" {
  algorithm = "RSA"
  rsa_bits  = 4096
}


resource "local_file" "ssh_private_key_pem" {
  content         = tls_private_key.ssh.private_key_pem
  filename        = "${path.module}/.ssh/hetzner_private_key"
  file_permission = "0600"
}

resource "local_file" "ssh_public_key_pem" {
  content  = tls_private_key.ssh.public_key_openssh
  filename = "${path.module}/.ssh/hetzner_public_key"
}

resource "hcloud_ssh_key" "cost_prediction_ssh" {
  name       = "cost_prediction_ssh"
  public_key = local_file.ssh_public_key_pem.content
}

output "website" {
  value = "${hcloud_server.costprediction.ipv4_address}:8000"
}

output "ssh" {
  value = "ssh -i ${local_file.ssh_private_key_pem.filename} root@${hcloud_server.costprediction.ipv4_address}"
}
