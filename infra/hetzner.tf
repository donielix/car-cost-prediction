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
resource "hcloud_ssh_key" "cost_prediction_ssh" {
  name       = "cost_prediction_ssh"
  public_key = file("~/.ssh/id_ed25519.pub")
}

output "website" {
  value = "${hcloud_server.costprediction.ipv4_address}:8000"
}
