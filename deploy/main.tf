provider "google" {
  project = "zinc-fusion-486709-b4"
  region  = "us-central1"
  zone    = "us-central1-a"
}

resource "google_compute_firewall" "allow_dbaas_bot" {
  name    = "allow-dbaas-bot-ports"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["8000", "4000", "8080"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["http-server", "https-server"]
}

# Create a instance for the DBaaS bot
resource "google_compute_instance" "dbaas_bot" {
  name         = "dbaas-bot-vm"
  machine_type = "e2-standard-2"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 50
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }

  metadata_startup_script = file("${path.module}/setup_dbaas_bot.sh")

  tags = ["http-server", "https-server"]

  service_account {
    email  = "default"
    scopes = ["cloud-platform"]
  }
}

output "instance_ip" {
  value = google_compute_instance.dbaas_bot.network_interface[0].access_config[0].nat_ip
}