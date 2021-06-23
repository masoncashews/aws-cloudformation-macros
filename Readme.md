# **AWS Cloudformation Macros**

The purpose of this project is to be a repository of cloudformation macros that can be reused in other [AWS Cloudformation Stacks](https://aws.amazon.com/cloudformation/).

***

&nbsp;
&nbsp;

## **Macros**

* [SG Ingress Transform](sg-ingress-transform)
  * This macro is used to dynamically add ingress rules to a [security group](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html) resource using a list of TCP ports and [CIDR](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) sources.
  
## **Custom Resources**

* [Load Balancer Listner Rule Auto Priority](alb-listener-rule-auto-priority)
  * This custom resource is used to automatically assign an available rule priority to a new listener rule for Elastic Loadbalancers on AWS.
  