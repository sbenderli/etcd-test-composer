#!/usr/bin/env python3

import subprocess
import time
from antithesis.lifecycle import setup_complete

namespace = "default"
service = "etcd-headless"
replicas = 3

def wait_for_all_etcd():
    while True:
        all_healthy = True
        for i in range(replicas):
            pod_host = f"etcd-{i}.{service}.{namespace}.svc:2379"
            try:
                resp = subprocess.check_output(
                    ["curl", "-sf", f"http://{pod_host}/health"],
                    text=True
                )
                if '"health":"true"' not in resp:
                    print(f"[health-checker] {pod_host} unhealthy: {resp.strip()}")
                    all_healthy = False
            except subprocess.CalledProcessError:
                print(f"[health-checker] {pod_host} not reachable")
                all_healthy = False
        if all_healthy:
            break
        time.sleep(5)

wait_for_all_etcd()

print("[health-checker] all etcd members healthy!")
setup_complete({"Message": "ETCD cluster is healthy"})
