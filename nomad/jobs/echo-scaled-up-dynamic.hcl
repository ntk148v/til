job "http-echo" {
  datacenters = ["dc1"]

  group "echo" {
    // scale to 5 instances
    count = 5

    task "server" {
      driver = "docker"

      config {
        image = "hashicorp/http-echo:latest"
        // Nomad provides a number of Runtime Env variables https://www.nomadproject.io/docs/runtime/environment.html
        // NOMAD_PORT_<label>, the <label> is the name you gave to port (http).
        args  = [
          "-listen", ":${NOMAD_PORT_http}",
          "-text", "Hello and welcome to ${NOMAD_IP_http} running on port ${NOMAD_PORT_http}",
        ]
      }

      // dynamic port assignment https://www.nomadproject.io/docs/job-specification/network.html#dynamic-ports
      resources {
        network {
          mbits = 10
          port "http" {}
        }
      }
    }
  }
}
