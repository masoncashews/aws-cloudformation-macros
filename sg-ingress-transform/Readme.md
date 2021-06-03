# SG Ingress Transform Macro (SGIngressTransformMacro)

This macro is used to dynamically add ingress rules to a [security group](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html) resource using a list of TCP ports and [CIDR](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) sources.

&nbsp;
&nbsp;

***

## **Asset List**

Asset | Description
----- | -----------
/code/index.py | Not used, just where I edit the code before inserting into the cloudformation template.
/code/request-example.json | An example request packet for testing the lambda function created for the macro.
example-sg-ingress-transform.yaml | An example cloudformation stack that uses the macro.
Readme.md | This markdown.
sg-ingress-transform.yaml | The cloudformation stack to create the SGIngressTransformMacro.  Creates the Lambda, an execution role, the cloudwatch log group, and the macro.

&nbsp;
&nbsp;

***

## Deploying the Macro

* Go to cloudformation in your environment and create a stack using [sg-ingress-transform.yaml](sg-ingress-transform.yaml).
  * I recommend giving the stack a name of `macro-SGIngressTransformMacro` for ease of reference
* The stack will create the following
  * The lambda function
  * The execution role for the lambda function
    * currently the only permissions given are to write cloudwatch logs
  * The cloudwatch log group to bue used by the function.
    * Retention period of 7 days.
  * The macro function `SGIngressTransformMacro`

&nbsp;
&nbsp;

***

## Using `SGIngressTransformMacro`

A working template can be found [here](example-sg-ingress-transform.yaml)

&nbsp;
&nbsp;

### Example #1

Explicitly listing the ports and CIDR subnets

```yaml
      
      SecurityGroupIngress:
        Fn::Transform:
          Name: SGIngressTransformMacro
          Parameters:
            AllowPorts:
              - 80
              - 443
            AllowCidrs:
              - 0.0.0.0/0
              - 127.0.0.1/32
```

This would result in ingress rules of the following.

Protocol | Port range | Source
--- | --- | ---
TCP | 80 | 0.0.0.0/0
TCP | 443 | 0.0.0.0/0
TCP | 80 | 127.0.0.1/32
TCP | 443 | 127.0.0.1/32

&nbsp;
&nbsp;

### Example #2

Using cloudformation template parameters of type `CommaDelimitedList`

```yaml
      
      SecurityGroupIngress:
        Fn::Transform:
          Name: SGIngressTransformMacro
          Parameters:
            AllowPorts: !Ref AllowPortsParameter
            AllowCidrs: !Ref AllowCidrsParameter
```
