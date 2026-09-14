for topic in streamingapp-deploy-success streamingapp-deploy-failure; do
  aws sns subscribe \
    --topic-arn arn:aws:sns:us-east-1:277385995709:$topic \
    --protocol lambda \
    --notification-endpoint arn:aws:lambda:us-east-1:277385995709:function:streamingapp-telegram-notifier \
    --region us-east-1

 aws lambda add-permission \
    --function-name streamingapp-telegram-notifier \
    --statement-id sns-$topic \
    --action lambda:InvokeFunction \
    --principal sns.amazonaws.com \
    --source-arn arn:aws:sns:us-east-1:277385995709:$topic \
    --region us-east-1
done
