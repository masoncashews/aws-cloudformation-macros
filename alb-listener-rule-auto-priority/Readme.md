# ALB Listener Rule Weight (ALBListenerRuleAutoWeightTransform)

This macro automatically sets the weight of a rule when adding to an existing Application Load Balancer Listener.

&nbsp;
&nbsp;

***

## **Asset List**

Asset | Description
----- | -----------
/code/index.py | Not used, just where I edit the code before inserting into the cloudformation template.
/code/request-example.json | An example request packet for testing the lambda function created for the macro.
Readme.md | This markdown.
alb-listener-rule-auto-priority-custom-resource.yaml | The cloudformation stack to create the ALBListenerRuleAutoPriority Custom Resource.  Creates the Lambda, an execution role, and the cloudwatch log group.

&nbsp;
&nbsp;

***

## Deploying the Custom Resource

* Go to cloudformation in your environment and create a stack using [alb-listener-rule-auto-priority-custom-resource.yaml](alb-listener-rule-auto-priority-custom-resource.yaml).
  * I recommend giving the stack a name of `custom-ALBListenerRuleAutoPriority` for ease of reference
* The stack will create the following
  * The lambda function
  * The execution role for the lambda function
    * Permissions/Policies Given
      * Lambda Execution Role Managed Policy
      * Cloudwatch log group permissions (specific to this function)
      * Elastic Loadbalancer `Describe Rules` permission  
  * The cloudwatch log group to bue used by the function.
    * Retention period of 7 days.
  * Creates an Output/Export of `customALBListenerRuleAutoPriority` which will be called by other stacks that use this custom resource

&nbsp;
&nbsp;

***

## Using the custom resource

### Example - using it in a CloudFormation stack

```yaml
  ALBListenerRuleAutoPriorityResource:
    Type: Custom::ALBListenerRuleAutoPriorityResource
    Properties:
      ServiceToken:
        Fn::ImportValue: customALBListenerRuleAutoPriority
      ListenerArn: <ARN of the listener>

  ALBListenerRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties: 
      ...your other properties...
      ListenerArn: <ARN of the listener>
      Priority: !GetAtt ALBListenerRuleAutoPriorityResource.Priority
```
