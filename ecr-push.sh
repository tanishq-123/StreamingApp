   for repo in frontend auth streaming admin chat; do
     aws ecr create-repository --repository-name streamingapp/$repo --region us-east-1
   done
