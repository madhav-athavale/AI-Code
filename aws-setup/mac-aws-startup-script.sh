aws ec2 run-instances \
  --image-id ami-02fe376e6ac9632c8 \
  --instance-type t3.small \
  --key-name NewKeyPair \
  --security-group-ids sg-06d190bebf4e78c72 \
  --iam-instance-profile Name=EC2-S3-SecretsManager-Profile \
  --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"VolumeSize":30}}]' \
  --user-data file://startup_script.sh \
  --region us-east-1 \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=my-server}]'