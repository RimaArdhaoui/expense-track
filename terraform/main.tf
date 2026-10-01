resource "kubernetes_secret" "ledger_secrets" {
  metadata { name = "ledger-secrets" }
  data = { "secret-key" = var.app_secret_key }
}

resource "kubernetes_deployment" "ledger_app" {
  metadata {
    name   = "ledger-app"
    labels = { app = "ledger-app" }
  }
  spec {
    replicas = 1
    selector { match_labels = { app = "ledger-app" } }
    template {
      metadata { labels = { app = "ledger-app" } }
      spec {
        container {
          name              = "ledger-app"
          image             = var.image_name
          image_pull_policy = "Never"
          port { container_port = 5000 }
          env {
            name = "SECRET_KEY"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.ledger_secrets.metadata[0].name
                key  = "secret-key"
              }
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "ledger_app" {
  metadata { name = "ledger-app" }
  spec {
    selector = { app = "ledger-app" }
    type     = "NodePort"
    port {
      port        = 5000
      target_port = 5000
      node_port   = 30080
    }
  }
}