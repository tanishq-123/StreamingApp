aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 277385995709.dkr.ecr.us-east-1.amazonaws.com

for repo in frontend auth streaming admin chat; do
  docker push 277385995709.dkr.ecr.us-east-1.amazonaws.com/streamingapp/$repo:1.0.0
done