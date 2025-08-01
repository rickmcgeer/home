gcloud container node-pools create gpu-lora-train \
  --cluster YOUR_CLUSTER_NAME \
  --machine-type=n2-standard-8 \
  --accelerator type=nvidia-l4,count=1 \
  --num-nodes=0 \
  --enable-autoscaling --min-nodes=0 --max-nodes=1 \
  --node-taints=nvidia.com/gpu=true:NoSchedule \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --preemptible \
  --zone=us-west1-b
